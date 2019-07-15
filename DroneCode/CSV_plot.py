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
from convert_CSV import convert_CSV
from clean_CSV import clean_CSV
from GPS_ECEF import GPS_to_ECEF_custom
from ECEF_ENU import ECEF_to_ENU_custom
from velocity import velocity
from acceleration import acceleration
from plot_kinematic import plot_trajectory3D
from plot_kinematic import plot_trajectory3D_ENU
from plot_kinematic_vel import plot_velocity3D_vector
from plot_kinematic_vel import plot_velocity3D_vector_ENU
from plot_kinematic_acc import plot_acceleration3D_vector
from plot_kinematic_acc import plot_acceleration3D_vector_ENU

if __name__ == '__main__':

    Tk().withdraw() # we don't want the full GUI, this kees the root window
                    # from appearing.
    full_Name=askopenfilename()

    extension=full_Name[len(full_Name)-3::]    # gets extension

    if extension=='csv' or extension!='CSV':
        pass
    else:
        print('Wrong extension of file, try again...')
        sys.exit()

# read the csv file into variable DataFrame (This is for files processed with
# our own software, labled "CLEAN"; If it is a random CSV file, won't read the right columns
# or you labled them by hand 'Lat', 'Lon', 'Alt')
    colnamesNew=['timestamp','Lat','Lon','Alt']
    gps_dataframe=pandas.read_csv(full_Name,usecols=colnamesNew) # gps_dataframe is of the type DataFrame.
                                                                # returns a DataFrame with columns ['timestamp','Lat','Lon','Alt']

    GPSxyz, Lat0, Lon0 =GPS_to_ECEF_custom(gps_dataframe) # returns a ndarray (Numpy-array), 2 real numbers.

    enu=ECEF_to_ENU_custom(GPSxyz,Lat0,Lon0)            # returns a Numpy-array

    vel_vector=numpy.empty(shape=(0,0))                 # Make arrays zero size initially, if the user doesn't
    acc_vector=numpy.empty(shape=(0,0))                 # want to save velocity or acceleration, the conditions can be checked.

    yN_velocity=input('Do you want to calculate the velocity of the drone? (y/n)')

    if yN_velocity == 'y' or yN_velocity =='Y':

        vel_vector=velocity(enu)       # returns a ndarray (Numpy-array)

    yN_acceleration=input('Do you want to calculate the acceleration of the drone? (y/n)')

    if yN_acceleration == 'y' or yN_acceleration =='Y':

        if numpy.size(vel_vector)!=0:

            acc_vector=acceleration(vel_vector)
        else:
            vel_vector=velocity(enu)
            acc_vector=acceleration(vel_vector)

    yN_saveData=input('Do you want to save the coordinate changes into a .CSV file? (y/n)')

    if yN_saveData == 'y' or yN_saveData =='Y':

        ECEFcoordinates=pandas.DataFrame(GPSxyz, columns=['timestamp','X','Y','Z'])
#       ECEFcoordinates.drop(['timestamp'], axis=1, inplace=True)

        ENUcoordinates=pandas.DataFrame(enu, columns=['timestamp','x_local-E','y_local-N','z_local-U'])
        ENUcoordinates.drop(columns=['timestamp'], inplace=True)    # Comment if you don't want to see the relative time.

        gps_dataframe.rename(columns={'timestamp':'timestamp_POSIX'}, inplace=True)

        if numpy.size(acc_vector)!=0:

            velocity=pandas.DataFrame(vel_vector, columns=['timestamp','vel_x','vel_y','vel_z'])
            velocity.drop(columns=['timestamp'], inplace=True)       # Not repeat time.

            acceleration=pandas.DataFrame(acc_vector, columns=['timestamp','acc_x','acc_y','acc_z'])
            acceleration.drop(columns=['timestamp'], inplace=True)       # Not repeat time.

            all_coordinates=pandas.concat([gps_dataframe, ECEFcoordinates, ENUcoordinates, velocity, acceleration], axis=1)

        elif numpy.size(vel_vector)!=0:

            velocity=pandas.DataFrame(vel_vector, columns=['timestamp','vel_x','vel_y','vel_z'])
            velocity.drop(columns=['timestamp'], inplace=True)       # Not repeat time.

            all_coordinates=pandas.concat([gps_dataframe, ECEFcoordinates, ENUcoordinates, velocity], axis=1)

        else:

            all_coordinates=pandas.concat([gps_dataframe, ECEFcoordinates, ENUcoordinates], axis=1)

        print('Select directory to store the ENU coordinates CSV file')
        path=askdirectory()+'/'

        if numpy.size(acc_vector)!=0:
            all_coordinates.to_csv(path+'GPS_ECEF_ENU_Coord_vel_acc.csv',columns=['timestamp_POSIX','timestamp','Lat','Lon','Alt','X','Y','Z','x_local-E','y_local-N','z_local-U','vel_x','vel_y','vel_z','acc_x','acc_y','acc_z'])

            # Only want to preserve columns 'timestamp','x_local-E','y_local-N','z_local-U','vel_x','vel_y','vel_z','acc_x','acc_y','acc_z'
            df_to_Plot=all_coordinates.drop(columns=['timestamp_POSIX','Lat','Lon','Alt','X','Y','Z'])

            data_array_to_Plot=df_to_Plot.to_numpy()

            plot_acceleration3D_vector_ENU(data_array_to_Plot)

        elif numpy.size(vel_vector)!=0:
            all_coordinates.to_csv(path+'GPS_ECEF_ENU_Coord_vel.csv',columns=['timestamp_POSIX','timestamp','Lat','Lon','Alt','X','Y','Z','x_local-E','y_local-N','z_local-U','vel_x','vel_y','vel_z'])

            # Only want to preserve columns 'timestamp','x_local-E','y_local-N','z_local-U','vel_x','vel_y','vel_z'
            df_to_Plot=all_coordinates.drop(columns=['timestamp_POSIX','Lat','Lon','Alt','X','Y','Z'])

            data_array_to_Plot=df_to_Plot.to_numpy()

            plot_velocity3D_vector_ENU(data_array_to_Plot)

        else:
            all_coordinates.to_csv(path+'GPS_ECEF_ENU_Coordinates.csv',columns=['timestamp_POSIX','timestamp','Lat','Lon','Alt','X','Y','Z','x_local-E','y_local-N','z_local-U'])

            plot_trajectory3D_ENU(enu)
