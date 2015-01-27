# coding=utf-8

from time import sleep

from gpio_wrapper import gpio_commands

from utils import DbSession

import pickledb

import settings


class DeviceWrongAction(Exception):
    pass


class Device:

    ACTION_SWITCH = 1
    ACTION_PULSE = 2

    def __init__(self, name, pin, action, reset_state=True):
        self.name = name
        self.pin = pin
        if action not in (Device.ACTION_PULSE, Device.ACTION_SWITCH):
            raise DeviceWrongAction("Wrong action selected")
        self.action = action
        if reset_state:
            gpio_commands.mode(pin=self.pin, set_mode='out')
            gpio_commands.write(pin=self.pin, value=0)

            # We assume that the initial state is "off". It is impossible to read
            # actual state as well as the state can be interfered by the physical
            # buttons (in case of "PULSE" switches). I will deal with that later. (FIXME)
            self.write_state(state=0)

    def switch(self):
        if self.action == Device.ACTION_SWITCH:
            status = int(not self.read_state())
            gpio_commands.write(pin=self.pin, value=status)
            self.write_state(status)

        elif self.action == Device.ACTION_PULSE:
            gpio_commands.write(pin=self.pin, value=1)
            sleep(.1)
            gpio_commands.write(pin=self.pin, value=0)
            self.write_state(int(not self.read_state()))

    def read_state(self):
        db = pickledb.load(settings.state_db_file, False)
        state = db.get("state"+str(self.pin))
        return state

    def write_state(self, state):
        db = pickledb.load(settings.state_db_file, False)
        db.set("state"+str(self.pin), state)
        db.dump()
        return True


class Session:
    def __init__(self):
        raise NotImplementedError

    def send_email(self):
        # sends email with session information
        raise NotImplementedError

    def delete(self):
        # removes self
        raise NotImplementedError

    @staticmethod
    def new(session_id, email='', comment=''):
        # creates new session
        raise NotImplementedError

    @staticmethod
    def fetch_all():
        # returns iterable
        raise NotImplementedError

    @staticmethod
    def get(session_id):
        # returns session object of given id or None
        raise NotImplementedError



    @staticmethod
    def init_db_file(filename):
        with DbSession(filename) as c:
            c.execute("CREATE TABLE IF NOT EXISTS [sessions] ([session_id] VARCHAR PRIMARY KEY NOT NULL UNIQUE, [comment] VARCHAR, [email] VARCHAR);")
