# Run Car in Autonomous LiDAR Mode

## Launch ROS Program for Autonomous LiDAR Mode

Open the terminal:

~~~bash
roslaunch hdp_pilot run_withlidar.launch
~~~

The above command launches multiple ROS processes for the car to be in
autonomous LiDAR mode.

> Note: The ROS launch command includes ROS package files teleop.launch and mux.launch
which contains access to the game controller and wheels, front-wheel steering
and the laser. run_withlidar.py script also is launched as a ROS process.

## Place the Car in Track

![car_on_track.jpg](../images/car_on_track.jpg)

## Turn on or off Car Autonomous LiDAR Mode

On the game controller, press **Y** button to turn on autonomous mode.

Press **B** button to turn off autonomous mode.
