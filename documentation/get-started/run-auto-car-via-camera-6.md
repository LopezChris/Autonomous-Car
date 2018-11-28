# Run Car in Autonomous Camera Mode

# Launch ROS Process to Start Autonomous Camera Mode

Open the terminal:

~~~bash
roslaunch hdp_pilot run_withcam.launch
~~~

The above command launches multiple ROS processes for the car to be in
autonomous camera mode.

> Note: The ROS launch command includes ROS package files teleop.launch, mux.launch
webcam.launch which contains access to the game controller and wheels,
front-wheel steering, camera and the laser. run_withcam.py script also is
launched as a ROS process.

## Place the Car in Track

![car_on_track.jpg](../images/car_on_track.jpg)

## Turn on or off Car Autonomous LiDAR Mode

On the game controller, press **Y** button to turn on autonomous mode.

Press **B** button to turn off autonomous mode.
