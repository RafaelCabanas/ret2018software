"""
Created on: 06-26-2019
Author: R.A.C. (Raf)

"""

import pandas                               # to manipulate csv files.
import sys                                  # to kill program when needed.

#### Function that produces a clean CSV file with time stamp, lat, long, alt.##

def clean_CSV(full_name, old_extension):    # extension .bin or .ulg of original drone file.

    if old_extension=='ulg':

        csvName=full_name[:len(full_name)-4]+'_vehicle_gps_position_0'+'.csv'
        colnames=['timestamp','lat','lon','alt']
        print(csvName)

    elif old_extension=='bin' or old_extension=='BIN':

        csvName=full_name[:len(full_name)-4]+'.csv'
        colnames=['timestamp','Lat','Lng','Alt']
        print(csvName)

    else:
        print('Error procesing .csv file. File removed or modified !!!')
        sys.exit()

    df=pandas.read_csv(csvName,usecols=colnames) # df is of the type DataFrame.

    if old_extension=='ulg':        # ulg gives 1/10 of mirodegrees. We need degrees
        df.lat=df.lat*(1e-7)
        df.lon=df.lon*(1e-7)
        df.alt=df.alt*(1e-3)

    # Using the same colnames, we can produce another .csv file with only the
    # columns we want, and both types labled Lat, Lon, Alt:
    cleanCSVName=csvName[:len(csvName)-4]+'_CLEAN.csv'

    # Change column name also on the DataFrame, so it matches the CSV file, and both csv files, from BIN or ulog can be processed at once later.
    df.rename({"lat": "Lat","lon": "Lon","alt": "Alt"}, axis=1, inplace=True) # for ulg files
    df.rename({'Lng': 'Lon'}, axis=1, inplace=True) # for BIN files. If a column is not present, it doesn't throw an exemption. That's characteristic of rename method.

    return(df, cleanCSVName)

def clean_CSV_throttle(full_name, old_extension):

    if old_extension=='bin' or old_extension=='BIN':

        csvName=full_name[:len(full_name)-4]+'_Throttle'+'.csv'
        colnames=['timestamp','ThI','ThO','ThH','Alt']
        print(csvName)

    else:
        print('Error procesing .csv file. File removed or modified !!!')
        sys.exit()

    df_throttle=pandas.read_csv(csvName,usecols=colnames) # df is of the type DataFrame.

    return(df_throttle)


if __name__=="__main__":

    clean=input('Do you want to produce a clean CSV file? (y/n)')

    if clean=='y' or clean=='Y':
        name=input('Full name of file:')
        ext=input('extension:')

        gps_dataframe, cleanCSVName=clean_CSV(name, ext)

        colnames=['timestamp','Lat','Lon','Alt']
        gps_dataframe.to_csv(cleanCSVName, columns=colnames, header=['timestamp','Lat','Lon','Alt'])

    else:
        print("Bye, bye my little birdy...")
        sys.exit()

    print(gps_dataframe)
