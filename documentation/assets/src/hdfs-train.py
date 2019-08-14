import os
import pydoop.hdfs as hpath
import pydoop.hdfs.path as kpath
import csv
import pandas as pd
import cv2
import numpy as np
import PIL
import io
import pickle
from matplotlib.pyplot import imshow
from IPython.display import Image, display

def get_image(basepath, filepath):
    # read in images from center, left and right cameras
    source_path = filepath
    # an easy way to update the path is to split the path on it's
    # slashes and then extract the final token, which is the filename
    filename = source_path.split('/')[-1]
    # then I can add that filename to the end of the path to the IMG
    # directory here on the AWS instance
    img_path_on_fs = basepath + filename
    # once I have the current path, I can use opencv to load the image
    with hpath.open(img_path_on_fs, encoding='utf-8') as imgFile:
      
      colourImg = PIL.Image.open(imgFile)
      nparray = np.asarray(colourImg)
      image = cv2.cvtColor(nparray, cv2.COLOR_RGB2BGR)
      
    return image


brand = "logitech"
mode = "image"

os.chdir("/tmp/")
myMachine = kpath.abspath('/tmp/csdv/data/input/racetrack/image/')
saveDir = kpath.abspath('/tmp/csdv/output/')

with hpath.open(myMachine+"driving_log.csv") as csvFile:
  df=pd.read_csv(csvFile, names=["image_center","image_left","image_right","steering","speed"])

#next(df.iterrows())[1]
df.iterrows()


# read and store multiple cameras and steering angles from driving_log.csv
# all three camera images will be used to train the model
images = []
steering_measurements = []

for index, row in df.iterrows():
  steering_center = float(row[3]) #row, column 3 = steering angle

  # create adjusted steering measurements for the side camera images
  correction = 0.2 # parameter to tune
  # steering left of center, recover back to center
  steering_left = steering_center - correction
  # steering right of center, recover back to center
  steering_right = steering_center + correction

  # read in images from center, left and right cameras
  basepath = myMachine + brand + "/"
  image_center = get_image(basepath, row[0])
  image_left = get_image(basepath, row[1])
  image_right = get_image(basepath, row[2])
  
  # insert multiple elements into list
  images.extend([image_center, image_left, image_right])
  steering_measurements.extend([steering_center, steering_left, steering_right])
  

# Data Augmentation.
# There's Problem where the model sometimes pulls too hard to the right. 
# This does/nt make sense since the training track is a loop and the car 
# drives counterclockwise. So, most of the time the model should learn to steer 
# to the left. Then in autonomous mode, the model does steer to the left
# even in situations when staying straight might be best. One approach to mitigate
# this problem is data augmentation. There are many ways to augment data to expand
# the training set and help the model generalize better. I could change the brightness
# on the images or I could shift them horizontally or vertically. In this case,
# I'll keep things simple and flip the images horizontally like a mirror, then invert
# the steering angles and I should end up with a balanced dataset that teaches the
# car to steer clockwise as well as counterclockwise. Just like using side camera data,
# using data augmentation carries 2 benefits: 1. we have more data to use for training 
# the network and 2. the data we use for the training the network is more comprehensive.
augmented_images, augmented_steering_measurements = [], []
for image, measurement in zip(images, steering_measurements):
    augmented_images.append(image)
    augmented_steering_measurements.append(measurement)
    augmented_images.append(cv2.flip(image,1)) # flip img horizontally
    augmented_steering_measurements.append(measurement*-1.0) # invert steering

# now that I've loaded the images and steering measurements,
# I am going to convert them to numpy arrays since that is the format
# keras requires
X_train = np.array(augmented_images)
y_train = np.array(augmented_steering_measurements)

# next I am going to build the most basic network possible just to make sure everything is working
# this single output node will predict my steering angle, which makes this
# a regression network, so I don't have to apply an activation function

from keras.models import Sequential
from keras.layers import Flatten, Dense, Activation, Lambda, Cropping2D
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D

# Building Net Architecture based on Nvidia Self Driving Car Neural Network 
model = Sequential()
# Layer 1: Normalization
# Data preprocessing to normalize input images
model.add(Lambda(lambda x: (x/255.0) - 0.5, input_shape = (180, 320, 3)))
# Crop2D layer used to remove top 40 pixels, bottom 30 pixels of image
model.add(Cropping2D(cropping = ((40,30), (0,0))))
# Layer 2: Convolutional. 24 filters, 5 kernel, 5 stride, relu activation function
model.add(Conv2D(24,5,5, subsample = (2,2), activation = "relu"))
# Layer 3: Convolutional. 36 filters
model.add(Conv2D(36,5,5, subsample = (2,2), activation = "relu"))
# Layer 4: Convolutional. 48 filters
model.add(Conv2D(48,5,5, subsample = (2,2), activation = "relu"))
# Layer 5: Convolutional. 64 filters
model.add(Conv2D(64,5,5, activation = "relu"))
# Layer 6: Convolutional. 64 filters
model.add(Conv2D(64,5,5, activation = "relu"))
### Flatten output into a vector
model.add(Flatten())
# Layer 7: Fully Connected
model.add(Dense(100))
# Layer 8: Fully Connected
model.add(Dense(50))
# Layer 9: Fully Connected
model.add(Dense(10))
# Layer 10: Fully Connected
model.add(Dense(1))

# with the network constructed, I will compile the model
# for the loss function, I will use mean squared error (mse)
# What I want to do is minimize the error between the steering
# measurement that the network predicts and the ground truth steering
# measurement. mse is a good loss function for this
model.compile(loss='mse', optimizer='adam')

# once the model is compiled, I will train it with the feature and label
# arrays I just built. I'll also shuffle the data and split off 20% of
# the data to use for a validation set. I set epochs to 7 since I saw
# with 10 epochs (keras default) that validation loss decreases with just 7,
# then increases. Thus, at 10 epochs, I may have been overfitting training data.
# Hence, at 7 epochs, the validation loss decreases for almost all the epochs.
# Change 7 epochs to 5 since we are training over more powerful neural net architecture
# update with data augmentation: training is going fine and is training on twice as
# many images as before. That makes sense since I copied each image and then flipped
# the copy
model.fit(X_train, y_train, validation_split=0.2, shuffle=True, epochs=7)

# finally I'll save the trained model, so later I can download it onto my 
# local machine and see how well it works for driving the simulator

with hpath.open(saveDir+"model.h5", "w") as file_model:
  pickle.dump(model, file_model)
