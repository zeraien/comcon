from nad_c356 import SerialConnection, SOURCES

__author__ = 'zeraien'


class Amplifier(object):

    def __init__(self, serial_port, logger):
        self.serial_port = serial_port
        self.configured = False
        self.logger = logger
        self.max_volume = 57
        self.current_volume = -1

    def connection(self):
        return SerialConnection(serial_port=self.serial_port, logger=self.logger)

    def set_source(self, what_source):
        with self.connection() as conn:
            what_source = what_source.strip().upper()
            idx = SOURCES.index(what_source)
            if idx >= 0:
                self.source = conn.set_value("Source", SOURCES[idx])

    def calibrate_volume(self):
        with self.connection() as conn:
            for i in range(0,self.max_volume):
                conn.send_command("Volume-")
                self.current_volume = 0

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

    def set_volume_percent(self, percent):
        if self.current_volume<0:
            return -1
        new_volume = self.max_volume*(percent/100.)
        steps = int(round(round(new_volume) - self.current_volume))
        with self.connection() as conn:
            if steps!=0:
                command = "Volume+"
                if steps<0:
                    command = "Volume-"
                for step in range(0, abs(steps)):
                    conn.send_command(command)
                self.current_volume = new_volume
        return new_volume

    def volume_down(self):
        with self.connection() as conn:
            conn.send_command("Volume-")
            self.current_volume -= 1
    def volume_up(self):
        with self.connection() as conn:
            conn.send_command("Volume+")
            self.current_volume += 1

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
            'volume': self.current_volume,
            'volume_percent': (self.current_volume/float(self.max_volume)*100.),
            'source': self.source,
        })
        return data
