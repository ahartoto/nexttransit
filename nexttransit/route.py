# Filename: route.py

"""
Transit Route Module
"""

# Standard libraries


class Route(object):
    """
    A representation of a route. Every route has:
    * name - string
    * id - unique identification (string) for the route for the agency
    * stops - list of stops relevant for the route
    """
    def __init__(self, name, uid):
        """
        Constructor

        :param uid: string - unique identification of a route
        """
        self.name = str(name)
        self.uid = str(uid)
        self.stops = list()

    def in_route(self, origin, dest=None):
        """

        :param origin:
        :param dest: (default: None)
        :return: boolean
        """
        pass
