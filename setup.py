# Filename: setup.py

# Standard libraries
import os
import sys

from setuptools import setup

dpath = os.path.dirname(__file__)
if dpath not in sys.path:
    sys.path.insert(0, dpath)

# NextTransit
from nexttransit import __version__

setup(
    name='nexttransit',
    version=__version__,
    description='Next Transit Estimated Departure Times',
    author='Alex Hartoto',
    author_email='ahartoto.dev@gmail.com',
    url='https://www.github.com/ahartoto/nexttransit',
    license='MIT',
    packages=['nexttransit'],
    install_requires=['requests>=2.13'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='transit requests html rest rest-api',
)
