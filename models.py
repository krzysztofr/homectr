# coding=utf-8

from time import sleep
from os import system

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
        system('gpio -g mode %d out' % self.pin)
        system('gpio -g write %d 0' % self.pin)

    def switch(self):
        if self.action == Device.ACTION_SWITCH:
            self.status = not self.status
            system('gpio -g write %d %d' % (self.pin, int(self.status)))
        elif self.action == Device.ACTION_PULSE:
            system('gpio -g write %d %d' % (self.pin, 1))
            sleep(.1)
            system('gpio -g write %d %d' % (self.pin, 0))

