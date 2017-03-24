# Filename: station.py

"""
BART Station Module
"""

# Standard libraries
from xml.etree import ElementTree

# Requests
import requests

# NextTransit
from nexttransit import stop

# BART
from nexttransit.bart import config
from nexttransit.bart.error import BartQueryError


# Global
STATIONS = dict()


class Station(stop.TransitStop):
    """
    Represent a station
    """
    def __init__(self, name, uid=None, city=None, coordinate=None):
        super().__init__(name, uid=uid, city=city, coordinate=coordinate)

        url = config.URL['station_info'].format(station=uid,
                                                key=config.VALIDATION_KEY)
        response = requests.get(url)
        if response.status_code == config.GetResponseCodeEnum.SUCCESS.value:
            xml_str = response.content.decode()
            root = ElementTree.fromstring(xml_str)
            for node in root.iterfind('.//route'):
                if node.text is not None:
                    self.routes.add(node.text.strip())

    def __str__(self):
        """
        :return: string - name of the station with the abbreviation in
                          parenthesis
        """
        return "{} ({})".format(self.name, self.uid)


def register_all_stations():
    """
    Retrieve all stations that are currently registered with the agency.
    """
    global STATIONS
    if STATIONS:
        return

    url = config.URL['station'].format(key=config.VALIDATION_KEY)
    response = requests.get(url)

    if response.status_code != config.GetResponseCodeEnum.SUCCESS.value:
        raise BartQueryError()

    xml_str = response.content.decode()

    root = ElementTree.fromstring(xml_str)
    for station_node in root.iter('station'):
        uid = station_node.find('abbr').text.strip()
        name = station_node.find('name').text.strip()
        city = station_node.find('city').text.strip()
        station = Station(name, uid=uid, city=city)

        STATIONS[uid] = station


def get(uid):
    """
    Get the instance which has the provide abbreviated station name

    :param uid: string - abbreviated station name
    :return: instance of station.Station
    """
    register_all_stations()
    return STATIONS[uid]


def iter_station():
    """
    Iterate over all the registered stations

    :return: iterator for going though all the registered stations
    """
    register_all_stations()
    yield from STATIONS.values()
