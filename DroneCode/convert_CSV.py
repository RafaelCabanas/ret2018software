"""
Created on: 06-26-2019
Author: R.A.C. (Raf)

"""

import os                                   # to run instruction in the bash.
import sys                                  # to kill program when needed.

#######Function that transforms .BIN or .ulg files into CSV file. Doesn't matter
# which extension you throw at it, it's process both. #######

def convert_CSV(full_name, extension):

    if extension=='ulg':
        myCmd='ulog2csv --messages vehicle_gps_position '+full_name
        os.system(myCmd)
# ulog2csv stores output file in same directory as original file.
    elif extension=='bin' or extension=='BIN':
# I force mavlogdump to store output file into same folder as original file,
# with same name but extension .csv
        myCmd='mavlogdump.py --format csv --types GPS '+full_name+'>'+full_name[:len(full_name)-4]+'.csv'
        os.system(myCmd)
    else:
        print("File with wrong extension, run program again :-)")
        sys.exit()

def convert_CSV_throttle(full_name, extension):

    if extension=='bin' or extension=='BIN':
# I force mavlogdump to store output file into same folder as original file,
# with same name but extension .csv
        myCmd='mavlogdump.py --format csv --types CTUN '+full_name+'>'+full_name[:len(full_name)-4]+'_Throttle'+'.csv'
        os.system(myCmd)
    else:
        print("File with wrong extension, run program again :-)")
        sys.exit()

# ulog2csv and mavlogdump are python script text executables, so I just return
# them form the bash using os.system()function.

if __name__=="__main__":
    name=input('Full name of file:')
    ext=input('extension:')
    convert_CSV(name,ext)
