# Filename: test_bart.py

# NextTransit Bart
from nexttransit.bart import route
from nexttransit.bart import station


class TestBart(object):
    @classmethod
    def setup_class(cls):
        route.register_all_routes()

    def test_register_stations(self):
        for _, cur_station in station.STATIONS.items():
            print(cur_station)

    def test_register_routes(self):
        for _, cur_route in route.ROUTES.items():
            print(cur_route)

    def test_next_departure(self):
        print(route.next_departure('MCAR', 'SFIA'))
        print(route.next_departure('PLZA', 'DBRK'))
        print(route.next_departure('RICH', 'FRMT'))
