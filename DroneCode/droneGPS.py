"""
Created on: 06-26-2019
Author: R.A.C. (Raf)

"""

# This code asks for name of file. Detects the two possible extensions we
# know how to conver: .bin and .ulg, and returns the name file and the
# extension.
# tkinter must be installed.

from tkinter import Tk                      # to get window and select file.
from tkinter.filedialog import askopenfilename

import sys                                  # to kill program when needed.

import os                                   # to run instruction in the bash.

import pandas                               # to manipulate csv files.


####### Function that gets the file name you want to trasnform. #######
def getFileName():
    yN=input("Do you want to convert your log drone file to CSV format? (y/n)")

    if yN=='y' or yN=='Y':
        Tk().withdraw() # we don't want the full GUI, this keeps the root window
                        # from appearing.
        fileName=askopenfilename()
        extension=fileName[len(fileName)-3::]    # gets extension bin or ulg
        print(fileName)
        print(extension)
        return[fileName, extension]             # Function returns both name
    else:                                       #and extension
        print("Bye, bye my little birdy...")
        sys.exit()

#######Function that transforms .BIN or .ulg files into CSV file. Doesn't matter
# which extension you throw at it, it's process both. #######
def convertToCSV(fileName01, extension01):
    print(fileName01)
    if extension01=='ulg':
        myCmd='ulog2csv --messages vehicle_gps_position '+fileName01
        os.system(myCmd)
# ulog2csv stores output file in same directory as original file.
    elif extension01=='bin' or extension01=='BIN':
        startName=False             # true when you reach beginning of file name.
        n=0                         # counter that goes backwards in file name.
        beacon='n'                  # stores each letter until reach /
        shortName=""                # stores just name of file without path
        while (startName==False):   # chops path keeps name of file alone.
            if beacon!='/':
                beacon=fileName01[(len(fileName01)-1)-n]
                shortName=beacon+shortName
                n+=1
            else:
                startName=True
# I force mavlogdump to store output file into same folder as original file,
# with same name but extension .csv
        myCmd='mavlogdump.py --format csv --types GPS '+fileName01+'>'+fileName01[:len(fileName01)-4]+'.csv'
        os.system(myCmd)
    else:
        print("File with wrong extension, run program again :-)")
        sys.exit()
# ulog2csv and mavlogdump are python script text executables, so I just return
# them form the bash using os.system()function.


#### Function that produces a clean CSV file with time stamp, lat, long, alt.##
def cleanCSV(fileName02, extension02):

    clean=input('Do you want to produce a clean CSV file? (y/n)')
    if clean=='y' or clean=='Y':
        if extension02=='ulg':

            csvName=fileName02[:len(fileName02)-4]+'_vehicle_gps_position_0'+'.csv'
            colnames=['timestamp','lat','lon','alt']
            print(csvName)

        elif extension02=='bin' or extension02=='BIN':

            csvName=fileName02[:len(fileName02)-4]+'.csv'
            colnames=['timestamp','Lat','Lng','Alt']
            print(csvName)

        else:
            print('Error procesing .csv file. File removed or modified !!!')
            sys.exit()

        df=pandas.read_csv(csvName,usecols=colnames) # df is of the type DataFrame.

    # Using the same colnames, we can produce another .csv file with only the
    # columns we want, and both types labled Lat, Lon, Alt:
        cleanCSVName=csvName[:len(csvName)-4]+'_CLEAN.csv'
        df.to_csv(cleanCSVName, columns=colnames, header=['timestamp','Lat','Lon','Alt'])

    else:
        print("Hold on, there's more...")

###### Function to transform GPS coordinates from lat, long, alt to x,y,z #####
def gpsCoorTrans(fileName03, extension03):

    tranform=input('Do you want to transform GPS coordiates? (y/n)')
    if tranform=='y' or tranform=='Y':
        if extension03=='ulg':

            csvName=fileName03[:len(fileName03)-4]+'_vehicle_gps_position_0'+'.csv'
            colnames=['timestamp','lat','lon','alt']
            print(csvName)

        elif extension03=='bin' or extension03=='BIN':

            csvName=fileName03[:len(fileName03)-4]+'.csv'
            colnames=['timestamp','Lat','Lng','Alt']
            print(csvName)

        else:
            print('Error procesing .csv file. File removed or modified !!!')
            sys.exit()
# read the csv file into variable DataFrame
        df=pandas.read_csv(csvName,usecols=colnames) # df is of the type DataFrame.
# create new variable that is an array:
        gpsLatLonAlt=df.to_numpy(copy=True)      # returns a ndarray (Numpy-array, NOT a Numpy-matrix). Options for columns= list, optional.

        gpsLatLonAlt.astype(float)

#### Point that links witht the function CoordTrans, that does the transformatoin
# reading from a CSV file. Here we already have the CSV raw file. CoordTrans
# function reads the clean CSV file, but the user might chose not to produce it.

        print(gpsLatLonAlt)
# Use that array to manipulate the coordinates:

        print("gps ndim: ", gpsLatLonAlt.ndim)
        print("gps shape:", gpsLatLonAlt.shape)
        print("gps size: ", gpsLatLonAlt.size)
        print("dtype:", gpsLatLonAlt.dtype)
        print("First data point is:")
        print(gpsLatLonAlt[0,0],gpsLatLonAlt[0,1],gpsLatLonAlt[0,2],gpsLatLonAlt[0,3])






    else:
        print("Bye, bye my little birdy...")
        sys.exit()



if __name__=="__main__":
        fullName=getFileName()
        convertToCSV(fullName[0],fullName[1])
        cleanCSV(fullName[0],fullName[1])
        gpsCoorTrans(fullName[0],fullName[1])





# if __name__=="__main__":
#    import sys
#    getFileName(int(sys.argv[1]))


# From the Python documentaion, adding __name__=="__main__": makes the file
# usable as a script as well as in importable module
