#!/usr/bin/env python
##
#
# Detect Lane Lines in an Image using Hough Transform
#
##
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Create figure for pictures
fig = plt.figure()

# Read and Show Image
image_c = mpimg.imread('/home/self-car/Autonomous-Car/application/lib/self-driving-cars/computer-vision/new_test_image_3.jpg')
image_c.shape

# Add subplot to current figure with 2 rows, 4 columns at index 1
fig.add_subplot(2, 4, 1)

# Draw 'image_c' in subplot
plt.imshow(image_c)

# Convert RGB Image to Greyscale Image
image_g = cv2.cvtColor(image_c, cv2.COLOR_RGB2GRAY)
image_g.shape

# Add subplot to current figure with 2 rows, 4 columns at index 2
fig.add_subplot(2, 4, 2)

plt.imshow(image_g, cmap = 'gray')

# Apply Gaussian Blurring and Canny Edge Detection
# Gaussian Blurring
image_blurred = cv2.GaussianBlur(image_g, (7, 7), 0)

# Add subplot to current figure with 2 rows, 4 columns at index 3
fig.add_subplot(2, 4, 3)

plt.imshow(image_blurred, cmap = 'gray')

# Canny Edge Detection
threshold_low = 10
threshold_high = 200

image_canny = cv2.Canny(image_blurred, threshold_low, threshold_high)

# Add subplot to current figure with 2 rows, 4 columns at index 4
fig.add_subplot(2, 4, 4)

plt.imshow(image_canny, cmap = 'gray')

# Define Region of Interest
# Get rid of canny edge detected areas not interested in
vertices = np.array( [[ (20,460),(340,300),(460,300),(740,460) ]], dtype=np.int32 )
mask = np.zeros_like(image_g)
cv2.fillPoly(mask, vertices, 255)
# Pass in gray image for bitwise and operation to mask pixels not in region of interest
masked_image = cv2.bitwise_and(image_g, mask)

# Add subplot to current figure with 2 rows, 4 columns at index 5
fig.add_subplot(2, 4, 5)

plt.imshow(masked_image)

# Pass in canny image for bitwise and operation to mask pixels not in region of interest
masked_image = cv2.bitwise_and(image_canny, mask)

# Add subplot to current figure with 2 rows, 4 columns at index 6
fig.add_subplot(2, 4, 6)

plt.imshow(masked_image)

# Hough Lines Detection and Draw Function
# Distance resolution in pixels
rho = 2
# Angular resolution in Radians
theta = np.pi/180
# Minimum Number of Votes
threshold = 40
# Minimum Number of pixels making up a line
min_line_len = 100
# Maximum gap in pixels between connectable line segments
max_line_gap = 50

lines = cv2.HoughLinesP(masked_image, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)

# Create an empty black image
line_image = np.zeros((masked_image.shape[0], masked_image.shape[1], 3), dtype=np.uint8)

for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(line_image, (x1,y1), (x2,y2), [0,255,0], 20)

lines

# Greek Variables
alpha = 1
beta = 1
gamma = 0

# Resultant weighted image is calculated as follows: 
# original_img * alpha + img * beta + gamma
Image_with_lines = cv2.addWeighted(image_c, alpha, line_image, beta, gamma)

# Add subplot to current figure with 2 rows, 4 columns at index 7
fig.add_subplot(2, 4, 7)

# Draw picture with lane lines detected in subplot
plt.imshow(Image_with_lines)

# Display picture of figure with subplot indices
plt.show()
