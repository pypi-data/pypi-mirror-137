#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2021 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Creates an hexagonal ASCII raster [0] from a CSV file with a set of point samples.
# Values in the new raster are interpolated using the multiquadratic method.
# It assumes the CSV file to be organised into three columns, with xx, yy 
# coordinates and values in succession, as:
# XX;YY;Values;    
# xx1;yy1;value1;
# xx2;yy2;value2;
# Always skips the first row, assuming it is the header.
# 
# Usage example:
# csv2hasc -x 0 -y 0 -X 10 -Y 10 -s 0.62 -i input.csv -o output.hasc
#
# [0] https://github.com/ldesousa/HexAsciiBNF
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 06-12-2016 

import argparse 
from hex_utils.hasc import HASC
from hex_utils.parserExtent import addExtentArguments
from hex_utils.csv2interpol import readCSV, interpol

def getArguments():

    parser = argparse.ArgumentParser(description=
        '''Creates an HASC raster from a CSV file with a set of point samples.
           Values in the new raster are interpolated using the multiquadratic method.
           It assumes the CSV file has a headers and is organised into three columns, 
           with xx, yy coordinates and values in succession, as:
           xx1;yy1;value1;
           xx2;yy2;value2;''')
    parser = addExtentArguments(parser)
    parser.add_argument("-s", "--side", dest="side", default = 0.62, # area ~ 1
                      type=float, help="hexagon cell side length" )
    parser.add_argument("-i", "--input", dest="input", required = True,
                      help="input CSV file" )
    parser.add_argument("-o", "--output", dest="output", default = "output.hasc",
                      help="output HASC file" )
    return parser.parse_args()


# ----- Main ----- #
def main():
    
    args = getArguments()

    coords, values = readCSV(args.input)

    hexRaster = HASC()
    hexRaster.initWithExtent(args.side, args.xmin, args.ymin, args.xmax, args.ymax)
    
    print("Geometries:" + 
          "\n Hexagon cell area         : " + str(hexRaster.cellArea())  +
          "\n Hexagon side length       : " + str(hexRaster.side)  +
          "\n Hexagon perpendicular     : " + str(hexRaster.hexPerp)  +
          "\n Number of rows in mesh    : " + str(hexRaster.nrows)  +
          "\n Number of columns in mesh : " + str(hexRaster.ncols))

    hexRaster = interpol(hexRaster, coords, values)
    hexRaster.save(args.output)        
    #hexRaster.saveAsGeoJSON(args.output + ".json") 
    hexRaster.saveAsGML(args.output + ".gml")
            
    print("\nSuccessfully created new HexASCII raster.")        
            
if __name__ == "__main__":
        main()            
