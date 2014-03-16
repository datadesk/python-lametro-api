========
Bus data
========

Methods for retrieving data about buses, stops and routes in the L.A. Metro system.

Stops
-----

.. function:: client.bus.stops.get(id)

   Return the stop with the provided Metro identifer. ::

        >>> from la_metro import LAMetro
        >>> client = LAMetro()
        >>> client.bus.stops.get(6033)
        <BusStop: Santa Monica / Vermont>

.. attribute:: stop_obj.id

    The identifier in the Metro system

.. attribute:: stop_obj.name

    The name of the bus stop

.. attribute:: stop_obj.latitute

    The y coordinate of the stop's location

.. attribute:: stop_obj.longitude

    The x coordinate of the stop's location

.. attribute:: stop_obj.y

    Alias to the latitude of the stop's location

.. attribute:: stop_obj.x

    Alias to the longitude of the stop's location

.. attribute:: stop_obj.wkt

    The stop's location in Well-Known Text format

.. attribute:: stop_obj.geojson

    The stop's location in GeoJSON format

.. attribute:: stop_obj.messages

   Returns an messages Metro has left for users of this bus stop. This can contain information about service problems and delays.

.. attribute:: stop_obj.predictions

   Returns a list of predictions that guess when busses will next arrive at this stop.

.. attribute:: stop_obj.routes

   Returns a list of the routes that connect with this bus route.

Routes
------

.. function:: client.bus.routes.all()

   Return all routes in the Metro system ::

        >>> from la_metro import LAMetro
        >>> client = LAMetro()
        >>> client.bus.routes.all()
        [<BusRoute: 2>, <BusRoute: 4>, <BusRoute: 10>, <BusRoute: 14>, <BusRoute: 16>, <BusRoute: 18>, <BusRoute: 20>, <BusRoute: 26>, <BusRoute: 28>, <BusRoute: 30> ...]

.. function:: client.bus.routes.get(id)

   Return the route with the provided Metro identifer. ::

        >>> from la_metro import LAMetro
        >>> client = LAMetro()
        >>> client.bus.routes.get(704)
        <BusRoute: 704>

.. attribute:: route_obj.id

    The identifier in the Metro system

.. attribute:: route_obj.name

    The name of the bus route

.. attribute:: route_obj.runs

   Returns a list of the runs on this bus route.

.. attribute:: route_obj.stops

   Returns a list of the stops on this bus route in their proper order.

.. attribute:: route_obj.vehicles

   Returns a list of the vehicles on this bus route with their latest positions.

Vehicles
--------

.. function:: client.bus.vehicles.all()

   Return all vehicles out in the Metro system ::

        >>> from la_metro import LAMetro
        >>> client = LAMetro()
        [<BusVehicle: 3129>, <BusVehicle: 6735>, <BusVehicle: 7433>, <BusVehicle: 6729>, <BusVehicle: 9270>, <BusVehicle: 6758>, <BusVehicle: 7071>, <BusVehicle: 9306>, <BusVehicle: 8206>, <BusVehicle: 8314> ...]

.. function:: client.bus.vehicles.get(id)

   Return the vehicle with the provided Metro identifer. ::

        >>> from la_metro import LAMetro
        >>> client = LAMetro()
        >>> client.bus.vehicles.get(7433)
        <BusVehicle: 7433>

.. attribute:: vehicle_obj.id

    The identifier in the Metro system

.. attribute:: vehicle_obj.seconds_since_report

    The time since the data on this vehicle was last updated

.. attribute:: vehicle_obj.is_predictable

    The boolean indicator related to whether or not the busses arrival time can be predicted that I do not understand

.. attribute:: vehicle_obj.id

    The identifier in the Metro system

.. attribute:: vehicle_obj.latitute

    The y coordinate of the vehicle's location

.. attribute:: vehicle_obj.longitude

    The x coordinate of the vehicle's location

.. attribute:: vehicle_obj.y

    Alias to the latitude of the vehicle's location

.. attribute:: vehicle_obj.x

    Alias to the longitude of the vehicle's location

.. attribute:: vehicle_obj.wkt

    The vehicle's location in Well-Known Text format

.. attribute:: vehicle_obj.geojson

    The vehicle's location in GeoJSON format

.. attribute:: vehicle_obj.heading

.. attribute:: vehicle_obj.route

    The route the vehicle is on.

.. attribute:: vehicle_obj.run

    The run the vehicle is on.

Runs
----

.. attribute:: run_obj.id

    The identifier in the Metro system

.. attribute:: run_obj.name

    The name of the bus run

.. attribute:: run_obj.direction

    The direction the run is going along the route

.. attribute:: run_obj.route

    The route the run is on.

Predictions
-----------

.. attribute:: prediction_obj.stop

   The stop this prediction is estimating an arrival for

.. attribute:: prediction_obj.route

    The route the prediction is estimating an arrival for

.. attribute:: prediction_obj.run

    The run the prediction is estimating an arrival for

.. attribute:: prediction_obj.minutes

    The estimated arrival time in minutes

.. attribute:: prediction_obj.seconds

    The estimated arrival time in seconds

.. attribute:: prediction_obj.is_departing

    A boolean indicator I do not understand
