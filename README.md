comcon
======

Control RS-232 devices in a browser.

Current version is very basic and only works with one amplifier, NAD C356. However it should not be too
difficult to write modules for other devices.

The plan is to create a plugin infrastructure to allow for easy addition of support for other devices,
with the UI adapting automatically.

Most likely a YAML configuration file will be used to define devices and commands.

Installation
==============

Required python libs:

  pyserial
  Flask
  Jinja2
  

Put **bootstrap 3** into the ampcon/static/bootstrap folder.

Put **jquery 2** into the ampcon/static folder.



Additional files for CGI and WSGI installations will be added at some point.
