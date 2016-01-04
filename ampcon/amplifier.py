import os
import yaml
from nad_c356 import SerialConnection, SOURCES

__author__ = 'zeraien'

class InvalidCommandError(Exception):
    pass

class Command(object):
    def __init__(self, data):
        self.title = data['title']
        self.command_string = data['command']
        self.can_ask = data.get('can_ask', False)

    def run(self, connection):
        return self._perform_command(connection)

    def ask(self, connection):
        if self.can_ask:
            return connection.ask(what=self.command_string)
        else:
            raise InvalidCommandError("This command does not support asking.")

    def _perform_command(self, connection):
        return connection.send_command(self.command_string)

    def __repr__(self):
        return u"%s: %s" % (self.title, self.command_string)

class AskCommand(Command):
    pass

class Amplifier(object):

    def __init__(self, serial_port, logger):
        self.serial_port = serial_port
        self.configured = False
        self.logger = logger
        self.max_volume = 57
        self._current_volume = -1
        self._SPEAKERS = ['A', 'B']
        self.command_objects = []

    def load_commands(self):
        with open(os.path.join(os.path.dirname(__file__),"nad_c356.yaml")) as f:
            config = yaml.load(f)
            commands = config['commands']
            for command in commands:
                is_list = command.get('list')
                if is_list:
                    for item in command['items']:
                        c = Command(item)
                        self.command_objects.append(c)
                else:
                    c = Command(command)
                    self.command_objects.append(c)

        print(self.command_objects)


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
                self.update_current_volume_value(0, force=True)

    def mute_toggle(self):
        with self.connection() as conn:
            self.mute = conn.set_bool("Mute", not self.mute)

    def power_toggle(self):
        with self.connection() as conn:
            self.power = conn.set_bool("Power", not self.power)
        self.configure()

    def speaker_toggle(self, speaker):
        if speaker in self._SPEAKERS:
            with self.connection() as conn:
                self.speakers[speaker] = conn.set_bool("Speaker%s"%speaker, not self.speakers[speaker])

    def set_volume_percent(self, percent):
        if self._current_volume<0:
            return -1
        new_volume = self.max_volume*(percent/100.)
        steps = int(round(new_volume - self._current_volume))
        with self.connection() as conn:
            if steps!=0:
                command = "Volume+"
                if steps<0:
                    command = "Volume-"
                for step in range(0, abs(steps)):
                    conn.send_command(command)
                self.update_current_volume_value(new_volume)
        return new_volume

    def update_current_volume_value(self, new_value, force=False):
        if self._current_volume < 0 and not force:
            return self._current_volume
        # new_value = int(round(new_value))
        self._current_volume = new_value

        if self._current_volume < 0:
            self._current_volume = 0
        elif self._current_volume>self.max_volume:
            self._current_volume = self.max_volume
        return self._current_volume

    def volume_change(self, steps):
        if steps==0: return

        with self.connection() as conn:
            command = "Volume+"
            if steps<0:
                command = "Volume-"
            for i in range(0,abs(steps)):
                conn.send_command(command)
            self.update_current_volume_value(self._current_volume+steps)

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
            self.speakers = {}
            self.speakers['A'] = self.ask(conn, "SpeakerA")
            self.speakers['B'] = self.ask(conn, "SpeakerB")
            self.configured = True

    def json_ready(self):
        data = {}
        for source in SOURCES:
            source = source.lower()
            data['source_%s' % source] = (self.source == source)

        data.update({
            'mute': self.mute,
            'power': self.power,
            'is_volume_calibrated': self._current_volume>=0,
            'volume': self._current_volume,
            'volume_percent': int(round(self._current_volume/float(self.max_volume)*100.)),
            'source': self.source,
        })
        for key, status in self.speakers.items():
            data["speaker_%s"%key] = status
        return data
