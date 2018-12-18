#!/usr/bin/env python
import ast

class DrawLidarScan():
    def __init__(self):
        base_dir = "/home/self-driving-car/Autonomous-Car/application/data"
        self.sensor_dir = base_dir+"/lidar_scan/"

        filename = self.sensor_dir+"lidar-08-38-40.txt"

        lidar_data = self.extract_lidar_file_data(filename)

        range_key, range_values = self.get_lidar_ranges(lidar_data)

        # Use a dictionary to hold the key value pair since value is a list
        lidar_scan_range = { range_key: range_values }

        # Print key and range values in string list
#        print("range_key = %s\n" %(range_key))
#        print("value[0] = %s\n" %(value[0]))
#        for range_val in range_values:
#            print("range_val = %s\n" %(range_val))        

        print(lidar_scan_range[range_key][0])

#        for data in lidar_data:
#            print(data)

        print("Drawing LiDAR Scan")


    def extract_lidar_file_data(self, filename):
        """
           LiDAR file has data consisting of key value pairs, some pairs are lists
           Extract the data into list data line by line
        """
        with open(filename, "r") as file:
           data = file.readlines()    

        return data

    def get_lidar_ranges(self, lidar_data):
        """
           From the lidar data, get the LiDAR ranges and split them into a key
           and a value consisting of a list of range points associated with that key
        """
        # Convert LiDAR ranges string data to key value list pair
        range_key_string, range_values_string = lidar_data[13].split(": ")
        # Convert string representation of list to list
        range_value_list = ast.literal_eval(range_values_string)
        return range_key_string, range_value_list

    def plot_lidar_scan(self, lidar_scan_range):
        """
           Draw a graph of the LiDAR scan using the points contained in the range list
        """


if __name__=="__main__":
    DrawLidarScan()

