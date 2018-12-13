#!/usr/bin/env python
##
#
# Detect Lane Lines in Gray Image using Image Masking
#
##
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Create figure
f = plt.figure()

# Read and Display Image
image_color = mpimg.imread('/home/self-car/Autonomous-Car/application/lib/self-driving-cars/computer-vision/image_lane_c.jpg')
image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)

# Specify subplot space for where to draw 'image_gray' picture
# add space for picture in subplot with 1 row and 2 columns in index 1
# Ref: https://pythonspot.com/matplotlib-subplot/
f.add_subplot(1, 2, 1)

# Draw the picture in subplot space
plt.imshow(image_gray, cmap = 'gray')

# Mask (blacken) Non White Colored Pixels in Image
image_copy = np.copy(image_gray)
image_copy.shape

image_copy[ (image_copy[:,:] < 250) ] = 0

# Specify subplot space for where to draw 'image_copy' picture
# add space for picture in subplot with 1 row and 2 columns in index 2
f.add_subplot(1, 2, 2)

# Display Detected Lane Lines in subplot space
plt.imshow(image_copy, cmap = 'gray')
plt.show()
