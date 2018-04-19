'''
    Converts the given filename with associated XML and TIF files to a corresponding
        GeoJSON file.

    USAGE: 'python3 to_geojson.py -f [filename]'
    NOTE: Generates GeoJSON in the same directory as the original files.

    @author     Patrick Jahnig (psj516@vt.edu)
    @version    2018.04.18
'''

from sys import argv
import json

# http://lxml.de/
from lxml import etree

# http://www.gdal.org/index.html
from osgeo import gdal

file_name = None

def appendFeature (geojson: dict, rect: list) -> None:
    '''
        Appends a feature representing the given bounding box to the given
        dictionary.

        @param  geojson - The dictionary to append the new feature to \n
        @param  rect    - The list representing the bounding box (as x1, y1, x2, y2)
    '''
    geojson ["features"].append ({
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [ rect ]
        }
    })

def convertCoordinates (dataset : gdal.Dataset, x: float, y: float) -> [float, float]:
    '''
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

def generateArguments () -> None:    
    '''
        Parses the program arguments to determine what file should be converted.

        @throws EnvironmentError if the argument couldn't be found / parsed
    '''
    global argv, file_name
    args = {}

    while argv:
        if argv [0][0] == "-":
            args [argv [0]] = argv [1]

        argv = argv [1:]

    if "-f" in args:
        arg = args ["-f"]
        n = arg.rfind (".")

        file_name = arg [:n] if n >= 0 else arg

    else:
        raise EnvironmentError ("Filename must be specified with -f")

def getCoordinates (dataset: gdal.Dataset, bndbox: etree.Element) -> list:
    '''
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
        convertCoordinates (dataset, xmax, ymin),
        convertCoordinates (dataset, xmax, ymax),
        convertCoordinates (dataset, xmin, ymax)]

def getOrigin (dataset: gdal.Dataset) -> [float, float]:
    '''
        Returns the origin of the given GDAL data set.

        @param  dataset - The GDAL data set to get the origin (geographical coordinates) of

        @return A tuple containing the x and y geographical coordinates of the origin
    '''
    geotransform = dataset.GetGeoTransform ()
    return geotransform [0], geotransform [3]

def getPixelSize (dataset: gdal.Dataset) -> [float, float]:
    '''
        Returns the pixel size of each pixel in the given GDAL data set.

        @param  dataset - The GDAL data set to get the pixel size of

        @return A tuple containing the x and y pixel sizes
    '''
    geotransform = dataset.GetGeoTransform ()
    return geotransform [1], geotransform [5]

def main () -> None:
    generateArguments ()

    data = gdal.Open(file_name + ".tif", gdal.GA_ReadOnly)
    tree = etree.parse (file_name + ".xml")

    rects = []
    for i in tree.getiterator ():
        if i.tag == "bndbox":
            rects.append (getCoordinates (data, i.getchildren ()))

    geojson = {
        "type": "FeatureCollection",
        "name": file_name,
        "features": []
    }

    for r in rects:
        appendFeature (geojson, r)

    file = open (file_name + ".geojson", "w")
    file.write (json.dumps (geojson))

if __name__ == "__main__":
    main ()
