#!/usr/bin/env python
##
#
# Perform Perspective Transform on Traffic Sign
#
##

# Perspective transformation changes the perspective of how the image is
# viewed, so our self-driving car can view it from the front
import cv2
import numpy as np
import matplotlib.image as mpimg
from matplotlib import pyplot as plt

# Read and Display image using OpenCV
image = cv2.imread('/home/self-car/Autonomous-Car/application/lib/self-driving-cars/computer-vision/Speed_Sign_View_2.jpg')
cv2.imshow('Original Image', image)
# Waits until a keyboard key is pressed to destory window
cv2.waitKey()
cv2.destroyAllWindows()

# Read and Display image using Matplotlib
# image = mpimg.imread('/home/self-car/Autonomous-Car/application/lib/self-driving-cars/computer-vision/Speed_Sign_View_2.jpg')
# plt.imshow(image)

height, width = image.shape[:2]

print("height = %d" %(height))
print("width = %d" %(width))

# Coordinates of the 4 corners of the original image
first_src_pt = [200,60]
second_src_pt = [450,150]
third_src_pt = [520,500]
fourth_src_pt = [170,470]
Source_points = np.float32([ first_src_pt, second_src_pt, third_src_pt, fourth_src_pt ])

# Coordinates of the 4 corners of the desired output
first_dst_pt = [0,0]
second_dst_pt = [width,0]
third_dst_pt = [width,height]
fourth_dst_pt = [0,height]
Destination_points = np.float32([ first_dst_pt, second_dst_pt, third_dst_pt, fourth_dst_pt ])

# Use the two sets of four points to compute the Perspective Transformation matrix, M
M = cv2.getPerspectiveTransform(Source_points, Destination_points)

warped = cv2.warpPerspective(image, M, (width, height))

# Display warped image using OpenCV
cv2.imshow('warped Image', warped)
# Waits until a keyboard key is pressed to destory window
cv2.waitKey()
cv2.destroyAllWindows()

# Draw warped image using Matplotlib
# plt.imshow(warped)

