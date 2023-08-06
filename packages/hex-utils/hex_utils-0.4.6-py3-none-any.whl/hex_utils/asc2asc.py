#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2022 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Transforms a rectangular ESRI ASCII grid into a different resolution. 
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 10-10-2021 
#
# [0] https://github.com/ldesousa/HexAsciiBNF

import sys
import math
import argparse 
from enum import Enum  
from hex_utils.asc import ASC

class Method(Enum):
    MULTIQUADRATIC = 'mq',
    NEAREST_NEIGHBOUR = 'nn' 


def setArguments():
    
    parser = argparse.ArgumentParser(description='Converts an ESRI ASCII grid into another of different resolution.')
    parser.add_argument("-s", "--size", dest="size", default = 1,
                      type=float, help="cell size of the output grid" )
    parser.add_argument("-m", "--method", default="mq",
                      help = "Interpolation mehonthod: mq - Multiquadratic, nn - Nearest Neighbour")
    parser.add_argument("-i", "--input", dest="inputFile", required = True,
                      help="input ESRI ASCII raster file" )
    parser.add_argument("-o", "--output", dest="outputFile", default = "out.asc",
                      help="output ESRI ASCII raster file" )
    
    return parser.parse_args()


# ------------ Main ------------ #
def main():
    
    args = setArguments()
    
    inGrid = ASC()
    try:
        inGrid.loadFromFile(args.inputFile)
    except (ValueError, IOError) as ex:
        print("Error loading the raster %s: %s" % (args.inputFile, ex))
        sys.exit()
    
    # Compute output grid extent
    xSpan = inGrid.size * inGrid.ncols
    ySpan = inGrid.size * inGrid.nrows
    
    outNcols = (xSpan // args.size)
    outNrows = (ySpan // args.size) 

    if ((xSpan % args.size) > 0):
        outNcols = outNcols + 1
    if ((ySpan % args.size) > 0):
        outNrows= outNrows + 1

    outGrid = ASC()
    outGrid.init(int(outNcols), int(outNrows), inGrid.xll, inGrid.yll, 
                 args.size, inGrid.nodata)
    
    print("Geometries:" + 
          "\n Input square cell size    : " + str(inGrid.size) + 
          "\n Output square cell size   : " + str(outGrid.size)  +
          "\n Number of rows in mesh    : " + str(outGrid.nrows)  +
          "\n Number of columns in mesh : " + str(outGrid.ncols))
    
    if(args.method == Method.MULTIQUADRATIC.value[0]):
        interpol = inGrid.interpolMultiquadratic
        print("\nConverting with Multi-quadratic interpolation ...")
    else:
        interpol = inGrid.getNearestNeighbour
        print("\nConverting with Nearest Neighbour interpolation ...")
    
    for j in range(outGrid.nrows):
        for i in range(outGrid.ncols):
            x, y = outGrid.getCellCentroidCoords(i, j)
            outGrid.set(i, j, interpol(x, y))

    try:
        outGrid.save(args.outputFile)
    except (ValueError, IOError) as ex:
        print ("Error saving output file %s: %s" % (args.outputFile, ex))
            
    print ("Finished successfully.")
    
if __name__ == "__main__":
    main()    
