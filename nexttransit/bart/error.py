# Filename: error.py

"""
BART Error Module
"""

# NextTransit
from nexttransit.error import NextTransitError


class BartError(NextTransitError):
    """

    """
    pass


class BartServiceNotAvailableError(BartError):
    """

    """
    pass


class BartQueryError(BartError):
    """

    """
    pass
