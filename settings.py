# coding=utf-8

from models import Device, DeviceWrongAction

devices = {}
devices[14] = Device(name='device1', pin=14, action=Device.ACTION_SWITCH)
devices[15] = Device(name='device2', pin=15, action=Device.ACTION_SWITCH)
devices[18] = Device(name='device3', pin=18, action=Device.ACTION_PULSE)

server_params = {
    'host': '0.0.0.0',
    'port': 8080
}

