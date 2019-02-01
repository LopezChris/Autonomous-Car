#!/usr/bin/env python

from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
from geometry_msgs.msg import Polygon, Point32, PolygonStamped
from std_msgs.msg import String, Header, Float64
from sensor_msgs.msg import LaserScan, Imu, Image
from cv_bridge import CvBridge, CvBridgeError
from utils import pre_process_lidar_data
from scipy import signal, stats
from threading import Thread

import matplotlib.pyplot as plt
import sensor_msgs.msg
import numpy as np
import cStringIO
import roslib
import rospy
import uuid
import math
import time
import csv
import sys
import cv2
import os

##
#
# Ingest data from all sensors connected to Racecar
#
##

FRAME_RATE = 30
USE_LOGIC_CAMERA = 1

class LogCarSensors():
    def __init__(self, save_base_dst):
        # Store Data in sensor_dir
        self.base_dir = save_base_dst
        # self.base_dir = "/media/nvidia/6139-3863/data/track"
        # self.base_dir = "/home/nvidia/Autonomous-Car/application/data/track"
        self.sensor_dir = [self.base_dir+"/lidar_scan/", self.base_dir+"/imu_data/", 
                           self.base_dir+"/motor_speed/", self.base_dir+"/servo_steering/", 
                           self.base_dir+"/cam_frames/"]

        # Initialize data recording
        self.record = 0

        # Initialize sensor data attributes
        self.lidar_raw_data = -1
        self.imu_raw_data = -1
        self.speed_raw_data = -1
        self.steering_raw_data = -1
        self.camera_raw_np_img = []

        self.last_time_stamp = -1

        # Camera sensor, check which topic to use
        if USE_LOGIC_CAMERA:
            # Subscribe to Cam "/webcam/image_raw/" topic with data published by the "/webcam_node",
            # In terminal, run ROS command to see camera data: "rostopic echo "/webcam/image_raw/"
            camera_topic = "/webcam/image_raw/"
        else:
            left_camera_raw_topic = "/zed/left/image_raw_color"
            left_camera_rect_topic = "/zed/left/image_rect_color"
            right_camera_raw_topic = "/zed/right/image_raw_color"
            right_camera_rect_topic = "/zed/right/image_rect_color"

        # Camera sensor, check which topic to use
        if USE_LOGIC_CAMERA:
            # Subscribe to Cam "/webcam/image_raw/" topic with data published by the "/webcam_node",
            # In terminal, run ROS command to see camera data: "rostopic echo "/webcam/image_raw/"
            self.sub_camera = rospy.Subscriber(camera_topic, Image, self.camera_callback)
        else:
            self.sub_camera = rospy.Subscriber(right_camera_rect_topic, Image, self.zos_camera_callback)

        # Check if sensor directories do not exist, if true, then create them
        for dir_name in self.sensor_dir:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
                rospy.loginfo("Created: %s", dir_name)

        # Subscribe to Joy "/joy" topic with data being published by the "/joy_node",
        # In terminal, run ROS command to see joy data: "rostopic echo "/joy"
        self.sub_joy = rospy.Subscriber("/joy", sensor_msgs.msg.Joy, self.joy_callback)

        # Subscribe to LiDAR "/scan" topic with data being published by the "/laser_node", 
        # call lidar_callback method when data takes up 1 space in queue
        # In terminal, run ROS command to see lidar data: rostopic echo "/scan"
        self.sub_lidar_scan = rospy.Subscriber("/scan", LaserScan, self.lidar_callback, queue_size = 1)
        
        # Subscribe to IMU "/imu/data" topic with data being published by the "/imu_node",
        # In terminal, run ROS command to see imu data: "rostopic echo "/imu/data"
        self.sub_imu_data = rospy.Subscriber("/imu/data", Imu, self.imu_callback, queue_size = 1)

        # Subscribe to ESC "..speed" topic with data being published by the "/vesc/ackermann_to_vesc" node
        # In terminal, run ROS command to see car speed data: rostopic echo "/vesc/commands/motor/speed"
        # Driving forward speed = 2307.0, driving reverse speed = -2307.0
        self.sub_esc_speed = rospy.Subscriber("/vesc/commands/motor/speed", Float64, 
                                              self.speed_callback, queue_size = 1)

        # Subscribe to ESC "..position" topic with data being published by the "/vesc/ackermann_to_vesc" node
        # In terminal, run ROS command to see steering angle: rostopic echo "/vesc/commands/motor/speed"
        # Steering right = 0.94299000434, steering left = 0.11780999566
        self.sub_esc_steering = rospy.Subscriber("/vesc/commands/servo/position", Float64,
                                                 self.steering_callback, queue_size = 1)

        # TODO: Need to subscribe to battery sensor
        
        # Bridge for converting ROS Image to CV2 Image
        self.bridge = CvBridge()

        # Store filenames for sensor data into csv file
        csv_file = open(self.base_dir + "/sensor_data.csv", "ab")

        self.csv_writer = csv.writer(csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
		
        self.csv_writer.writerow(["camera_frame", "lidar_scan", "esc_speed",
                                  "esc_steering", "imu"])

    def joy_callback(self, joy_raw_msg):
        """Sets ON or OFF flag for recording data from all sensors.
           When B is pressed, data recording is off, but if Y is pressed, data recording on.
        """
        if joy_raw_msg.buttons[2] == 1: # B button
            self.record = 0
            rospy.logerr("Data Recording Off! %s", str(self.record))
        if joy_raw_msg.buttons[3] == 1: # Y button
            self.record = 1
            rospy.logerr("Data Recording On! %s", str(self.record))

    def lidar_callback(self, lidar_raw_msg):
        """Write raw LiDAR data to txt file:
           Data can be used for path planning, object segmentation, obstacle avoidance
        """
        # Check if data recording on
        if self.record != 1:
            return

        self.lidar_raw_data = lidar_raw_msg

    def imu_callback(self, imu_raw_msg):
        """
           Write raw IMU data to txt file:
           Data can be used for linear acceleration, angular rotation velocity, magnetic field vectors
        """
        # Check if data recording on
        if self.record != 1:
            return

        self.imu_raw_data = imu_raw_msg

    def speed_callback(self, speed_raw_msg):
        """
           Write raw speed data to txt file:
           Data can be used for tracking motor speed
        """
        # Check if data recording on
        if self.record != 1:
            return

        self.speed_raw_data = speed_raw_msg

    def steering_callback(self, steering_raw_msg):
        """
           Write raw steering data to txt file:
           Data can be used for tracking servo steering angle
        """
        # Check if data recording on
        if self.record != 1:
            return

        self.steering_raw_data = steering_raw_msg

    def camera_callback(self, ros_image_msg):
        """
           Store camera frame to jpeg file:
           Data can be used for detecting lane lines, lane curvature, etc
        """
        # Check if data recording on
        if self.record != 1:
            return

        # Get current time before saving frame
        current_time = long(time.time() * 1000.0)
        print("current_time=%f; last_timestamp=%f" %(current_time, self.last_time_stamp))
        # Check if ms to capture next frame has passed, if not, then exit function
        if current_time - self.last_time_stamp < 1000 / FRAME_RATE:
            return
        # Assign last_time_stamp with new timestamp since we are ready to save another frame
        self.last_time_stamp = current_time

        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            frame = self.bridge.imgmsg_to_cv2(ros_image_msg, "bgr8")
        except CvBridgeError, e:
            print(e)

        # Convert image to Numpy array, most cv2 functions require Numpy arrays
        np_img = np.array(frame, dtype = np.uint8)

        # Convert camera_raw_data from list to numpy array
        self.camera_raw_np_img = np_img

        # Based on camera frames that are captured, save the sensor data recorded per frame
        self.save_sensor_data()

    def save_sensor_data(self):
        """
           Save car's sensor data into csv
        """
        unique_id = str(uuid.uuid4())

        # Saved np_img frame with cam_write_file value
        cam_filename = "cam-" + time.strftime("%H-%M-%S") + "-" + unique_id + ".jpeg"
        cam_raw_file = self.sensor_dir[4] + cam_filename

        res_saved_file = cv2.imwrite(cam_raw_file, self.camera_raw_np_img)

        # Save Raw LiDAR data at filepath
        lidar_filename = "lidar-" + time.strftime("%H-%M-%S") + "-" + unique_id + ".txt"
        lidar_raw_file = self.sensor_dir[0] + lidar_filename

        with open(lidar_raw_file, "w") as file: # Use file to refer to file object
            file.write(str(self.lidar_raw_data))

        # Save Raw Speed data at filepath
        speed_filename = "speed-" + time.strftime("%H-%M-%S") + "-" + unique_id + ".txt"
        speed_raw_file = self.sensor_dir[2] + speed_filename

        with open(speed_raw_file, "w") as file:
            file.write(str(self.speed_raw_data))

        # Save Raw Steering data at filepath
        steering_filename = "steering-" + time.strftime("%H-%M-%S") + "-" + unique_id + ".txt"
        steering_raw_file = self.sensor_dir[3] + steering_filename

        with open(steering_raw_file, "w") as file:
            file.write(str(self.steering_raw_data))

        # Save Raw IMU data at filepath
        imu_filename = "imu-" + time.strftime("%H-%M-%S") + "-" + unique_id + ".txt"
        imu_raw_file = self.sensor_dir[1] + imu_filename

        with open(imu_raw_file, "w") as file: # Use file to refer to file object
            file.write(str(self.imu_raw_data))

        # check if path doesn't exist, then return
        #sensor_filename = []
        #if not os.path.exists(sensor_filename):
        #    rospy.logerr("sensor filepath doesn't exist: %s", sensor_filename)
        #    return  

        self.csv_writer.writerow([cam_filename, lidar_filename, speed_filename,
                                  steering_filename, imu_filename])

        rospy.logerr("============ Recording All Sensor Data Per Frame =============")

if __name__=="__main__":
    save_base_dst = "/media/nvidia/6139-3863/log_car_sensors/outdoor"
    #save_base_dst = "/media/nvidia/6139-3863/log_car_sensors/outdoor_garage"
    #save_base_dst = "/media/nvidia/6139-3863/log_car_sensors/clockwise_rightside_tracklane"
    #save_base_dst = "/media/nvidia/6139-3863/log_car_sensors/counterclockwise_rightside_tracklane"
    #save_base_dst = "/media/nvidia/6139-3863/log_car_sensors/clockwise_leftside_tracklane"
    #save_base_dst = "/media/nvidia/6139-3863/log_car_sensors/counterclockwise_leftside_tracklane"
    rospy.init_node("log_car_sensors")
    LogCarSensors(save_base_dst)
    rospy.spin()
