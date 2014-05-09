# coding=utf-8

from models import Device, DeviceWrongAction

from time import sleep

d1 = Device(name='device1', pin=14, action=Device.ACTION_SWITCH)
d2 = Device(name='device2', pin=15, action=Device.ACTION_PULSE)

d1.switch()
sleep(1)
d1.switch()
sleep(1)
d2.switch()
sleep(1)
d2.switch()


