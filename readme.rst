solarshed
=========

A Python library to help monitor solar charge controllers typically used in
off the grid applications.

The primary goal of the library is to provide a common interface in Python
for a variety of solar charge controllers.  A secondary goal is for easy monitoring
of off the grid solar installations via Prometheus using the included
solarshed.server module.  This project has been in use for several months on a
Raspberry Pi connected to a Renogy Rover solar controller.  This off the grid
solar installation is mobile on a trailer and links up to WiFi for monitoring
and alerting via Prometheus (with solar production visualized using Grafana)

.. image:: images/solarshed_front.jpg
    :alt: Solarshed Trailer (front)


Supported Solar Charge Controllers
----------------------------------

* **Renogy Rover**
  The Renogy Rover is currently the only supported charge controller.
  New charge controllers should be added to the solarshed.controllers
  package.


Charge Controller module contributions are welcome if you have access
to the hardware to help test and verify functionality.

Prometheus Support
------------------

The solarshed library includes a server process that may be used in cases
where you'd like continuous monitoring of a solar installation.
This process periodically reads information from the connected solar controller
and exposes it as prometheus gauges for easy collection and monitoring.

TODO
----

There's still a lot to be done.  The project is still in the early stages
but has been up and running continuously on an off the grid solar "shed" that's
on a trailer.  This project started out as a cool meet up idea and has grown
from there.  The project needs some configuration support in order to handle a growing
number of supported solar charge controllers.
The steps to install and run on a Raspberry Pi are also needed as documentation
and automated scripts.
