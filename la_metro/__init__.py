"""
Python library for interacting with the L.A. Metro API.

Further documentation:

    http://datadesk.github.io/python-lametro-api/
    http://developer.metro.net/introduction/realtime-api-overview/

"""
from __future__ import unicode_literals
import sys
import six
import requests


#
# 2to3 fixes
#

class UnicodeMixin(object):
    """
    Make our unicode methods play nice.

    Docs: http://lucumr.pocoo.org/2011/1/22/forwards-compatible-python/
    """
    if sys.version_info > (3, 0):
        __str__ = lambda x: x.__unicode__()
    else:
        __str__ = lambda x: six.text_type(x).encode('utf-8')


#
# API connection mixins
#

class BaseLAMetroClient(object):
    """
    Patterns common to all of the different API methods.
    """
    BASE_URI = 'http://api.metro.net/agencies/lametro/'

    def _make_request(self, resource):
        """
        Configure a HTTP request, fire it off and return the response.
        """
        url = self.BASE_URI + resource
        response = requests.get(url)
        return response.json()


class GeoObject(object):
    """
    Common attributes of an API object that contains geospatial data
    """
    @property
    def x(self):
        return self.longitude

    @property
    def y(self):
        return self.latitude

    @property
    def wkt(self):
        if not self.longitude or not self.latitude:
            return None
        return 'POINT(%s %s)' % (self.longitude, self.latitude)

    @property
    def geojson(self):
        if not self.longitude or not self.latitude:
            return None
        return '{"type": "Point", "coordinates": [%s, %s]}' % (
            self.longitude, self.latitude
        )


#
# The public API client
#

class LAMetro(BaseLAMetroClient):
    """
    The public interface for the L.A. Metro API
    """
    def __init__(self):
        self.bus = BusClient()


#
# Bus methods
#

class BusClient(BaseLAMetroClient):
    """
    Methods for collecting documents
    """
    def __init__(self):
        self.routes = BusRouteClient()
        self.stops = BusStopClient()
        self.vehicles = BusVehicleClient()


class BusRouteClient(BaseLAMetroClient):
    """
    Methods for collecting bus routes
    """
    def all(self):
        """
        Retrieve all routes in the system.
        """
        json = self._make_request('routes/')
        return [
            BusRoute(i['id'], i['display_name'], self)
            for i in json.get("items")
        ]

    def get(self, id):
        json = self._make_request('routes/%s/' % id)
        return BusRoute(json['id'], json['display_name'], self)


class BusStopClient(BaseLAMetroClient):
    """
    Methods for collecting bus stops
    """
    def get(self, id):
        json = self._make_request('stops/%s/' % id)
        return BusStop(json['id'], json['display_name'], connection=self)


class BusVehicleClient(BaseLAMetroClient):
    """
    Methods for collecting bus vehicles
    """
    def all(self):
        """
        Retrieve all vehicles in the system.
        """
        json = self._make_request('vehicles/')
        return [BusVehicle(
            j["id"],
            j['predictable'],
            j['seconds_since_report'],
            j['latitude'],
            j['longitude'],
            j['heading'],
            j['route_id'],
            j.get("run_id", ""),
            self,
            None,
        ) for j in json.get("items")]

    def get(self, id):
        """
        Retrieve a particular vehicle
        """
        json = self._make_request('vehicles/%s/' % id)
        return BusVehicle(
            json["id"],
            json['predictable'],
            json['seconds_since_report'],
            json['latitude'],
            json['longitude'],
            json['heading'],
            json['route_id'],
            json.get("run_id", ""),
            self,
            None,
        )


#
# API objects
#

class BaseAPIObject(UnicodeMixin):
    """
    An abstract version of the objects returned by the API.
    """
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.__str__())

    def __unicode__(self):
        return six.text_type('%s' % self.name)


class BusRoute(BaseAPIObject):

    def __init__(self, id, name, connection):
        self.id = id
        self.name = name
        self._connection = connection

    def __unicode__(self):
        return six.text_type('%s' % self.id)

    def get_runs(self):
        """
        Fetch the runs on this route if they have not already been pulled.
        """
        try:
            return self.__dict__['runs']
        except KeyError:
            json = self._connection._make_request('routes/%s/runs/' % self.id)
            obj_list = [BusRun(
                j["id"],
                j['display_name'],
                j['direction_name'],
                self,
                self._connection,
            ) for j in json.get("items")]
            self.__dict__['runs'] = obj_list
            return obj_list
    runs = property(get_runs)

    def get_stops(self):
        """
        Fetch the stops, in proper sequence, if they
        have not already been pulled.
        """
        try:
            return self.__dict__['stops']
        except KeyError:
            json = self._connection._make_request(
                'routes/%s/sequence/' % self.id
            )
            obj_list = [BusStop(
                j.get("id", ""),
                j['display_name'],
                j['latitude'],
                j['longitude'],
                self._connection,
            ) for j in json.get("items")]
            self.__dict__['stops'] = obj_list
            return obj_list
    stops = property(get_stops)

    def get_vehicles(self):
        """
        Fetch the latest position of the vehicles on this route.
        """
        json = self._connection._make_request('routes/%s/vehicles/' % self.id)
        return [BusVehicle(
            j["id"],
            j['predictable'],
            j['seconds_since_report'],
            j['latitude'],
            j['longitude'],
            j['heading'],
            j['route_id'],
            j.get("run_id", ""),
            self._connection,
            self,
        ) for j in json.get("items")]
    vehicles = property(get_vehicles)


