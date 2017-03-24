# Filename: route.py

"""
BART Route Module
"""

# Standard libraries
import datetime

from xml.etree import ElementTree

# Requests
import requests

# NextTransit
from nexttransit import route

# BART
from nexttransit.bart import config
from nexttransit.bart import station
from nexttransit.bart.error import BartError, BartQueryError

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
        stations = [node.text.strip() for node in root.iter('station')]
        self.stops = stations

    def __str__(self):
        """
        String representation of a BART route

        :return: string
        """
        msg = [
            "{} route has {} stops:".format(self.name, len(self.stops)),
        ] + [
            "  {}".format(station.get(stop)) for stop in self.stops
        ]
        return "\n".join(msg)


def register_all_routes(date=datetime.date.today()):
    """
    Retrieve all routes that are currently run by the agency.

    :param date: instance of datetime.date (default: today)
    """
    global ROUTES
    if date.isoformat() in ROUTES:
        return
    else:
        ROUTES.clear()

    ROUTES[date.isoformat()] = dict()

    url = config.URL['routes'].format(date=date.strftime(config.STRFTIME),
                                      key=config.VALIDATION_KEY)
    response = requests.get(url)

    if response.status_code != config.GetResponseCodeEnum.SUCCESS.value:
        raise BartQueryError()

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

        ROUTES[date.isoformat()][uid] = cur_route


def get(uid, date=datetime.date.today()):
    """

    :param uid:
    :param date: instance of datetime.date (default: today)
    :return:
    """
    register_all_routes(date=date)
    dates = list(ROUTES.keys())
    return ROUTES[dates[0]][uid]


def iter_routes(date=datetime.date.today()):
    """

    :param date: instance of datetime.date (default: today)
    :return:
    """
    register_all_routes(date=date)
    dates = list(ROUTES.keys())
    yield from ROUTES[dates[0]].values()


def next_departure(orig, dest, date=datetime.date.today()):
    """
    Find the next departure time from the an origin station heading to
    destination station.

    :param orig: string - origin station (abbreviation)
    :param dest: string - destination station (abbreviation)
    :param date: instance of datetime.date (default: today)
    :return: an iterable of string
    """
    if orig == dest:
        raise BartError("origin and destination stations cannot be the same")

    orig_station = station.get(orig)
    dest_station = station.get(dest)

    # Find if there is any intersecting routes. If so, we would know the
    # direction as well as the relevant routes right away.
    relevant_routes = set()
    for orig_route in orig_station.routes:
        try:
            cur_route = get(orig_route, date=date)
        except KeyError:
            continue

        for dest_route in dest_station.routes:
            try:
                other_route = get(dest_route, date=date)
            except KeyError:
                continue

            relevant = True
            intersection = set(cur_route.stops) & set(other_route.stops)
            if orig in intersection and dest in intersection:
                if cur_route.stops.index(orig) <= cur_route.stops.index(dest):
                    relevant_routes.add(cur_route)
                    break

            for stop in intersection:
                stop_idx_in_cur = cur_route.stops.index(stop)
                if cur_route.stops.index(orig) > stop_idx_in_cur:
                    relevant = False
                    break

                stop_idx_in_other = other_route.stops.index(stop)
                if stop_idx_in_other > other_route.stops.index(dest):
                    relevant = False
                    break

            if relevant:
                relevant_routes.add(cur_route)
                break

    url = config.URL['etd'].format(station=orig_station.uid,
                                   key=config.VALIDATION_KEY)

    response = requests.get(url)
    if response.status_code != config.GetResponseCodeEnum.SUCCESS.value:
        raise BartQueryError()

    xml_str = response.content.decode()
    root = ElementTree.fromstring(xml_str)
    departures = set()
    for etd_node in root.iter('etd'):
        last_station = etd_node.find('abbreviation').text.strip()
        for cur_route in relevant_routes:
            if last_station in cur_route.stops[-2:]:
                for minutes_node in etd_node.iterfind('estimate/minutes'):
                    departures.add(minutes_node.text.strip())

    return _special_sort(departures)


def _special_sort(departures):
    if 'Leaving' in departures:
        departures.remove('Leaving')
        departures = sorted(departures, key=int)
        departures.insert(0, 'Leaving')
    else:
        departures = sorted(departures, key=int)
    return departures
