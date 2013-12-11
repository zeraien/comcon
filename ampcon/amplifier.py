from nad_c356 import SerialConnection, SOURCES

__author__ = 'zeraien'


class Amplifier(object):

    def __init__(self, serial_port, logger):
        self.serial_port = serial_port
        self.configured = False
        self.logger = logger

    def connection(self):
        return SerialConnection(serial_port=self.serial_port, logger=self.logger)

    def set_source(self, what_source):
        with self.connection() as conn:
            what_source = what_source.strip().upper()
            idx = SOURCES.index(what_source)
            if idx >= 0:
                self.source = conn.set_value("Source", SOURCES[idx])

    def mute_toggle(self):
        with self.connection() as conn:
            self.mute = conn.set_bool("Mute", not self.mute)

    def power_toggle(self):
        with self.connection() as conn:
            self.power = conn.set_bool("Power", not self.power)
        self.configure()

    def speaker_a_toggle(self):
        with self.connection() as conn:
            self.speaker_a = conn.set_bool("SpeakerA", not self.speaker_a)

    def volume_down(self):
        with self.connection() as conn:
            conn.send_command("Volume-")
    def volume_up(self):
        with self.connection() as conn:
            conn.send_command("Volume+")

    def ask(self, conn, what):
        if what.lower() == 'power' or self.power:
            return conn.ask(what=what)
        else:
            return False


    def configure(self):
        with self.connection() as conn:
            self.power = self.ask(conn, "Power")
            self.mute = self.ask(conn, "Mute")
            self.source = self.ask(conn, "Source")
            self.speaker_a = self.ask(conn, "SpeakerA")
            self.configured = True

    def json_ready(self):
        data = {}
        for source in SOURCES:
            source = source.lower()
            data['source_%s' % source] = (self.source == source)

        data.update({
            'mute': self.mute,
            'speaker_a': self.speaker_a,
            'power': self.power,
            'source': self.source,
        })
        return data
