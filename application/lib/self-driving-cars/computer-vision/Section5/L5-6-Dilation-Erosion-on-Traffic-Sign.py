#!/usr/bin/env python
##
#
# Perform Dilation and Erosion on Traffic Sign
#
##

# Dilation: adding extra pixels ot the boundaries of the objects in an image

# Erosion: removing pixels at the boundaries of objects in an image
import cv2
import numpy as np
import matplotlib.image as mpimg
from matplotlib import pyplot as plt

# Create figure for Matplotlib image
# fig = plt.figure()

# Read and Display Image
# Read image using OpenCV
image = cv2.imread('/home/self-car/Autonomous-Car/application/lib/self-driving-cars/computer-vision/Speed_Sign_View_2.jpg')

# Read image using Matplotlib
# image = mpimg.imread('/home/self-car/Autonomous-Car/application/lib/self-driving-cars/computer-vision/Speed_Sign_View_2.jpg')

# You can increase the effect of the erosion and dilation by increasing kernel size
# kernel = np.ones( (8,8), np.uint8 )
kernel = np.ones( (6,6), np.uint8 )

# Removing pixels from the white background means increasing the thickness of letters
image_erosion = cv2.erode(image, kernel, iterations = 1)

# Adding pixels to the white background, so letters appear thinner
image_dilation = cv2.dilate(image, kernel, iterations = 1)

# Display Input, Erosion Dilation Images using OpenCV
cv2.imshow('Input', image)
cv2.imshow('Erosion', image_erosion)
cv2.imshow('Dilation', image_dilation)

cv2.waitKey()
cv2.destroyAllWindows()

# Add subplot for current figure with 1 row, 3 columns at index 1
# fig.add_subplot(1, 2, 1)

# Draw Input image using Matplotlib
# plt.imshow(image)

# Add subplot for current figure with 1 row, 3 columns at index 2
# fig.add_subplot(1, 2, 2)

# Draw Erosion image using Matplotlib
# plt.imshow(image_erosion)

# Add subplot for current figure with 1 row, 3 columns at index 3
# fig.add_subplot(1, 2, 3)

# Draw Dilation image using Matplotlib
# plt.imshow(image_dilation)

# plt.show()

