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


####### Function that gets the file name you want to trasnform. #######
def get_file_name(string_yN):

    if string_yN=='y' or string_yN=='Y':
        Tk().withdraw() # we don't want the full GUI, this kees the root window
                        # from appearing.
        full_name=askopenfilename()
        extension=full_name[len(full_name)-3::]    # gets extension bin or ulg

        startName=False             # true when you reach beginning of file name.
        n=0                         # counter that goes backwards in file name.
        beacon=full_name[len(full_name)-1] # stores each letter until reach /, starting with last letter of the file+extension.
        short_name=""                # stores just name of file without path
        while (startName==False):   # chops path keeps name of file alone.

            if beacon!='/':
                n+=1
                short_name=beacon+short_name
            else:
                startName=True

            beacon=full_name[len(full_name)-1-n]

        path=full_name[:len(full_name)-n:]
# One can use tkinter method from tkinter.filedialog askdirectory, and returns the directory. I just didn't know when I programmed this.
    else:
        print("Bye, bye my little birdy...")
        sys.exit()


    return[full_name, extension, short_name, path]          # Function returns full name, extension of file, just name of file and path.

if __name__=="__main__":

    yN=input("Do you want to convert your log drone file to CSV format? (y/n)")

    file_name=get_file_name(yN)
    print('full name of file is: ' + file_name[0])
    print('extension: ' + file_name[1])
    print('name of file is: ' + file_name[2])
    print('folder of file is: ' + file_name[3])
