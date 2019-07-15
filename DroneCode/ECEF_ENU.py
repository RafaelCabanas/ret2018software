from tkinter import Tk                      # to get window and select file.
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

import sys                                  # to kill program when needed.

import os                                   # to run instruction in the bash.

import pandas                               # to manipulate csv files.

import math                                 # to use sin and cos

import numpy                                # to use numpyarrays


def ECEF_to_ENU_custom(gpsCoorECEFAsNumpayArray,latRef,lonRef):

    relativeECEF=numpy.empty(shape=gpsCoorECEFAsNumpayArray.shape)
#    latRef=lat0
#    lonRef=lon0
# Use reference point of TLP (Tangent Local Plane) for ENU (East, North, UP)
# reference system at the FIRST point of the file. We can change this to be
# maybe a point at a later time, or after some time has past, or even ask the
# user to introduce the reference lat, lon they might want.
    relativeECEF=gpsCoorECEFAsNumpayArray
    relativeECEF[:,:]=relativeECEF[:,:]-relativeECEF[0,:]

# Coordinate sytem transformation from ECEF to ENU TLP:
    coorENU_rel=numpy.empty(shape=gpsCoorECEFAsNumpayArray.shape)
    coorENU_rel[:,0]=relativeECEF[:,0]       # Relative timestamp is the same time.

    for n in range(numpy.size(relativeECEF,0)):
        coorENU_rel[n,1]=(-math.sin(lonRef)*relativeECEF[n,1])+(math.cos(lonRef)*relativeECEF[n,2])
        coorENU_rel[n,2]=(-math.sin(latRef)*math.cos(lonRef)*relativeECEF[n,1])-(math.sin(latRef)*math.sin(lonRef)*relativeECEF[n,2])+(math.cos(latRef)*relativeECEF[n,3])
        coorENU_rel[n,3]=(math.cos(latRef)*math.cos(lonRef)*relativeECEF[n,1])+(math.cos(latRef)*math.sin(lonRef)*relativeECEF[n,2])+(math.sin(latRef)*relativeECEF[n,3])

    return(coorENU_rel)
# Function returns the ENU coordinates, in the tangent local plane (TLP), relative to the FIRST datapoint in your file, as a numpyArray.

if __name__=="__main__":

    print("Select .CSV file to convert. Make sure ECEF columns are labled timestamp, X, Y, Z")

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
    colnames=['timestamp','X','Y','Z']
    df=pandas.read_csv(fileName,usecols=colnames) # df is of the type DataFrame.


    ECEF_coord=df.to_numpy(copy=True)           # returns a ndarray (Numpy-array,
                                                # NOT a Numpy-matrix). Options for columns= list, optional.
    lat0=float(input('Provide epoch latitude for this calculation (reference TLP)'))
    lon0=float(input('Provide epoch longitude for this calculation (reference TLP)'))
    # for testing purposes, you provide the first point latitude and longitude.
    # When linked to the procesing of a drone file, the previous function
    # gpslatlonalt to ECEF will provide the lat and lon of the first point in the file, or reference point for your TLP.

    enu=ECEF_to_ENU_custom(ECEF_coord,lat0,lon0)       # returns a ndarray (Numpy-array)

    ENUcoordinates=pandas.DataFrame(enu, columns=['timestamp','x_local-E','y_local-N','z_local-U'])

    print('Select directory to store the ENU coordinates CSV file')

    path=askdirectory()

    ENUcoordinates.to_csv(path+'/ENU_Coordinates.csv',columns=['timestamp','x_local-E','y_local-N','z_local-U'])
