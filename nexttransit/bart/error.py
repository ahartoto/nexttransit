# Filename: error.py

"""
BART Error Module
"""

# NextTransit
from nexttransit.error import NextTransitError


class BartError(NextTransitError):
    """
    BART base exception class
    """
    pass


class BartServiceNotAvailableError(BartError):
    """
    BART's service is not available
    """
    pass


class BartQueryError(BartError):
    """
    BART's querying system returned unexpected content
    """
    pass
