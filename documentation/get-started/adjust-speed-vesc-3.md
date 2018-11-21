# Adjust Car Speed using VESC YAML File

You will adjust the car's speed in the forward and reverse direction by modifying
configuration parameters in the vesc.yaml file.

## Prerequisites

- Get the Car Moving with the Game Controller

## Modify the Speed Parameters in VESC YAML File

~~~bash
cd ~/racecar-ws/src/racecar/racecar/config/racecar-v2/
gedit vesc.yaml
~~~

Currently **speed_to_erpm_gain** may be set to **4614**, which means the
electrical rotations per minute in either forward or reverse direction is
4614/-4614. We want to make the car move faster, so first we must modify this
value.

~~~yaml
speed_to_erpm_gain: 18000
~~~

Currently the speed in the forward and reverse direction for the **vesc_driver**
parameter denote **speed_max** at **3250** and denote **speed_min** at **-3250**
. We can update these two parameters to control speed in both directions.

~~~yaml
vesc_driver:
  ...
  speed_min: -4000 # reverse direction(max -18000)
  speed_max: 12000 # forward direction(max 18000)
~~~

The reverse direction for the car will be noticeably slower than the forward
direction.

Save the file.

## Launch the ROS Program to Activate Car Wheels

Run the following command in an open terminal on Jetson Ubuntu:

~~~bash
# CMD Definition: roslaunch package_name file.launch
roslaunch racecar teleop.launch
~~~

> Note: the above command activates the laser scanner, telop and wheel controls

## Control the Car Wheels with the Game Controller

Press the **Logitech** button in the center of the game controller to power it on.

Press **LB** button to take control of the car's wheels.

To move the car forward, on the direction pad, press the **UP** direction.

To move the car backward, on the direction pad, press the **DOWN** direction.

To steer left, move the **right joystick** toward the **left** direction.

To steer right, move the **right joystick** toward the **right** direction.

[![car-moving.jpg](../images/car-moving.jpg)](https://www.youtube.com/watch?v=SD1wBIz1uDU&feature=youtu.be)

**Figure 2:** Image navigates to second video with car moving at various speeds
