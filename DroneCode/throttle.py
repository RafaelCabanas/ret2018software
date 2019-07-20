"""
Created on: 07-08-2019
Author: R.A.C. (Raf)

"""
### Program to completely transform coordinates from GPS latitude, longitude, height
# over the WGS84 ellipsoid, to East, North, Up (ENU), using two transformations,
# first to ECEF (Earth Centered Earth Fix) coordinates, and later to ENU.
# Saves each step into a CSV file and plots the ENU trajectory.

from tkinter import Tk                      # to get window and select file.
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

import sys                                  # to kill program when needed.
import os                                   # to run instruction in the bash.
import pandas                               # to manipulate csv files.
import math                                 # to use sin and cos
import numpy                                # to use numpyarrays

import matplotlib as mpl                    # to plot data.
from mpl_toolkits.mplot3d import Axes3D
mpl.use("TKAgg")         ### Uncomment this line to use framework TKAgg
import matplotlib.pyplot as plt

from get_file_name import get_file_name
from convert_CSV import convert_CSV_throttle
from clean_CSV import clean_CSV_throttle
from plot_kinematic import plot_throttle

if __name__ == '__main__':

    print('Do you want to get the throttle from your log drone file?')
    print('This option gets the throttle from your log drone file .BIN to .CSV, produces a clean CSV and plots the three different types of throttle')
    yN_file=input("(y/n)")

    file_name=get_file_name(yN_file)
    convert_CSV_throttle(file_name[0],file_name[1])  # full name of file = file_name[0]
                                            # extension = file_name[1]

    throttle_dataframe=clean_CSV_throttle(file_name[0],file_name[1])  # returns a DataFrame with columns ['timestamp','Lat','Lon','Alt']

    plot_throttle(throttle_dataframe)

    
