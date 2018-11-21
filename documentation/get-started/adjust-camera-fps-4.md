# Adjust Frames Per Second using video_stream_opencv

You can increase the frames per second (FPS) to potentially increase the amount
of images that are captured when the car is recording video.

## Check Video Camera Configurations Currently Applied

By running the following ROS process, we can see if our camera configurations
were successful:

~~~bash
roslaunch video_stream_opencv webcam.launch
~~~

From the output, we can see what we are trying to set the camera FPS to **40**,
what the camera actually reports for FPS **30** and what we are throttling from
the FPS **40**.

We need to check what the FPS limitation for the camera. Is 30 FPS the most we
can do?

Press **ctrl + C** to exit the ROS process.

## Check Supported Webcam Resolutions

Assuming the webcam be accessed via lsusb, use the command:

~~~bash
lsusb
lsusb -s <Bus>:<Device> -v | egrep "Width|Height"
~~~

Ex: `lsusb -s 001:025 -v | egrep "Width|Height"``

You will get output with the image resolution size and the fps associated.
To increase the frame per second from **30** fps to **120** fps, we could manipulate
the resolution to be **1280 x 720**.

The current image width **640** and image height **480**, which we saw from
ros webcam.launch.

## Check Supported Webcam FPS and Resolution Needed

Let's list the following video camera devices connected to the car:

~~~
v4l2-ctl --list-devices
~~~

You should see resolution and their associated FPS. This output should show us
whether our device allows for more than 30 FPS if a different resolution is
selected.

> Note: to change the resolution, we can use OpenCV.

> Problem: I wasn't able to see the logitech webcam using the above command,
but I was able to see it using lsusb.

## Modify Resolution for Webcam

If we want to achieve higher FPS, we need to modify the **[webcam.launch](https://github.com/ros-drivers/video_stream_opencv/blob/master/launch/webcam.launch)** in the
ROS **video_stream_opencv** package.

~~~
cd ~/racecar-ws/src/video_stream_opencv/launch/
cp webcam.launch webcam.launch.bak
gedit webcam.launch
~~~

Make sure the **appropriate video camera device is selected**. For instance, since
our camera appears on **/dev/video1**, we need to change **value=0** to
**value=1** for **video_stream_provider**.

~~~xml
<arg name="video_stream_provider" value="1" />
~~~

Now based on if the webcam device supports more than 30FPS, we can increase FPS.
Let's increase FPS from **30FPS** to **60FPS**.

~~~xml
<arg name="set_camera_fps" value="60"/>
~~~

Let's also increase the number frames that can be accessed when we issue a
query:

~~~xml
<!-- throttling the querying of frames to -->
<arg name="fps" value="60" />
~~~

Lets also change the dimensions of the image from default width x height
**640x480** to **1920x1080**.

~~~xml
<arg name="width" value="1920"/>
<arg name="height" value="1080"/>
~~~

## Re-Check Video Camera Configurations That Were Modified

Re-run the following command:

~~~bash
roslaunch video_stream_opencv webcam.launch
~~~

If our camera allows for more than **30FPS**, then we should see **60FPS**
in our output.

## Launch Camera Frame Recording ROS Process

Open second terminal window:

~~~bash
roslaunch hdp_pilot recording.launch
~~~

The above command launches a ROS process that allows the user to turn on or off recording by using the game controller.

Now when you record frames, you should obtain more images because FPS is higher.

## Further Reading

- [ROS video_stream_opencv package](http://wiki.ros.org/video_stream_opencv), talks about modifying the parameters used in video camera streaming
- [ROS controlReading.py](https://gitlab.com/saumitra_bg/hdp-pilot/blob/master/hdp_pilot/scripts/controlRecording.py)
