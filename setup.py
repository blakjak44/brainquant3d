# Set this to True to enable building extensions using Cython.
# Set it to False to build extensions from the C file (that was previously created using Cython).
# Set it to 'auto' to build with Cython if available, otherwise
# from the C file.

import os
import sys
import numpy
import pip
import pkgutil
import shutil
import tarfile
import urllib.request as request

from pathlib import Path
from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install as _install
from distutils.core import setup
from distutils.extension import Extension

from brainquant3d._version import __version__

if sys.platform not in ['linux', 'darwin']:
    raise EnvironmentError(f'Platform {sys.platform} not supported.')

if sys.platform == 'linux':
    opencv_libs = '.lib-linux'
elif sys.platform == 'darwin':
    opencv_libs = '.lib-osx'

USE_CYTHON = 'auto'

if USE_CYTHON:
    try:
        from Cython.Distutils import build_ext
        from Cython.Build import cythonize
    except ImportError:
        if USE_CYTHON == 'auto':
            USE_CYTHON = False
        else:
            raise

cmdclass = {}
ext_modules = []

if USE_CYTHON:
    ext_modules += cythonize([
        Extension("brainquant3d.analysis._voxelization",
                  sources=["brainquant3d/analysis/_voxelization.pyx"],
                  include_dirs=[numpy.get_include()]
                  ),
        Extension("brainquant3d.image_filters.filters._background_subtraction",
                  sources=["brainquant3d/image_filters/filters/_background_subtraction.pyx"]
                  ),
        Extension("brainquant3d.image_filters.filters.helpers.array_manipulations",
                  sources=["brainquant3d/image_filters/filters/helpers/array_manipulations.pyx"]
                  ),
        Extension("brainquant3d.image_filters.filters.label._connect",
                  sources=["brainquant3d/image_filters/filters/label/_connect.pyx"],
                  language="c++",
                  include_dirs=[numpy.get_include(), "include"],
                  extra_link_args=[os.path.join(f'brainquant3d/{opencv_libs}', f) for f in os.listdir(
                      f'brainquant3d/{opencv_libs}')],
                  runtime_library_dirs=[f'$ORIGIN/../../../{opencv_libs}']
                  ),
        Extension("brainquant3d.image_filters.filters.label._threshold",
                  sources=["brainquant3d/image_filters/filters/label/_threshold.pyx"],
                  include_dirs=[numpy.get_include()],
                  language="c++"
                  ),
        Extension("brainquant3d.image_filters.filters.label._filter",
                  sources=["brainquant3d/image_filters/filters/label/_filter.pyx"],
                  include_dirs=[numpy.get_include()],
                  language="c++"
                  ),
        Extension("brainquant3d.image_filters.filters.label._overlap",
                  sources=["brainquant3d/image_filters/filters/label/_overlap.pyx"],
                  include_dirs=[numpy.get_include()],
                  language="c++"
                  ),
        Extension("brainquant3d.image_filters.filters.label.watershed._watershed",
                  sources=["brainquant3d/image_filters/filters/label/watershed/_watershed.pyx"],
                  include_dirs=[numpy.get_include()],
                  language="c++"
                  ),
        Extension("brainquant3d.image_filters.filters.label.util._nonzero_coords",
                  sources=["brainquant3d/image_filters/filters/label/util/_nonzero_coords.pyx"],
                  include_dirs=[numpy.get_include()],
                  language='c++'
                  )
    ])
    cmdclass['build_ext'] = build_ext
