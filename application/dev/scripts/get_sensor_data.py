#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Header, Float64
import numpy as np
from threading import Thread
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
from sensor_msgs.msg import LaserScan, Imu
from scipy import signal, stats
import matplotlib.pyplot as plt
import math
from geometry_msgs.msg import Polygon, Point32, PolygonStamped
import time
from utils import pre_process_lidar_data
import csv
import sys
import os

##
#
# Ingest data from all sensors connected to MIT Racecar
#
##

class CarSensors():
    def __init__(self):
        # base_dir = "/media/nvidia/6139-3863/car_sensors"
        base_dir = "/home/nvidia/Autonomous-Car/application/data"
        self.sensor_dir = [base_dir+"/lidar_scan/", base_dir+"/imu_data/"]

        # Subscribe to LiDAR "/scan" topic with data being published by the "/laser_node", 
        # call lidar_callback method when data takes up 1 space in queue
        # In terminal, run ROS command to see lidar data: "rostopic echo "/scan"
        self.sub_lidar_scan = rospy.Subscriber("/scan", LaserScan, self.lidar_callback, queue_size = 1)
        
        # Subscribe to IMU "/imu/data" topic with data being published by the "/imu_node",
        # In terminal, run ROS command to see imu data: "rostopic echo "/imu/data"
        self.sub_imu_data = rospy.Subscriber("/imu/data", Imu, self.imu_callback, queue_size = 1)

        # TODO: Need to subscribe to battery sensor, electronic speed controller for speed and steering
        # and Camera sensor

        # Check if sensor directories do not exist, if true, then create them
        for dirname in self.sensor_dir:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
                rospy.loginfo("Created: %s", dirname)

    def lidar_callback(self, lidar_raw_msg):
        """Write raw LiDAR data to txt file:
           Data can be used for path planning, object segmentation, obstacle avoidance
        """
        lidar_raw_file = self.sensor_dir[0] + "lidar-" + time.strftime("%H-%M-%S") + ".txt"
        
        with open(lidar_raw_file, "w") as file: # Use file to refer to file object
            file.write(str(lidar_raw_msg))

    def imu_callback(self, imu_raw_msg):
        """
           Write raw IMU data to txt file:
           Data can be used for linear acceleration, angular rotation velocity, magnetic field vectors
        """
        imu_raw_file = self.sensor_dir[1] + "imu-" + time.strftime("%H-%M-%S") + ".txt"
        with open(imu_raw_file, "w") as file: # Use file to refer to file object
            file.write(str(imu_raw_msg))

if __name__=="__main__":
    rospy.init_node("get_car_data")
    CarSensors()
    rospy.spin()
