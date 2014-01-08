comcon
======

Control RS-232 devices such as amplifiers and projectors in a browser.

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

Required web libs:

    boostrap3 in ampcon/static/bootstrap
    jquery2 in ampcon/static/
    

Additional files for CGI and WSGI installations will be added at some point.
In the mean time, run it using the flask development server or roll your own CGI conf.
