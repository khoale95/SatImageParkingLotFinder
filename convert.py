'''
    Converts any TIF files found in the directory and subdirectories that this script is executed
        in.

    NOTE: Generates files of the given format in the same directory as the original file.

    @authors    Patrick Jahnig (psj516@vt.edu), Thomas Wolfe (twolfe99@vt.edu)
    @version    2018.04.05
'''

import os
from enum import Enum

class File_Type (Enum):
    '''
        Represents the supported file types that can be converted to from TIF files.
    '''

    JPEG = 1, "jpeg"
    PNG = 2, "png"

    @classmethod
    def list (cls) -> str:
        '''
            Returns a String that represents each possible conversion type.

            @param  cls - The class instance of File_Type \n
            @return The String of each conversion option
        '''
        enum_list = "["

        for e in cls:
            enum_list += e.__str__ () + " | "

        if enum_list.__len__ () > 1:
            enum_list = enum_list [:-3]

        enum_list += "]"

        return enum_list

    def __str__ (self) -> str:
        return self.value [1]

GDAL_COMMAND    = "gdal_translate -scale_1 20 1463 -scale_2 114 1808 -scale_3 139 1256 -ot Byte -of"
file_type       = None

def convertTifTo (file_type: File_Type, file_name: str) -> None:
    type_str = file_type.__str__ ()
    conv_str = file_name.replace ("tif", type_str)

    os.system (GDAL_COMMAND + " " + type_str.upper () + " " + file_name + " " + conv_str)
    os.system ("rm " + conv_str + ".aux.xml")

def generateArguments () -> None:
    '''
        Parses the arguments passed to the script, and sets fields appropriately.

        @throws EnvironmentError if an argument couldn't be understood (i.e. file format was not understood).
    '''

    from sys import argv
    
    args = {}
    global file_type

    while argv:
        if argv [0][0] == "-":
            args [argv [0]] = argv [1]

        argv = argv [1:]

    if "-f" in args:
        arg = args ["-f"]

        for t in File_Type:
            if arg in t.__str__ ():
                file_type = t
                break

        if file_type is None:
            raise EnvironmentError ("Conversion file format was not recognized; Use: " + File_Type.list ())
    
    else:
        raise EnvironmentError ("A file format to convert to must be specified: -f " + File_Type.list ())

def walkThrough (root: str = None) -> None:
    '''
        Walks through the given directory and subdirectories, and converts any TIF files found to
        the file format given as an argument to the script.

        @param  root - The directory to begin the conversion at
    '''

    if root is None:
        root = "."

    for dirpath, dirnames, filenames in os.walk (root):
        for file in filenames:
            if file.endswith (".tif"):
                convertTifTo (file_type, os.path.join (dirpath, file))

generateArguments ()
walkThrough ()
