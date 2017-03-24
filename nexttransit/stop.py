# Filename: stop.py

"""
Transit Stop Module
"""


class TransitStop(object):
    """
    A representation of a stop
    """
    def __init__(self, name, uid=None, address=None, city=None,
                 coordinate=None):
        """
        Constructor

        :param name: name of the stop
        :param uid: unique identifier of the stop
        :param address: address of the stop (street info)
        :param city: city where the stop is
        :param coordinate: coordinate (lat, lon) of the stop
        """
        self.name = name
        self.uid = uid
        self.address = address
        self.city = city
        self.coordinate = coordinate
        self.routes = set()
