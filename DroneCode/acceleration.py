"""
Created on: 07-08-2019
Author: R.A.C. (Raf)

"""
### Program to calculate the acceleration vector, given the 3D coordinates and time
# associated with each position.
# It considers the first data point with acceleration ZERO.
from tkinter import Tk                      # to get window and select file.
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

import sys                                  # to kill program when needed.
import os                                   # to run instruction in the bash.
import pandas                               # to manipulate csv files.
import math                                 # to use sin and cos
import numpy                                # to use numpyarrays

def acceleration(velocity_numpyarray):

    acc_vector=numpy.empty(shape=velocity_numpyarray.shape)

    acc_vector[:,0]=velocity_numpyarray[:,0]        # time is same.

    acc_vector[0,1:4]=0                     # First datapoint consider acceleration ZERO.

    for n in range(0,numpy.size(velocity_numpyarray,0)-1):   # number rows in array.

        acc_vector[n+1,1]=(velocity_numpyarray[n+1,1]-velocity_numpyarray[n,1])/(velocity_numpyarray[n+1,0]-velocity_numpyarray[n,0])     # X component of velocity
        acc_vector[n+1,2]=(velocity_numpyarray[n+1,2]-velocity_numpyarray[n,2])/(velocity_numpyarray[n+1,0]-velocity_numpyarray[n,0])     # Y component of velocity
        acc_vector[n+1,3]=(velocity_numpyarray[n+1,3]-velocity_numpyarray[n,3])/(velocity_numpyarray[n+1,0]-velocity_numpyarray[n,0])     # X component of velocity

    return(acc_vector)              # returns Numpy Array.

if __name__=='__main__':                    # For testing putposes.

    print("Select .CSV file to find acceleration. Make sure columns exist labeled: timestamp, vel_x, vel_y, vel_z")

    Tk().withdraw() # we don't want the full GUI, this keeps the root window
                        # from appearing.
    fileName=askopenfilename()

    extension=fileName[len(fileName)-3::]    # gets extension

    if extension=='csv' or extension!='CSV':
        pass
    else:
        print('Wrong extension of file, try again...')
        sys.exit()

    # read the csv file into variable DataFrame (This is for files processed with
    # our own software, labled "CLEAN"; If it is a random CSV file, won't read the right columns
    # or you labled them by hand 'Lat', 'Lon', 'Alt')
    colnames=['timestamp', 'vel_x', 'vel_y', 'vel_z']
    df=pandas.read_csv(fileName,usecols=colnames) # df is of the type DataFrame.

    velocity=df.to_numpy(copy=True)           # returns a ndarray (Numpy-array,
                                                # NOT a Numpy-matrix). Options for columns= list, optional.

    acc_vector=acceleration(velocity)       # returns a ndarray (Numpy-array)

    acceleration=pandas.DataFrame(acc_vector, columns=['timestamp','acc_x','acc_y','acc_z'])

    print('Select directory to store the acceleration CSV file')

    path=askdirectory()

    acceleration.to_csv(path+'/acceleration.csv',columns=['timestamp','acc_x','acc_y','acc_z'])
