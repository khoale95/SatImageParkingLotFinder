from lxml import etree
from osgeo import gdal
import json

file_name = None

def appendFeature (geojson, rect):
    geojson ["features"].append ({
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [ rect ]
        }
    })

def convertCoordinate (dataset, x, y):
    origin = getOrigin (dataset)
    pixel_size = getPixelSize (dataset)

    return x * pixel_size [0] + origin [0], y * pixel_size [1] + origin [1]

def generateArguments () -> None:
    from sys import argv
    
    global file_name
    args = {}

    while argv:
        if argv [0][0] == "-":
            args [argv [0]] = argv [1]

        argv = argv [1:]

    if "-f" in args:
        arg = args ["-f"]
        n = arg.rfind (".")

        file_name = arg [:n] if n >= 0 else arg

def getCoordinates (dataset, robndbox):
    cx = float (robndbox [0].text)
    cy = float (robndbox [1].text)
    w = float (robndbox [2].text)
    h = float (robndbox [3].text)

    return [convertCoordinate (data, cx - w / 2, cy - h / 2),
        convertCoordinate (data, cx + w / 2, cy - h / 2),
        convertCoordinate (data, cx + w / 2, cy + h / 2),
        convertCoordinate (data, cx - w / 2, cy + h / 2)]

def getOrigin (dataset):
    geotransform = data.GetGeoTransform ()
    return geotransform [0], geotransform [3]

def getPixelSize (dataset):
    geotransform = data.GetGeoTransform ()
    return geotransform [1], geotransform [5]

generateArguments ()

data = gdal.Open(file_name + ".tif", gdal.GA_ReadOnly)
tree = etree.parse (file_name + ".xml")
rects = []
for i in tree.getiterator():
    tag = i.tag
    if tag == "robndbox":
        rects.append (getCoordinates (data, i.getchildren()))

geojson = {
    "type": "FeatureCollection",
    "name": file_name,
    "features": []
}

for r in rects:
    appendFeature (geojson, r)

file = open (file_name + ".geojson", "w")
file.write (json.dumps (geojson))
