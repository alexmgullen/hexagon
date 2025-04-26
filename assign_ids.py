import h3
import pandas

import sys
import math

input_file = "raw/36f92c5b-0c8b-4a4b-b4c5-d15a43894297.csv"
output_file = "output/36f92c5b-0c8b-4a4b-b4c5-d15a43894297.assign_ids.csv"

resolution=4

def apply_latlng_id(x):
    result = None
    try:
        lat = float(x[20])
        lon = float(x[21])

        if math.isnan(lat) or math.isnan(lon):
            raise TypeError("Invalid Latitude or Longitude coordinates.")

        result = h3.latlng_to_cell(lat,lon,resolution)
    
    except Exception as e:
        print(e)
    
    return result
    

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

    dataframe = pandas.read_csv(input_file)

    dataframe["hex_id"] = dataframe.apply(apply_latlng_id,axis=1)

    dataframe.to_csv(output_file,index=False)

