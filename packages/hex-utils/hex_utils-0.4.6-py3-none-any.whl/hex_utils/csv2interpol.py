#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2021 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Encapsulates interpolation tasks for CSV tools.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 14-06-2021

import csv
import numpy
import warnings
from scipy import spatial
from scipy import interpolate


def readCSV(inputFile):

    coords_list = []
    values_list = []

    try:
        with open(inputFile, 'rt') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            # Skip header
            next(spamreader, None)

            for row in spamreader:
                if (len(row) > 0):
                    raw = str(row[0]).split(',')
                    coords_list.append([float(raw[0]), float(raw[1])])
                    values_list.append(float(raw[2]))

    except Exception as ex:
        print("Failed to read input file:\n" + str(ex))
        exit()
    
    return numpy.array(coords_list),numpy.array(values_list)


def interpol(raster, coords, values):

    neighbours = 5
    tolerance = 0.1
    epsilon = 100

    tree = spatial.KDTree(coords)

    # Set maximum and minimum admissable values
    max_value = values.max() + (values.max() - values.min()) * tolerance
    min_value = values.min() - (values.max() - values.min()) * tolerance

    # Supress warnings from numpy
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', r'scipy.linalg.solve')

        for j in range(raster.nrows):
          for i in range(raster.ncols):

              xx = []
              yy = []
              vals = []
              x, y = raster.getCellCentroidCoords(i, j)
              d, ind = tree.query(numpy.array([x, y]),neighbours)

              for n in range(neighbours):
                  xx.append(tree.data[ind[n]][0])
                  yy.append(tree.data[ind[n]][1])
                  vals.append(values[ind[n]])

              try:
                  f = interpolate.Rbf(xx, yy, vals, epsilon=epsilon)
                  new_value = f(x,y)
              except (Exception) as ex:
                  new_value = sum(vals) / len(vals)
              else:
                  if new_value < min_value:
                      raster.set(i, j, min_value)
                  elif new_value > max_value:
                      raster.set(i, j, max_value)
                  else:
                      raster.set(i, j, new_value)

    return raster



