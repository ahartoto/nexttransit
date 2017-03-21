# Filename: config.py

"""
BART Configuration
"""
# Standard libraries
import os

from enum import Enum


VALIDATION_KEY = os.getenv('BART_VALIDATION_KEY', None)
if VALIDATION_KEY is None:
    raise ImportError("cannot find the value of $BART_VALIDATION_KEY")

URL = {
    'etd': 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={station}&key={key}',
    'etd_dir': 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={station}&'
               'key={key}&dir={direction}',
    'route_info': 'http://api.bart.gov/api/route.aspx?cmd=routeinfo&'
                  'route={number}&key={key}',
    'routes': 'http://api.bart.gov/api/route.aspx?cmd=routes&'
              'key={key}',
    'station': 'http://api.bart.gov/api/stn.aspx?cmd=stns&key={key}',
    'station_info': 'http://api.bart.gov/api/stn.aspx?cmd=stninfo&'
                    'orig={station}&key={key}',
}


class GetResponseCodeEnum(Enum):
    SUCCESS = 200