else:
    ext_modules += [
        Extension("brainquant3d.analysis._voxelization",
                  sources=["brainquant3d/analysis/_voxelization.c"],
                  include_dirs=[numpy.get_include()]
                  ),
        Extension("brainquant3d.image_filters.filters._background_subtraction",
                  sources=["brainquant3d/image_filters/filters/_background_subtraction.c"]
                  ),
        Extension("brainquant3d.image_filters.filters.helpers.array_manipulations",
                  sources=["brainquant3d/image_filters/filters/helpers/array_manipulations.c"]
                  ),
        Extension("brainquant3d.image_filters.filters.label._connect",
                  sources=["brainquant3d/image_filters/filters/label/_connect.cpp"],
                  language="c++",
                  include_dirs=[numpy.get_include(), "include"],
                  extra_link_args=[os.path.join(f'brainquant3d/{opencv_libs}', f) for f in os.listdir(
                      f'brainquant3d/{opencv_libs}')],
                  runtime_library_dirs=[f'$ORIGIN/../../../{opencv_libs}']
                  ),
        Extension("brainquant3d.image_filters.filters.label._threshold",
                  sources=["brainquant3d/image_filters/filters/label/_threshold.cpp"],
                  include_dirs=[numpy.get_include()],
                  language="c++"
                  ),
        Extension("brainquant3d.image_filters.filters.label._filter",
                  sources=["brainquant3d/image_filters/filters/label/_filter.cpp"],
                  include_dirs=[numpy.get_include()],
                  language="c++"
                  ),
        Extension("brainquant3d.image_filters.filters.label._overlap",
                  sources=["brainquant3d/image_filters/filters/label/_overlap.cpp"],
                  include_dirs=[numpy.get_include()],
                  language="c++"
                  ),
        Extension("brainquant3d.image_filters.filters.label.watershed._watershed",
                  sources=["brainquant3d/image_filters/filters/label/watershed/_watershed.cpp"],
                  include_dirs=[numpy.get_include()],
                  language="c++"
                  ),
        Extension("brainquant3d.image_filters.filters.label.util._nonzero_coords",
                  sources=["brainquant3d/image_filters/filters/label/util/_nonzero_coords.cpp"],
                  include_dirs=[numpy.get_include()],
                  language='c++'
                  )
    ]


class install(_install):
    def run(self):

        #  download external programs required by package to install directory.
        dest = Path(os.getcwd()) / 'brainquant3d/.external'

        print('installing elastik')
        url = 'https://github.com/SuperElastix/elastix/releases/download/5.0.0/elastix-5.0.0-linux.tar.bz2'
        tmp = Path(url).name
        sink = dest / 'elastix-5.0.0-linux'
        with request.urlopen(url) as response, open(tmp, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            tar = tarfile.open(tmp, "r:bz2")
            tar.extractall(sink)
            tar.close()

        print('installing ilastik')
        url = 'https://files.ilastik.org/ilastik-1.3.3-Linux.tar.bz2'
        tmp = Path(url).name

        sink = dest
        with request.urlopen(url) as response, open(tmp, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            tar = tarfile.open(tmp, "r:bz2")
            tar.extractall(sink)
            tar.close()

        _install.run(self)

        # install antspy
        if sys.platform == 'linux':
            pip.main(['install', "https://github.com/ANTsX/ANTsPy/releases/download/v0.1.4/antspy-0.1.4-cp36-cp36m-linux_x86_64.whl"])
        if sys.platform == 'darwin':
            pip.main(['install', "https://github.com/ANTsX/ANTsPy/releases/download/Weekly/antspy-0.1.4-cp36-cp36m-macosx_10_7_x86_64.whl"])


cmdclass['install'] = install

setup(
    name=               'brainquant3d',
    version=            __version__,
    description=        'Tools for tera-voxel image analysis.',
    author=             'Ricardo Azevedo, Jack Zeitoun',
    author_email=       'ricardo-re-azevedo@gmail.com, jack.zeitoun@outlook.com',
    maintainer=         'Ricardo Azevedo',
    maintainer_email=   'ricardo-re-azevedo@gmail.com',
    url=                'https://github.com/sunilgandhilab/brainquant3d',
    license=            'BY-NC-SA 4.0',
    cmdclass=           cmdclass,
    packages=           find_packages(),
    install_requires=[
        'numpy',
        'pyyaml',
        'scipy',
        'opencv-python',
        'tifffile',
        'scikit-image',
        'pandas',
        'h5py',
        'vtk',
        'anytree',
        'webcolors',  # required for antspy
        'plotly'  # required for antspy
    ],
    include_package_data=True,
    ext_modules=ext_modules,
    keywords='tera voxel teravoxel image analysis biology'
)
