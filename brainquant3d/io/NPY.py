# -*- coding: utf-8 -*-
"""
Interface to write binary files for point like data

The interface is based on the numpy library.

Example:
    >>> import os, numpy
    >>> import bq3d.Settings as settings
    >>> import bq3d.IO.NPY as npy
    >>> filename = os.path.join(bq3d.config.brainquant3dPath, 'Test/Data/NPY/points.npy')
    >>> points = npy.readPoints(filename)
    >>> print points.shape
    (5, 3)

"""
#:copyright: Copyright 2015 by Christoph Kirst, The Rockefeller University, New York City
#:license: GNU, see LICENSE.txt for details.
#TODO: merge readPoints and readData into one function

import os
import shutil
import numpy as np

from bq3d import io
import imp

import logging
log = logging.getLogger(__name__)

def writePoints(filename, data, returnMemmap = False, **args):
    np.save(filename, data)
    if returnMemmap:
        data = np.load(filename, mmap_mode='r+')
        return data
    else:
        return filename


def readPoints(filename, **args):
    data = np.load(filename, mmap_mode='r+')
    return io.pointsToRange(data, **args)

def writeData(filename, data, returnMemmap = False, **args):

    np.save(filename, data)
    if returnMemmap:
        data = np.load(filename, mmap_mode='r+')
        return data
    else:
        return filename


def readData(filename, **args):
    data = np.load(filename, mmap_mode='r+')
    return io.pointsToRange(data, **args)
