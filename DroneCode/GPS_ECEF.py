from tkinter import Tk                      # to get window and select file.
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

import sys                                  # to kill program when needed.

import pandas                               # to manipulate csv files.

import math                                 # to use sin and cos

import numpy                                # to use numpyarrays



def GPS_to_ECEF_custom(DataFrame_input):
    # DataFrame has the columns timestamp Lat, Lon, Alt from our previous processing program clean_CSV
    gpsLatLonAlt=DataFrame_input.to_numpy(copy=True)          # returns a ndarray (Numpy-array, NOT a Numpy-matrix). Options for columns= list, optional.


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

    return(GPSxyz,gpsLatLonAlt[0,1],gpsLatLonAlt[0,2])

    # Returns GPS coordinates in the ECEF ref system numpyarray, the FIRST Point
    # of the file latitude and longitude. This point will be the ORIGIN of the
    # ENU reference system in the TLP.

if __name__=="__main__":
    print("Select .CSV file to convert. Make sure latitude, longitude and altitude columns are labled Lat, Lon, Alt")

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
    colnamesNew=['timestamp','Lat','Lon','Alt']
    df=pandas.read_csv(fileName,usecols=colnamesNew) # df is of the type DataFrame.

    GPSxyz, Lat0, Lon0 =GPS_to_ECEF_custom(df)

    ECEFcoordinates=pandas.DataFrame(GPSxyz, columns=['timestamp','X','Y','Z'])

    print('Select directory to store the ECEF coordinates CSV file')

    path=askdirectory()

    ECEFcoordinates.to_csv(path+'/ECEF_Coordinates_custom.csv',columns=['timestamp','X','Y','Z'])

    print(ECEFcoordinates)
    print(Lat0)
    print(Lon0)
