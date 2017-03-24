# Filename: test_bart.py

# PyTest
import pytest

# NextTransit Bart
from nexttransit.bart.error import BartError
from nexttransit.bart import route
from nexttransit.bart import station


class TestBart(object):
    @classmethod
    def setup_class(cls):
        route.register_all_routes()
        station.register_all_stations()

    def test_routes(self):
        for cur_route in route.iter_routes():
            print(cur_route)
            assert isinstance(cur_route, route.Route)

    def test_stations(self):
        for cur_station in station.iter_station():
            print(cur_station)
            assert isinstance(cur_station, station.Station)

    def test_next_departure(self):
        print(route.next_departure('FRMT', 'SFIA'))
        print(route.next_departure('PLZA', 'DBRK'))
        print(route.next_departure('RICH', 'FRMT'))

        with pytest.raises(BartError):
            route.next_departure('MLBR', 'MLBR')
