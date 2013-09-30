#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests out the LA Metro API.
"""
import os
import random
import unittest
from la_metro import LAMetro
from la_metro import BusRoute, BusStop, BusMessage, BusPrediction, BusRun, BusVehicle

#
# Tests
#

class BaseTest(unittest.TestCase):
    
    def setUp(self):
        self.client = LAMetro()


class BusRouteTests(BaseTest):
    
    def test_all(self):
        """
        Test a request that returns all the routes in the system.
        """
        obj_list = self.client.bus.routes.all()
        self.assertEqual(type(obj_list), type([]))
        [self.assertEqual(type(i), BusRoute) for i in obj_list]
    
    def test_get(self):
        """
        Test a request that returns a particular bus route.
        """
        obj = self.client.bus.routes.get(704)
        self.assertEqual(type(obj), BusRoute)
        self.assertEqual(obj.id, '704')
        self.assertEqual(obj.name, '704 Downtown LA - Santa Monica Via Santa Monica Bl')
    
    def test_get_stops(self):
        """
        Test a lazy-loaded call to the stops.
        """
        obj = self.client.bus.routes.get(704)
        self.assertEqual(type(obj.stops), type([]))
        [self.assertEqual(type(i), BusStop) for i in obj.stops]
    
    def test_get_runs(self):
        """
        Test a lazy-loaded call to the runs.
        """
        obj = self.client.bus.routes.get(704)
        self.assertEqual(type(obj.runs), type([]))
        [self.assertEqual(type(i), BusRun) for i in obj.runs]
        [self.assertEqual(type(i.route), BusRoute) for i in obj.runs]
    
    def test_get_vehicles(self):
        """
        Test a request for vehicles on this route.
        """
        obj = self.client.bus.routes.get(704)
        self.assertEqual(type(obj.vehicles), type([]))
        [self.assertEqual(type(i), BusVehicle) for i in obj.vehicles]
        [self.assertEqual(type(i.route), BusRoute) for i in obj.vehicles]
        [self.assertEqual(type(i.run), BusRun) for i in obj.vehicles if i.is_predictable]
        [self.assertEqual(type(i.run), type(None)) for i in obj.vehicles if not i.is_predictable]


class BusStopTests(BaseTest):
    
    def test_get(self):
        """
        Test a request that returns a particular bus stop.
        """
        obj = self.client.bus.stops.get(6033)
        self.assertEqual(type(obj), BusStop)
        self.assertEqual(obj.id, '6033')
        self.assertEqual(obj.name, 'Santa Monica / Vermont')
    
    def test_get_messages(self):
        """
        Test a call for messages
        """
        obj = self.client.bus.stops.get(6033)
        self.assertEqual(type(obj.messages), type([]))
        [self.assertEqual(type(i), BusMessage) for i in obj.messages]
    
    def test_get_predictions(self):
        """
        Test a call for a prediction.
        """
        obj = self.client.bus.stops.get(6033)
        self.assertEqual(type(obj.predictions), type([]))
        [self.assertEqual(type(i), BusPrediction) for i in obj.predictions]
        [self.assertEqual(type(i.route), BusRoute) for i in obj.predictions]
        [self.assertEqual(type(i.run), BusRun) for i in obj.predictions]
    
    def test_get_routes(self):
        """
        Test a call for routes that visit this stop.
        """
        obj = self.client.bus.stops.get(6033)
        self.assertEqual(type(obj.routes), type([]))
        [self.assertEqual(type(i), BusRoute) for i in obj.routes]


class BusVehicleTests(BaseTest):
    
    def test_all(self):
        """
        Test a request that returns all the vehicles in the system.
        """
        obj_list = self.client.bus.vehicles.all()
        self.assertEqual(type(obj_list), type([]))
        [self.assertEqual(type(i), BusVehicle) for i in obj_list]
    
    def test_get(self):
        """
        Test a request that returns a particular bus vehicle.
        """
        obj_list = self.client.bus.vehicles.all()
        num = random.choice(obj_list).id
        obj = self.client.bus.vehicles.get(num)
        self.assertEqual(type(obj), BusVehicle)
        self.assertEqual(obj.id, num)
        self.assertEqual(type(obj.run), BusRun)


if __name__ == '__main__':
    unittest.main()
