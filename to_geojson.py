u'''
    Converts the given filename with associated XML and TIF files to a corresponding
        GeoJSON file.

    USAGE: 'python2 to_geojson.py -f [filename]'
    NOTE: Generates GeoJSON in the same directory as the original files.

    @author     Patrick Jahnig (psj516@vt.edu)
    @version    2018.05.01
'''

from __future__ import absolute_import
from sys import argv
import json

# http://lxml.de/
from lxml import etree

# http://www.gdal.org/index.html
from osgeo import gdal
from io import open

file_name = None

def appendFeature (geojson, rect):
    u'''
        Appends a feature representing the given bounding box to the given
        dictionary.

        @param  geojson - The dictionary to append the new feature to \n
        @param  rect    - The list representing the bounding box (as x1, y1, x2, y2)
    '''
    geojson [u"features"].append ({
        u"type": u"Feature",
        u"properties": {},
        u"geometry": {
            u"type": u"Polygon",
            u"coordinates": [ rect ]
        }
    })

def convertCoordinates (dataset, x, y):
    u'''
        Converts the given pixel coordinates to geographical coordinates using the given
        GDAL data set.

        @param  dataset - The GDAL data set to extract latitude / longitude from \n
        @param  x       - The x pixel coordinate \n
        @param  y       - The y pixel coordinate \n

        @return A tuple containing the pixel coordinates converted to geographical coordinates
    '''
    origin = getOrigin (dataset)
    pixel_size = getPixelSize (dataset)

    return x * pixel_size [0] + origin [0], y * pixel_size [1] + origin [1]

def generateArguments ():    
    u'''
        Parses the program arguments to determine what file should be converted.

        @throws EnvironmentError if the argument couldn't be found / parsed
    '''
    global argv, file_name
    args = {}

    while argv:
        if argv [0][0] == u"-":
            args [argv [0]] = argv [1]

        argv = argv [1:]

    if u"-f" in args:
        arg = args [u"-f"]
        n = arg.rfind (u".")

        file_name = arg [:n] if n >= 0 else arg

    else:
        raise EnvironmentError (u"Filename must be specified with -f")

def getCoordinates (dataset, bndbox):
    u'''
        Gets and converts the coordinates of the bounding box contained in the given tree
        element.

        @param  dataset     - The GDAL data set to extract latitude / longitude from \n
        @param  robndbox    - The XML tree element that contains the bounding box (robndbox tag)

        @return A list containing the converted coordinates of the bounding box
    '''
    xmin = float (bndbox [0].text)
    ymin = float (bndbox [1].text)
    xmax = float (bndbox [2].text)
    ymax = float (bndbox [3].text)

    return [convertCoordinates (dataset, xmin, ymin),
        convertCoordinates (dataset, xmin, ymax),
        convertCoordinates (dataset, xmax, ymax),
        convertCoordinates (dataset, xmax, ymin),
        convertCoordinates (dataset, xmin, ymin)]

def getOrigin (dataset):
    u'''
        Returns the origin of the given GDAL data set.

        @param  dataset - The GDAL data set to get the origin (geographical coordinates) of

        @return A tuple containing the x and y geographical coordinates of the origin
    '''
    geotransform = dataset.GetGeoTransform ()
    return geotransform [0], geotransform [3]

def getPixelSize (dataset):
    u'''
        Returns the pixel size of each pixel in the given GDAL data set.

        @param  dataset - The GDAL data set to get the pixel size of

        @return A tuple containing the x and y pixel sizes
    '''
    geotransform = dataset.GetGeoTransform ()
    return geotransform [1], geotransform [5]

def main ():
    generateArguments ()

    data = gdal.Open(file_name + u".tif", gdal.GA_ReadOnly)
    tree = etree.parse (file_name + u".xml")

    rects = []
    for i in tree.getiterator ():
        if i.tag == u"bndbox":
            rects.append (getCoordinates (data, i.getchildren ()))

    geojson = {
        u"type": u"FeatureCollection",
        u"name": file_name,
        u"features": []
    }

    for r in rects:
        appendFeature (geojson, r)

    file = open (file_name + u".geojson", u"w")
    file.write (json.dumps (geojson))

if __name__ == u"__main__":
    main ()
