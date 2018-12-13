#!/usr/bin/env python
##
#
# Detect Lane Lines in Colored Image using Image Masking
#
##
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Create figure for image
fig = plt.figure()

# Read and Display Image
image_color = mpimg.imread('/home/self-car/Autonomous-Car/application/lib/self-driving-cars/computer-vision/image_lane_c.jpg')
image_color.shape

# Specify where 'image_color' will be drawn in current figure using subplot
# add subplot to current figure with 1 row, 2 columns at index 1
# image will be drawn at row 1 in column 1
fig.add_subplot(1, 2, 1)

# Draw picture of image in subplot
plt.imshow(image_color)

# Mask Non White Colored Pixels in RGB Image
image_copy = np.copy(image_color)
image_copy.shape

# Check each non white pixel on all layers < 200, if true, then change pixel to black
image_copy[ (image_copy[:,:,0] < 200) | (image_copy[:,:,1] < 200) | (image_copy[:,:,2] < 200) ] = 0

# Specify where 'image_copy' will be drawn in current figure using subplot
# add subplot to current figure with 1 row, 2 columns at index 2
# image will be drawn at row 1 in column 2
fig.add_subplot(1, 2, 2)

# Draw picture image in subplot
plt.imshow(image_copy, cmap = 'gray')
plt.show()

