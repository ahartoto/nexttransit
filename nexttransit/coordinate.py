# Filename: coordinate.py

"""
Next Transit Coordinate Module
"""


class GTFSCoordinate(object):
    """
    Coordinate/location of where the stops are
    """
    def __init__(self, latitude, longitude):
        """
        Constructor

        :param latitude: string
        :param longitude: string
        """
        self.latitude = latitude
        self.longitude = longitude
