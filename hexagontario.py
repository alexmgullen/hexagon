import json
import h3

from geojson import Feature, FeatureCollection, dumps

import sys

def hexagonize(file_name,resolution):
    file = open(file_name,'r')
    shape = json.load(file)
    file.close()

    geometry = shape['features'][0]['geometry']['coordinates']

    geo_array = []
    for geo in geometry:
        for line in geo:
            line[0], line[1] = line[1], line[0]
        geo_array.append(h3.LatLngPoly(geo))

    #TODO: rename this [à la uber](https://github.com/uber/h3-py/blob/master/src/h3/_h3shape.py):to support multiple ll3 objects
    cells = h3.polygon_to_cells(geo_array[0],resolution)

    features = []

    for cell in cells:
        coordinates = h3.cell_to_boundary(cell)

        shape = []
        for point in coordinates:
            latitude = point[0]
            longitude = point[1]
            shape.append((longitude,latitude))

        features.append(Feature(geometry={ "type" : "Polygon", "coordinates": [shape]},id=cell,properties={"cell_id":cell}))

    return FeatureCollection(features,crs={ "type" : "name", "properties" : { "name": "epsg:4326"} })

if __name__ == "__main__":

    resolution = 5

    try:
        arg_input = int(sys.argv[1])
        if arg_input < 0:
            print("Value too small, please try a value of 0 or greater")
            print("More details: https://h3geo.org/docs/core-library/restable/")
        elif arg_input > 15:
            print("Value too large, please try a value of 15 or greater")
            print("More details: https://h3geo.org/docs/core-library/restable/")
        else:
            resolution = arg_input
    except:
        print("Could not convert value to a numeric, defaulting to 5")

    province = hexagonize("raw/Province.geojson",resolution)

    output = open(f"output/province.{resolution}.geojson",'w')
    output.write(dumps(province))
    output.close()