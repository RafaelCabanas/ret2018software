from tkinter import Tk                      # to get window and select file.
from tkinter.filedialog import askopenfilename

import sys                                  # to kill program when needed.

import os                                   # to run instruction in the bash.

import pandas                               # to manipulate csv files.

import math                                 # to use sin and cos

import numpy                                # to use numpyarrays

import pyproj                               # library that does coordinate
                                            # transformations.

import matplotlib as mpl                    # to plot data.
from mpl_toolkits.mplot3d import Axes3D
mpl.use("TKAgg")         ### Uncomment this line to use framework TKAgg
# That will be a temporary solution. Trying the files before:
# Use it becuase the python is using the wrong frameowrk and gives an error.
# Creating the following .matplotlib/matplotlibrc file seem to solve the problem:
# Downloaded a sample file that only contains uncommented the following line:
#               backend : TKAgg
# The file is in the folder ~/.matplotlib and it has extension .dms
# That doesn't solve the problem.
# I added the same file to the anaconda matplotlib folder.
# /anaconda3/lib/python3.6/site-packages/matplotlib/
# Didn't work either... so I just have to add that line with TKAgg framework...
# Solution maybe here: https://www.codesofinterest.com/2018/05/fixing-matplotlib-pyplot-import-errors.html

import matplotlib.pyplot as plt



####### Function that gets the file name you want to trasnform. #######
# and make a GPS coordinates (Lat, Long, Alt) change to ECEF coordinate
# system.

def GPS_to_ECEF_pyproj_fromFile():
    print("Select .CSV file to convert. Make sure latitude, longitude and altitude columns are labled Lat, Lon, Alt")

    Tk().withdraw() # we don't want the full GUI, this keeps the root window
                        # from appearing.
    fileName=askopenfilename()
    extension=fileName[len(fileName)-3::]    # gets extension
    print(fileName)
    print(extension)

    if extension=='csv' or extension!='CSV':
        pass
    else:
        print('Wrong extension of file, try again...')
        sys.exit()

# read the csv file into variable DataFrame (This is for files processed with
# our own software, labled "CLEAN" If it is a random CSV file, won't read the right columns
# or you labled them by hand 'Lat', 'Lon', 'Alt')
    colnamesNew=['timestamp','Lat','Lon','Alt']
    df=pandas.read_csv(fileName,usecols=colnamesNew) # df is of the type DataFrame.
# create new variable that is an array:
    gpsLatLonAlt=df.to_numpy(copy=True)      # returns a ndarray (Numpy-array, NOT a Numpy-matrix). Options for columns= list, optional.

    print(gpsLatLonAlt)

#### Point that links witht the main program, that does the transformatoin
# reading from a CSV file. Here we already have the CSV raw file. CoordTrans
# function reads the clean CSV file, but the user might chose not to produce it.

######## Coordinate transformation ########

    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

    GPSxyz=numpy.empty(shape=gpsLatLonAlt.shape)

    GPSxyz[:,0]=gpsLatLonAlt[:,0]       # timestamp is the same time.

    for i in range(gpsLatLonAlt.shape[0]):

        GPSxyz[i,1],GPSxyz[i,2],GPSxyz[i,3]= pyproj.transform(lla, ecef, gpsLatLonAlt[i,2], gpsLatLonAlt[i,1], gpsLatLonAlt[i,3], radians=False)

    print(GPSxyz)

    ECEFcoordinates=pandas.DataFrame(GPSxyz, columns=['timestamp','x','y','z'])
    print(ECEFcoordinates)
    ECEFcoordinates.to_csv('ECEF_Coordinates_pyProj.csv',columns=['timestamp','x','y','z'])


####### Function that gets the file name you want to trasnform. #######
# and make a GPS coordinates (Lat, Long, Alt) change to ECEF coordinate
# system, using a raw coordinate transformation. Custom made.

def GPS_to_ECEF_custom_fromFile():
    print("Select .CSV file to convert. Make sure latitude, longitude and altitude columns are labled Lat, Lon, Alt")

    Tk().withdraw() # we don't want the full GUI, this keeps the root window
                        # from appearing.
    fileName=askopenfilename()
    extension=fileName[len(fileName)-3::]    # gets extension
    print(fileName)
    print(extension)

    if extension=='csv' or extension!='CSV':
        pass
    else:
        print('Wrong extension of file, try again...')
        sys.exit()

# read the csv file into variable DataFrame (This is for files processed with
# our own software, labled "CLEAN" If it is a random CSV file, won't read the right columns
# or you labled them by hand 'Lat', 'Lon', 'Alt')
    colnamesNew=['timestamp','Lat','Lon','Alt']
    df=pandas.read_csv(fileName,usecols=colnamesNew) # df is of the type DataFrame.
# create new variable that is an array:
    gpsLatLonAlt=df.to_numpy(copy=True)          # returns a ndarray (Numpy-array, NOT a Numpy-matrix). Options for columns= list, optional.

#    print(gpsLatLonAlt)

#### Point that links witht the main program, that does the transformatoin
# reading from a CSV file. Here we already have the CSV raw file. CoordTrans
# function reads the clean CSV file, but the user might chose not to produce it.

