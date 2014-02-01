#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests out the LA Metro API.
"""
import random
import unittest
from la_metro import LAMetro
from la_metro import BusRun, BusVehicle
from la_metro import BusRoute, BusStop, BusMessage, BusPrediction


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.client = LAMetro()


class BusRouteTests(BaseTest):

    def setUp(self):
        super(BusRouteTests, self).setUp()
        self.route_list = self.client.bus.routes.all()
        self.random_route = self.route_list[0]

    def test_all(self):
        """
        Test a request that returns all the routes in the system.
        """
        self.assertEqual(type(self.route_list), type([]))
        [self.assertEqual(type(i), BusRoute) for i in self.route_list]

    def test_get(self):
        """
        Test a request that returns a particular bus route.
        """
        obj = self.client.bus.routes.get(self.random_route.id)
        self.assertEqual(type(obj), BusRoute)
        self.assertEqual(obj.id, self.random_route.id)
        self.assertEqual(obj.name, self.random_route.name)

    def test_get_stops(self):
        """
        Test a lazy-loaded call to the stops.
        """
        obj = self.client.bus.routes.get(self.random_route.id)
        stops = obj.stops
        self.assertEqual(type(stops), type([]))
        [self.assertEqual(type(i), BusStop) for i in stops]
        self.assertEqual(stops[0].longitude, stops[0].x)
        self.assertEqual(stops[0].latitude, stops[0].y)
        stops[0].wkt
        stops[0].geojson
        stops[0].__repr__()
        stops[0].__str__()
        stops[0].__unicode__()

    def test_get_runs(self):
        """
        Test a lazy-loaded call to the runs.
        """
        obj = self.client.bus.routes.get(self.random_route.id)
        self.assertEqual(type(obj.runs), type([]))
        [self.assertEqual(type(i), BusRun) for i in obj.runs]
        [self.assertEqual(type(i.route), BusRoute) for i in obj.runs]
        obj.runs[0].__repr__()
        obj.runs[0].__str__()
        obj.runs[0].__unicode__()
    
    def test_get_vehicles(self):
        """
        Test a request for vehicles on this route.
        """
        obj = self.client.bus.routes.get(self.random_route.id)
        vehicles = obj.vehicles
        self.assertEqual(type(vehicles), type([]))
        self.assertEqual(vehicles[0].longitude, vehicles[0].x)
        self.assertEqual(vehicles[0].latitude, vehicles[0].y)
        vehicles[0].wkt
        vehicles[0].geojson
        [self.assertEqual(type(i), BusVehicle) for i in vehicles]
        [self.assertEqual(type(i.route), BusRoute) for i in vehicles]
        [self.assertEqual(type(i.run), BusRun)
            for i in vehicles if i.is_predictable]
        [self.assertEqual(type(i.run), type(None))
            for i in vehicles if not i.is_predictable]
        vehicles[0].__repr__()
        vehicles[0].__str__()
        vehicles[0].__unicode__()
        self.assertRaises(TypeError, vehicles[0].set_route, 'foobar')


class BusStopTests(BaseTest):

    def setUp(self):
        super(BusStopTests, self).setUp()
        self.route_list = self.client.bus.routes.all()
        self.random_route = self.route_list[0]
        self.random_stop = self.random_route.stops[0]
        self.stop = self.client.bus.stops.get(self.random_stop.id)

    def test_get(self):
        """
        Test a request that returns a particular bus stop.
        """
        self.assertEqual(type(self.stop), BusStop)
        self.assertEqual(self.stop.id, self.random_stop.id)
        self.assertEqual(self.stop.name, self.random_stop.name)

    def test_get_messages(self):
        """
        Test a call for messages
        """
        obj = self.client.bus.stops.get(self.random_stop.id)
        self.assertEqual(type(self.stop.messages), type([]))
        [self.assertEqual(type(i), BusMessage) for i in self.stop.messages]
        bm = BusMessage('foo')
        bm.__repr__()
        bm.__str__()
        bm.__unicode__()

    def test_get_predictions(self):
        """
        Test a call for a prediction.
        """
        predictions = self.stop.predictions
        self.assertEqual(type(predictions), type([]))
        [self.assertEqual(type(i), BusPrediction) for i in predictions]
        [self.assertEqual(type(i.route), BusRoute) for i in predictions]
        [self.assertEqual(type(i.run), BusRun) for i in predictions]
        predictions[0].__repr__()
        predictions[0].__str__()
        predictions[0].__unicode__()

    def test_get_routes(self):
        """
        Test a call for routes that visit this stop.
        """
        routes = self.stop.routes
        self.assertEqual(type(routes), type([]))
        [self.assertEqual(type(i), BusRoute) for i in routes]
        routes[0].__repr__()
        routes[0].__str__()
        routes[0].__unicode__()


class BusVehicleTests(BaseTest):

    def setUp(self):
        super(BusVehicleTests, self).setUp()
        self.vehicle_list = self.client.bus.vehicles.all()

    def test_all(self):
        """
        Test a request that returns all the vehicles in the system.
        """
        self.assertEqual(type(self.vehicle_list), type([]))
        [self.assertEqual(type(i), BusVehicle) for i in self.vehicle_list]

    def test_get(self):
        """
        Test a request that returns a particular bus vehicle.
        """
        num = random.choice(self.vehicle_list).id
        obj = self.client.bus.vehicles.get(num)
        self.assertEqual(type(obj), BusVehicle)
        self.assertEqual(obj.id, num)
        self.assertEqual(type(obj.run), BusRun)


if __name__ == '__main__':
    unittest.main()
