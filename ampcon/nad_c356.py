import logging
import serial

__author__ = 'zeraien'
SOURCES = ["MP", "AUX", "CD"]

class SerialConnection(object):

    def __init__(self, serial_port, logger):
        self.serial_port = serial_port
        self.logger = logger

    def __enter__(self):
        self.port = None
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def set_bool(self, key, value):
        return self.send_command("%s=%s" % (key, self._from_bool(value)))

    def set_value(self, key, value):
        return self.send_command("%s=%s" % (key, value))

    def ask(self, what):
        return self.send_command("%s?" % what)

    def send_command(self, cmd):

        self.logger.debug("Sending:\t\t%s" % cmd)

        self.port.write("\nMain.%s\n" % cmd)
        self.port.readline()
        response = self.port.readline().strip()

        self.logger.debug("Raw response:\t\t%s" % response)

        actual_value = self._to_bool(response)

        self.logger.debug("Response:\t\t%s" % actual_value)

        return actual_value

    def connect(self):
        if self.port is None:
            self.port = serial.Serial(port=self.serial_port,
                                      baudrate=115200,
                                      bytesize=serial.EIGHTBITS,
                                      parity=serial.PARITY_NONE,
                                      stopbits=serial.STOPBITS_ONE,
                                      timeout=2,
                                      xonxoff=0,
                                      rtscts=0,
                                      dsrdtr=0
                                      )

    def disconnect(self):
        if self.port:
            self.port.close()
            self.port = None

    def _to_bool(self, data):
        if '=' in data:
            value = data.split('=')[1].lower()
        else:
            value = data

        if value in ("on", "off"):
            return value == 'on'
        else:
            return value

    def _from_bool(self, value):
        if value in (True, False):
            return value is True and "On" or "Off"
        else:
            return value
