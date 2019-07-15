"""
Created on: 07-08-2019
Author: R.A.C. (Raf)

"""
### Program to calculate the velocity vector, given the 3D coordinates and time
# associated with each position.
# It considers the first data point with velocity ZERO.
from tkinter import Tk                      # to get window and select file.
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

import sys                                  # to kill program when needed.
import os                                   # to run instruction in the bash.
import pandas                               # to manipulate csv files.
import math                                 # to use sin and cos
import numpy                                # to use numpyarrays

def velocity(position_numpyarray):

    vel_vector=numpy.empty(shape=position_numpyarray.shape)

    vel_vector[:,0]=position_numpyarray[:,0]        # time is same.

    vel_vector[0,1:4]=0                     # First datapoint consider velocity ZERO.

    for n in range(0,numpy.size(position_numpyarray,0)-1):   # number rows in array.

        vel_vector[n+1,1]=(position_numpyarray[n+1,1]-position_numpyarray[n,1])/(position_numpyarray[n+1,0]-position_numpyarray[n,0])     # X component of velocity
        vel_vector[n+1,2]=(position_numpyarray[n+1,2]-position_numpyarray[n,2])/(position_numpyarray[n+1,0]-position_numpyarray[n,0])     # Y component of velocity
        vel_vector[n+1,3]=(position_numpyarray[n+1,3]-position_numpyarray[n,3])/(position_numpyarray[n+1,0]-position_numpyarray[n,0])     # X component of velocity

    return(vel_vector)              # returns Numpy Array.

if __name__=='__main__':                    # For testing putposes.

    print("Select .CSV file to find velocity. Make sure columns exist labeled: timestamp, x_local-E, y_local-N, z_local-U")

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
    colnames=['timestamp', 'x_local-E', 'y_local-N', 'z_local-U']
    df=pandas.read_csv(fileName,usecols=colnames) # df is of the type DataFrame.

    position=df.to_numpy(copy=True)           # returns a ndarray (Numpy-array,
                                                # NOT a Numpy-matrix). Options for columns= list, optional.

    vel_vector=velocity(position)       # returns a ndarray (Numpy-array)

    velocity=pandas.DataFrame(vel_vector, columns=['timestamp','vel_x','vel_y','vel_z'])

    print('Select directory to store the velocity CSV file')

    path=askdirectory()

    velocity.to_csv(path+'/velocity.csv',columns=['timestamp','vel_x','vel_y','vel_z'])
