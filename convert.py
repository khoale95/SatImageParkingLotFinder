u'''
    Converts any TIF files found in the directory and subdirectories that this script is executed
        in.

    USAGE: 'python2 convert.py -t [jpeg | png] [-f filename]'
    NOTE: Generates files of the given format in the same directory as the original file.

    @authors    Patrick Jahnig (psj516@vt.edu), Thomas Wolfe (twolfe99@vt.edu)
    @version    2018.05.01
'''

from __future__ import absolute_import
import os

GDAL_COMMAND    = u"gdal_translate -scale_1 20 1463 -scale_2 114 1808 -scale_3 139 1256 -ot Byte -of"
file_type       = None
file_name       = None

file_types = ["jpeg", "png"]

def convertTifTo (file_type, file_name):
    u'''
        Converts the given TIF file to the given file format.

        @param  file_type   - The file format to convert to \n
        @param  file_name   - The TIF file to convert
    '''
    type_str = file_type.__str__ ()
    conv_str = file_name.replace (u"tif", type_str)

    os.system (GDAL_COMMAND + u" " + type_str.upper () + u" " + file_name + u" " + conv_str)
    os.system (u"rm " + conv_str + u".aux.xml")

def generateArguments ():
    u'''
        Parses the arguments passed to the script, and sets fields appropriately.

        @throws EnvironmentError if an argument couldn't be understood (i.e. file format was not understood).
    '''

    from sys import argv
    
    args = {}
    global file_name, file_type

    while argv:
        if argv [0][0] == u"-":
            args [argv [0]] = argv [1]

        argv = argv [1:]

    if u"-t" in args:
        arg = args [u"-t"]

        for t in file_types:
            if arg in t:
                file_type = t
                break

        if file_type is None:
            raise EnvironmentError (u"Conversion file format was not recognized; Use: " + File_Type.list ())
    
    else:
        raise EnvironmentError (u"A file format to convert to must be specified: -t " + File_Type.list ())

    if u"-f" in args:
        file_name = args [u"-f"]

def walkThrough (root = None):
    u'''
        Walks through the given directory and subdirectories, and converts any TIF files found to
        the file format given as an argument to the script.

        @param  root - The directory to begin the conversion at
    '''

    if root is None:
        root = u"."

    for dirpath, dirnames, filenames in os.walk (root):
        for file in filenames:
            if file.endswith (u".tif"):
                convertTifTo (file_type, os.path.join (dirpath, file))

def main ():
    generateArguments ()

    if file_name is None:
        walkThrough ()

    else:
        convertTifTo (file_type, file_name)

if __name__ == u"__main__":
    main ()
