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

        :param name:
        :param uid:
        :param address:
        :param city:
        :param coordinate:
        """
        self.name = name
        self.uid = uid
        self.address = address
        self.city = city
        self.coordinate = coordinate
        self.routes = dict()

    def add_next_stop(self, route_uid, next_stop):
        """

        :param route_uid:
        :param next_stop:
        :return:
        """
        self.routes[route_uid] = next_stop

    def get_next_stop(self, route_uid):
        """

        :param route_uid:
        :return:
        """
        return self.routes[route_uid]
