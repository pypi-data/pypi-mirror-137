#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2021 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Creates an ESRI ASCII raster [0] from a CSV file with a set of point samples.
# Values in the new raster are interpolated using the multiquadratic method.
# It assumes the CSV file to be organised into three columns, with xx, yy 
# coordinates and values in succession, as:
# XX,YY,Values,     
# xx1,yy1,value1,
# xx2,yy2,value2,
# The programmes assumes a header to be present.
# 
# Usage example:
# csv2asc -x 0 -y 0 -X 10 -Y 10 -s 1 -i input.csv -o output.asc
#
# [0] https://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/esri-ascii-raster-format.htm
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 10-06-2021 

import argparse 
from hex_utils.asc import ASC
from hex_utils.parserExtent import addExtentArguments
from hex_utils.csv2interpol import readCSV, interpol

def getArguments():

    parser = argparse.ArgumentParser(description=
        '''Creates an ESRI ASCII raster from a CSV file with a set of point samples.
           Values in the new raster are interpolated using the multiquadratic method.
           It assumes the CSV file a headers and is organised into three columns, 
           with xx, yy coordinates and values in succession, as:
           xx1;yy1;value1;
           xx2;yy2;value2;''')
    parser = addExtentArguments(parser)
    parser.add_argument("-s", "--side", dest="side", default = 1,
                      type=float, help="square cell side length" )
    parser.add_argument("-i", "--input", dest="input", required = True,
                      help="input CSV file" )
    parser.add_argument("-o", "--output", dest="output", default = "output.hasc",
                      help="output ESRI ASCII file" )
    return parser.parse_args()

# ----- Main ----- #
def main():

    args = getArguments()

    coords, values = readCSV(args.input)

    raster = ASC()
    raster.initWithExtent(args.side, args.xmin, args.ymin, args.xmax, args.ymax)

    print("Geometries:" +
          "\n Square cell area         : " + str(raster.size * raster.size)  +
          "\n Square side length       : " + str(raster.size)  +
          "\n Number of rows in mesh    : " + str(raster.nrows)  +
          "\n Number of columns in mesh : " + str(raster.ncols))

    raster = interpol(raster, coords, values)
    raster.save(args.output)

    print("\nSuccessfully created new ESRI ASCII raster.")

if __name__ == "__main__":
        main()
