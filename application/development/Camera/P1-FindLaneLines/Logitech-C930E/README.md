# Finding Lane Lines on the Track

<img src="test_images_output/line_segments/1547786906080.jpeg" width="480" alt="Combined Image" />

Lane Line Detection Using RGB Color and Region Selection (Needs Improvement)

<img src="test_images_output/line_segments/cam_track_leftside.jpeg" width="480" alt="Combined Image" />

Lane Line Detection Using HSV Color and Region Selection and Hough Transform (After Improvement)

Overview
---

When we drive, we use our eyes to decide where to go.  The lines on the road that show us where the lanes are act as our constant reference for where to steer the vehicle. Naturally, one of the first things we did in developing a self-driving car is to automatically detect lane lines using an **lane finding pipeline algorithm**.

In this project, Python with OpenCV was used to detect lane lines in images.  OpenCV means "Open-Source Computer Vision", which is a package that has many useful tools for analyzing images.

Contents
---

- **[P1.ipynb](https://github.com/james94/Autonomous-Car/blob/master/application/development/Camera/P1-FindLaneLines/Logitech-C930E/P1.ipynb)**: project code
- **[writeup.md]()**: a brief writeup explaining my lane detection pipeline, shortcomings and potential improvements
- **README.md**: this file
- **data_pipeline_images/**: images to show each step of the pipeline process
- **notebook_checkpoints/**: notebooks that were saved as checkpoints I progressed through the project
- **test_images_output/**: test_images with lane lines detected, which contains two folders. **solid_line/** folder contains images with solid lines representing detected lane lines. **line_segments/** contains images with line segments representing detected lane lines.
- **test_videos_output/**: test videos with lane lines detected

How To Set Up Project
---

**Step 1:** Setup Python

Python 3 is needed. Python packages that you will use include numpy, matplotlib, OpenCV and moviepy. Jupyter notebook will be used to build the lane line detection application.

Choose **[Python 3 Anaconda](https://www.anaconda.com/download/#macos)** install package for your operating system. Download and install it.

~~~bash
conda create --name={environment-name} python=3 
source activate {environment-name}
~~~

**Step 2:** Installing OpenCV

~~~bash
pip install msgpack
pip install opencv-contrib-python
~~~

**Step 3:** Installing moviepy

~~~bash
pip install moviepy
~~~

**Step 4:** Opening the project in Jupyter Notebook

~~~bash
jupyter notebook
~~~