######## Coordinate transformation ########
    GPSxyz=numpy.empty(shape=gpsLatLonAlt.shape)

    GPSxyz[:,0]=gpsLatLonAlt[:,0]       # timestamp is the same time.

# write latitude and longitude in radians:

    gpsLatLonAlt[:,1]=gpsLatLonAlt[:,1]*math.pi/180
    gpsLatLonAlt[:,2]=gpsLatLonAlt[:,2]*math.pi/180

# Define variables, like axis ellipsoid and excentriciy

    a=6378137.0                     # Semi-major axis of ellipsoid of Earth.
                                    # WGS84 Datum. In meters.
    inv_f=298.257223563             # Inverse Flattening of ellipsoid of Earth.
# https://confluence.qps.nl/qinsy/en/world-geodetic-system-1984-wgs84-29855173.html#WorldGeodeticSystem1984(WGS84)-WGS84,ITRFandGDA94

    f=1/inv_f
    e2=1-(1-f)*(1-f)      # Eccentricity square; e^2= 2f-f^2

# Creates a numpy array of 1 column and length same as gps matrix rows
    N_lat=numpy.empty((numpy.size(gpsLatLonAlt,0),1))


    for n in range(numpy.size(gpsLatLonAlt,0)):
        N_lat[n,0]=a/math.sqrt(1-e2*math.sin(gpsLatLonAlt[n,1])*math.sin(gpsLatLonAlt[n,1]))

        GPSxyz[n,1] = (N_lat[n,0]+gpsLatLonAlt[n,3])*math.cos(gpsLatLonAlt[n,1])*math.cos(gpsLatLonAlt[n,2])
        GPSxyz[n,2] = (N_lat[n,0]+gpsLatLonAlt[n,3])*math.cos(gpsLatLonAlt[n,1])*math.sin(gpsLatLonAlt[n,2])
        GPSxyz[n,3] = (N_lat[n,0]*(1-e2)+gpsLatLonAlt[n,3])*math.sin(gpsLatLonAlt[n,1])

#    print(N_lat)

    ECEFcoordinates=pandas.DataFrame(GPSxyz, columns=['timestamp','x','y','z'])
#    print(ECEFcoordinates)
    ECEFcoordinates.to_csv('ECEF_Coordinates_custom.csv',columns=['timestamp','x','y','z'])

    return(GPSxyz,gpsLatLonAlt[0,1],gpsLatLonAlt[0,2])

'''
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(GPSxyz[:,1], GPSxyz[:,2], GPSxyz[:,3], label='parametric curve')
    ax.legend()

    plt.show()
'''

# Returns GPS coordinates in the ECEF ref system numpyarray, the FIRST Point
# of the file latitude and longitude. This point will be the ORIGIN of the
# ENU reference system in the TLP.


##### function that transforms ECEF coordinate into ENU coordinate, given an
# origin for the reference system.

def ECEF_to_ENU(gpsCoorECEFAsNumpayArray,lat3,lon3):

    relativeECEF=numpy.empty(shape=gpsCoorECEFAsNumpayArray.shape)
    latRef=lat3
    lonRef=lon3
# Use reference point of TLP (Tangent Local Plane) for ENU (East, North, UP)
# reference system at the FIRST point of the file. We can change this to be
# maybe a point at a later time, or after some time has past, or even ask the
# user to introduce the reference lat, lon they might want.
    relativeECEF=gpsCoorECEFAsNumpayArray
    relativeECEF[:,:]=relativeECEF[:,:]-relativeECEF[0,:]

# Coordinate sytem transformation from ECEF to ENU TLP:
    coorENU_rel=numpy.empty(shape=gpsCoorECEFAsNumpayArray.shape)
    coorENU_rel[:,0]=relativeECEF[:,0]       # Relative timestamp is the same time.

    print(coorENU_rel)

    for n in range(numpy.size(relativeECEF,0)):
        coorENU_rel[n,1]=(-math.sin(lonRef)*relativeECEF[n,1])+(math.cos(lonRef)*relativeECEF[n,2])
        coorENU_rel[n,2]=(-math.sin(latRef)*math.cos(lonRef)*relativeECEF[n,1])-(math.sin(latRef)*math.sin(lonRef)*relativeECEF[n,2])+(math.cos(latRef)*relativeECEF[n,3])
        coorENU_rel[n,3]=(math.cos(latRef)*math.cos(lonRef)*relativeECEF[n,1])+(math.cos(latRef)*math.sin(lonRef)*relativeECEF[n,2])+(math.sin(latRef)*relativeECEF[n,3])

    print(coorENU_rel)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(coorENU_rel[:,1], coorENU_rel[:,2], coorENU_rel[:,3], label='parametric curve')
    ax.legend()

    plt.show()

if __name__=="__main__":

    coorECEF=GPS_to_ECEF_custom_fromFile()
    ECEF_to_ENU(coorECEF[0],coorECEF[1],coorECEF[2])
#   GPS_to_ECEF_pyproj_fromFile()
