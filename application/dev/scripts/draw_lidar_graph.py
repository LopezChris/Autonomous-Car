#!/usr/bin/env python
import ast
import matplotlib.pyplot as plt

class DrawLidarScan():
    def __init__(self):
        base_dir = "/home/self-driving-car/Autonomous-Car/application/data"
        sensor_dir = base_dir+"/lidar_scan/"

        # LiDAR attributes of the class
        self.filename = sensor_dir+"lidar-08-38-40.txt"
        # LiDAR data gathered from file stored into string lidar_data list
        self.lidar_data = self.extract_lidar_file_data()
        # LiDAR angle_min extracted from list and converted to float number
        self.angle_min = self.get_lidar_angle_min()
        # LiDAR angle_max extracted from list
        self.angle_max = self.get_lidar_angle_max()
        # LiDAR angle_increment extracted from list
        self.angle_increment = self.get_lidar_angle_increment()
        # LiDAR time_increment extracted from list
        self.time_increment = self.get_lidar_time_increment()
        # LiDAR scan_time extracted from list
        self.scan_time = self.get_lidar_scan_time()
        # LiDAR range_min extracted from list
        self.range_min = self.get_lidar_range_min()
        # LiDAR range_max extracted from list
        self.range_max = self.get_lidar_range_max()
        # LiDAR ranges[] extracted from list
        self.ranges = self.get_lidar_ranges()
        # Filter outliers from original LiDAR ranges[] list into new list
        filtered_ranges = self.preprocess_lidar_ranges()

        print("Drawing LiDAR Scan")

        self.show_lidar_scan_plot(filtered_ranges)

    def extract_lidar_file_data(self):
        """
           LiDAR file has data consisting of key value pairs, some pairs are lists
           Extract the data into list data line by line
        """
        with open(self.filename, "r") as file:
           data = file.readlines()    

        return data

    def get_lidar_angle_min(self):
        """
           Get the lidar angle_min, which is the start angle of the scan [rad]
        """
        angle_min_k, angle_min_v = self.lidar_data[6].split(": ")
        if angle_min_k == "angle_min":
            print("angle_min = %.14f [rad]" %(float(angle_min_v)))
            return float(angle_min_v)
        else:
            msg = "angle_min key not found"
            print(msg)
            return msg

    def get_lidar_angle_max(self):
        """
           Get the lidar angle_max, which is the end angle of the scan [rad]
        """
        angle_max_k, angle_max_v = self.lidar_data[7].split(": ")
        if angle_max_k == "angle_max":
            print("angle_max = %.14f [rad]" %(float(angle_max_v)))
            return float(angle_max_v)
        else:
            msg = "angle_max key not found"
            print(msg)
            return msg

    def get_lidar_angle_increment(self):
        """
           Get the lidar angle_increment, which the angular distance between measurements [rad]
        """
        angle_inc_k, angle_inc_v = self.lidar_data[8].split(": ")
        if angle_inc_k == "angle_increment":
            print("angle_increment = %.14f [rad]" %(float(angle_inc_v)))
            return float(angle_inc_v)
        else:
            msg = "angle_increment key not found"
            print(msg)
            return msg

    def get_lidar_time_increment(self):
        """
           Get the lidar time_increment, which the time between measurements [seconds]
        """
        time_inc_k, time_inc_v = self.lidar_data[9].split(": ")
        if time_inc_k == "time_increment":
            print("time_increment = %.14f [seconds]" %(float(time_inc_v)))
            return float(time_inc_v)
        else:
            msg = "time_increment key not found"
            print(msg)
            return msg
    
    def get_lidar_scan_time(self):
        """
           Get the lidar scan_time, which the time between scans [seconds]
        """
        scan_time_k, scan_time_v = self.lidar_data[10].split(": ")
        if scan_time_k == "scan_time":
            print("scan_time = %.14f [seconds]" %(float(scan_time_v)))
            return float(scan_time_v)
        else:
            msg = "scan_time key not found"
            print(msg)
            return msg

    def get_lidar_range_min(self):
        """
           Get the lidar range_min, which is the minimum range value [m]
        """
        range_min_k, range_min_v = self.lidar_data[11].split(": ")
        if range_min_k == "range_min":
            print("range_min = %.14f [m]" %(float(range_min_v)))
            return float(range_min_v)
        else:
            msg = "range_min key not found"
            print(msg)
            return msg

    def get_lidar_range_max(self):
        """
           Get the lidar range_max, which is the maximum range value [m]
        """
        range_max_k, range_max_v = self.lidar_data[12].split(": ")
        if range_max_k == "range_max":
            print("range_max = %.14f [m]" %(float(range_max_v)))
            return float(range_max_v)
        else:
            msg = "range_max key not found"
            print(msg)
            return msg

    def get_lidar_ranges(self):
        """
           Get the lidar ranges, which is the range data [m]
        """
        # Convert LiDAR ranges string data to key value list pair
        ranges_k, ranges_v = self.lidar_data[13].split(": ")

        if ranges_k == "ranges":
            # Convert string representation of list to list of string range elements
            ranges_list = ast.literal_eval(ranges_v)            
            print("num of elements in ranges_list = %i" %(len(ranges_list)))
            print("data type of ranges_list = %s" %(type(ranges_list)))
            print("ranges_list = %s" %(ranges_list))
            print("data type of ranges_list element[0] = %s" %(type(ranges_list[0])))
            return ranges_list
        else:
            msg = "ranges key not found"
            print(msg)
            return msg

    def preprocess_lidar_ranges(self):
        """
           Remove outliers from ranges[] list and save it as a new list 
           Outliers: values < range_min or values > range_max will be deleted
        """
        new_ranges_list = []
        for range_val in self.ranges:
            if range_val < self.range_min:
                # Do nothing
                print("T when %s < %s" %(range_val, self.range_min))
            elif range_val > self.range_max:
                # Do nothing
                print("T when %s > %s" %(range_val, self.range_max))
            else:
                # Not an outlier, so append range value to new list
                new_ranges_list.append(range_val)
        print("num of elements in lidar_filtered_ranges = %i" %(len(new_ranges_list)))
        print("lidar_filtered_ranges = %s" %(new_ranges_list))
        return new_ranges_list

    def show_lidar_scan_plot(self, lidar_scan_ranges):
        """
           Draw a graph of the LiDAR scan using the points contained in the ranges list
           Will utilize angle_increment on Z-axis within angle_min and angle_max boundary
           Will utilize ranges list on X-axis, so plot points on (X, Z) plane
        """
        # Set current start angle of scan to angle_inc scan
        angle_inc_scan = self.angle_min
        i = 0
        while i < len(lidar_scan_ranges):
            if angle_inc_scan >= self.angle_min and \
            angle_inc_scan < self.angle_max:
                # plot points (Z, X)
                plt.plot(angle_inc_scan, lidar_scan_ranges[i], 'ro')
                angle_inc_scan += self.angle_increment
            i += 1
        plt.xlabel('Angle Increment [rad]')
        plt.ylabel('Ranges [m]')
        plt.title('RC LiDAR Scan')
        plt.show()

if __name__=="__main__":
    DrawLidarScan()

