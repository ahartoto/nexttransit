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
            self.north_routes = set()
            self.south_routes = set()

            self.north_platforms = set()
            self.south_platforms = set()

            xml_str = response.content.decode()
            root = ElementTree.fromstring(xml_str)
            for node in root.iterfind('.//north_routes/route'):
                if node.text is not None:
                    self.north_routes.add(node.text.strip())

            for node in root.iterfind('.//south_routes/route'):
                if node.text is not None:
                    self.south_routes.add(node.text.strip())

            for node in root.iterfind('.//north_platforms/platform'):
                if node.text is not None:
                    self.north_platforms.add(node.text.strip())

            for node in root.iterfind('.//south_platforms/platform'):
                if node.text is not None:
                    self.south_platforms.add(node.text.strip())

    def platform(self, dest):
        """
        The platform number to be at to board from current station
        to get to the destination station.

        :param dest:
        :return: string
        """
        pass

    def __str__(self):
        """

        :return:
        """
        msg = [
            "{} is part of the following routes:".format(self.name),
        ] + [
            "  {}: {}".format(route_id, next_stop.name)
            for route_id, next_stop in self.routes.items()
        ]
        return "\n".join(msg)


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

    :param uid:
    :return:
    """
    register_all_stations()
    try:
        return STATIONS[uid]
    except KeyError:
        return Station('foo', uid=uid)