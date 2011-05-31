===============
Getting started
===============

This tutorial will walk you through the process of installing python-lametro-api and making your first requests.

.. raw:: html

   <hr>

Installation
------------

Provided that you have `pip <http://pypi.python.org/pypi/pip>`_ installed, you can install the library like so: ::

    $ pip install python-lametro-api

.. raw:: html

   <hr>

Creating a client
-----------------

Before you can interact with Metro's data, you first must import the library and initialize a client to talk with the site on your behalf. ::

    >>> from la_metro import LAMetro
    >>> client = LAMetro()

.. raw:: html

   <hr>

Retrieve a bus stop and get predictions for incoming busses
-------------------------------------------------------------

    >>> obj = client.bus.stops.get(6033)
    >>> obj
    <BusStop: Santa Monica / Vermont>
    >>> obj.predictions
    [<BusPrediction: Santa Monica / Vermont (4)>, <BusPrediction: Santa Monica / Vermont (4)>]

.. raw:: html

   <hr>

Retrieve a bus route and get the location of all stops and vehicles
-------------------------------------------------------------------

    >>> obj = client.bus.routes.get(704)
    >>> obj
    <BusRoute: 704>
    >>> obj.stops
    [<BusStop: 2nd / Santa Monica>, <BusStop: Ocean / Santa Monica>, <BusStop: Santa Monica / 4th>, <BusStop: Santa Monica / Lincoln>, <BusStop: Santa Monica / 20th>, <BusStop: Santa Monica / 26th>, <BusStop: Santa Monica / Bundy>, <BusStop: Santa Monica / Barrington>, <BusStop: Santa Monica / Sepulveda>, <BusStop: Santa Monica / Westwood>, <BusStop: Santa Monica / Beverly Glen>, <BusStop: Santa Monica / Ave Of The Stars>, <BusStop: Santa Monica / Wilshire>, <BusStop: Santa Monica / Canon>, <BusStop: Santa Monica / San Vicente>, <BusStop: Santa Monica / La Cienega>, <BusStop: Santa Monica / Sweetzer>, <BusStop: Santa Monica / Fairfax>, <BusStop: Santa Monica / La Brea>, <BusStop: Santa Monica / Highland>, <BusStop: Santa Monica / Vine>, <BusStop: Santa Monica / Western>, <BusStop: Santa Monica / Normandie>, <BusStop: Santa Monica / Vermont>, <BusStop: Sunset / Sanborn>, <BusStop: Sunset / Parkman>, <BusStop: Sunset / Alvarado>, <BusStop: Sunset / Echo Park>, <BusStop: Sunset / Figueroa>, <BusStop: Cesar E Chavez / Grand>, <BusStop: Cesar E Chavez / Spring>, <BusStop: Vignes / Cesar E Chavez>, <BusStop: Terminal 31>]
    >>> obj.vehicles
    [<BusVehicle: 9364>, <BusVehicle: 9376>, <BusVehicle: 9391>, <BusVehicle: 9380>, <BusVehicle: 9390>, <BusVehicle: 9399>, <BusVehicle: 9373>, <BusVehicle: 9372>, <BusVehicle: 9371>]

.. raw:: html

   <hr>

Get the location of vehicles
----------------------------

Here's how you can get all vehicles::

    >>> obj_list = client.bus.vehicles.all()
    >>> len(obj_list)
    392
    >>> obj_list[0]
    <BusVehicle: 7433>

And here's how to get a single one::

    >>> obj = client.bus.vehicles.get(7433)
    >>> obj.latitude, obj.longitude
    (34.047089, -118.282776)


