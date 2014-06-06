# coding=utf-8

from time import sleep

from gpio_wrapper import gpio_commands

from utils import DbSession


class DeviceWrongAction(Exception):
    pass


class Device:

    ACTION_SWITCH = 1
    ACTION_PULSE = 2

    def __init__(self, name, pin, action):
        self.name = name
        self.pin = pin
        if action not in (Device.ACTION_PULSE, Device.ACTION_SWITCH):
            raise DeviceWrongAction("Wrong action selected")
        self.action = action
        self.status = False
        gpio_commands.mode(pin=self.pin, mode='out')
        gpio_commands.write(pin=self.pin, value=0)

    def switch(self):
        if self.action == Device.ACTION_SWITCH:
            self.status = not self.status
            gpio_commands.write(pin=self.pin, value=int(self.status))
        elif self.action == Device.ACTION_PULSE:
            gpio_commands.write(pin=self.pin, value=1)
            sleep(.1)
            gpio_commands.write(pin=self.pin, value=0)


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
    def new(id, email='', comment=''):
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
