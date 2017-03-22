# Filename: route.py

"""
BART Route Module
"""

# Standard libraries
from xml.etree import ElementTree

# Requests
import requests

# NextTransit
from nexttransit import route

# BART
from nexttransit.bart import config
from nexttransit.bart import station
from nexttransit.bart.error import BartQueryError

# Global
ROUTES = dict()


class Route(route.Route):
    """
    A representation of a BART route.
    """
    def __init__(self, name, uid, color=None, number=None):
        """
        Constructor

        :param uid: string - unique identification of a route
        """
        super().__init__(name, uid)
        self.color = color
        self.number = number

    def update_stations(self):
        """
        Find all stations relevant to this route, and connect them.
        """
        url = config.URL['route_info'].format(number=self.number,
                                              key=config.VALIDATION_KEY)
        response = requests.get(url)

        if response.status_code != config.GetResponseCodeEnum.SUCCESS.value:
            raise BartQueryError()

        xml_str = response.content.decode()
        root = ElementTree.fromstring(xml_str)
        stations = [station.get(node.text) for node in root.iter('station')]

        # Connect these stations
        for index, cur_station in enumerate(stations[:-1]):
            cur_station.add_next_stop(self.uid, stations[index + 1])

        self.stops = stations

    def __str__(self):
        """

        :return:
        """
        msg = [
            "{} route has {} stops:".format(self.name, len(self.stops)),
        ] + [
            "  {}".format(stop.name) for stop in self.stops
        ]
        return "\n".join(msg)


def register_all_routes():
    """
    Retrieve all routes that are currently run by the agency.
    """
    url = config.URL['routes'].format(key=config.VALIDATION_KEY)
    response = requests.get(url)

    if response.status_code != config.GetResponseCodeEnum.SUCCESS.value:
        raise BartQueryError()

    global ROUTES
    xml_str = response.content.decode()
    root = ElementTree.fromstring(xml_str)

    for route_node in root.iter('route'):
        uid = route_node.find('routeID').text.strip()
        name = route_node.find('name').text.strip()
        number = route_node.find('number').text.strip()
        color = route_node.find('hexcolor').text
        cur_route = Route(name, uid, color=color, number=number)

        # Get all relevant stations for this route
        cur_route.update_stations()

        ROUTES[uid] = cur_route


def get(uid):
    """

    :param uid:
    :return:
    """
    return ROUTES[uid]


def iter_routes():
    """

    :return:
    """
    yield from ROUTES.values()


def next_departure(orig, dest):
    """
    Find the next departure time from the an origin station heading to
    destination station.

    :param orig: string - origin station (abbreviation)
    :param dest: string - destination station (abbreviation)
    :return: an iterable of string
    """
    direction = None

    orig_station = station.get(orig)
    dest_station = station.get(dest)

    # Find the route (north-bound or south-bound)
    # First, we know all the routes that this station serves
    relevant_routes = list()
    for cur_route in iter_routes():
        if orig_station in cur_route.stops and dest_station in cur_route.stops:
            orig_index = cur_route.stops.index(orig_station)
            dest_index = cur_route.stops.index(dest_station)
            if orig_index < dest_index:
                if cur_route.uid in orig_station.north_routes:
                    direction = 'n'
                else:
                    direction = 's'
                relevant_routes.append(cur_route)

    if direction is None:
        url = config.URL['etd'].format(station=orig_station.uid,
                                       key=config.VALIDATION_KEY)
    else:
        url = config.URL['etd_dir'].format(station=orig_station.uid,
                                           key=config.VALIDATION_KEY,
                                           direction=direction)

    response = requests.get(url)
    if response.status_code != config.GetResponseCodeEnum.SUCCESS.value:
        raise BartQueryError()

    xml_str = response.content.decode()
    root = ElementTree.fromstring(xml_str)
    departures = set()
    for etd_node in root.iter('etd'):
        abbr_node = etd_node.find('abbreviation')
        last_station = station.get(abbr_node.text)
        for cur_route in relevant_routes:
            if last_station in cur_route.stops[-2:]:
                for minutes_node in etd_node.iterfind('estimate/minutes'):
                    departures.add(minutes_node.text)

    return _special_sort(departures)


def _special_sort(departures):
    if 'Leaving' in departures:
        departures.remove('Leaving')
        departures = sorted(departures, key=int)
        departures.insert(0, 'Leaving')
    else:
        departures = sorted(departures, key=int)
    return departures