class BusStop(BaseAPIObject, GeoObject):

    def __init__(
        self, id, name, latitude=None, longitude=None, connection=None
    ):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self._connection = connection

    def get_messages(self):
        """
        Fetch any messages for this stop.
        """
        if self.id:
            json = self._connection._make_request(
                'stops/%s/messages/' % self.id
            )
            obj_list = [BusMessage(j) for j in json.get("items")]
        else:
            obj_list = []
        return obj_list
    messages = property(get_messages)

    def get_predictions(self):
        """
        Fetch the predictions for this stop.
        """
        if self.id:
            json = self._connection._make_request(
                'stops/%s/predictions/' % self.id
            )
            obj_list = [BusPrediction(
                self,
                j['route_id'],
                j['run_id'],
                j['block_id'],
                j['minutes'],
                j['seconds'],
                j['is_departing'],
                self._connection,
            ) for j in json.get("items")]
        else:
            obj_list = []
        return obj_list
    predictions = property(get_predictions)

    def get_routes(self):
        """
        Fetch the routes that visit this stop,
        if they havn't already been pulled.
        """
        try:
            return self.__dict__['routes']
        except KeyError:
            json = self._connection._make_request('stops/%s/routes/' % self.id)
            obj_list = [BusRoute(
                i['id'],
                i['display_name'],
                self._connection)
                for i in json.get("items")
            ]
            self.__dict__['routes'] = obj_list
            return obj_list
    routes = property(get_routes)


class BusMessage(BaseAPIObject):

    def __init__(self, text):
        self.text = text

    def __unicode__(self):
        return six.text_type('%s' % self.text)


class BusPrediction(BaseAPIObject):

    def __init__(
        self, stop, route_id, run_id, block_id, minutes,
        seconds, is_departing, connection
    ):
        self.stop = stop
        self.route_id = route_id
        self.run_id = run_id
        self.block_id = block_id
        self.minutes = minutes
        self.seconds = seconds
        self.is_departing = is_departing
        self._connection = connection

    def __unicode__(self):
        return six.text_type('%s (%s)' % (self.stop.name, self.route_id))

    def get_route(self):
        """
        Fetch the route, if it hasn't already been pulled.
        """
        try:
            return self.__dict__['route']
        except KeyError:
            json = self._connection._make_request('routes/%s/' % self.route_id)
            obj = BusRoute(json['id'], json['display_name'], self._connection)
            self.__dict__['route'] = obj
            return obj
    route = property(get_route)

    def get_run(self):
        """
        Fetch the run, if it hasn't already been pulled.
        """
        try:
            return self.__dict__['run']
        except KeyError:
            route = self.get_route()
            for run in route.get_runs():
                if run.id.split("_")[-1] == self.run_id.split("_")[-1]:
                    self.__dict__['run'] = run
                    return run
            self.__dict__['run'] = None
            return None
    run = property(get_run)


class BusRun(BaseAPIObject):

    def __init__(self, id, name, direction, route, connection):
        self.id = id
        self.name = name
        self.direction = direction
        self.route = route
        self._connection = connection

    def __unicode__(self):
        return six.text_type('%s (%s)' % (self.name, self.route.id))


class BusVehicle(BaseAPIObject, GeoObject):

    def __init__(
        self, id, is_predictable, seconds_since_report, latitude,
        longitude, heading, route_id, run_id, connection, route=None
    ):
        self.id = id
        self.is_predictable = is_predictable
        self.seconds_since_report = seconds_since_report
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading
        self.route_id = route_id
        self.run_id = run_id
        self._connection = connection
        if route:
            self.route = route

    def __unicode__(self):
        return six.text_type('%s' % self.id)

    def set_route(self, route):
        if not isinstance(route, BusRoute):
            raise TypeError
        self.__dict__['route'] = route

    def get_route(self):
        """
        Fetch the route, if it hasn't already been pulled.
        """
        try:
            return self.__dict__['route']
        except KeyError:
            json = self._connection._make_request('routes/%s/' % self.route_id)
            obj = BusRoute(json['id'], json['display_name'], self._connection)
            self.__dict__['route'] = obj
            return obj
    route = property(get_route, set_route)

    def get_run(self):
        """
        Fetch the run, if it hasn't already been pulled.
        """
        try:
            return self.__dict__['run']
        except KeyError:
            for run in self.route.get_runs():
                if run.id.split("_")[-1] == self.run_id.split("_")[-1]:
                    self.__dict__['run'] = run
                    return run
            self.__dict__['run'] = None
            return None
    run = property(get_run)
