# coding=utf-8

from bottle import Bottle, run, static_file, request, template
from models import Device, DeviceWrongAction

app = Bottle()

devices = {}
devices[14] = Device(name='device1', pin=14, action=Device.ACTION_SWITCH)
devices[15] = Device(name='device2', pin=15, action=Device.ACTION_SWITCH)
devices[18] = Device(name='device3', pin=18, action=Device.ACTION_PULSE)

@app.route('/')
def index():
    return template('public/index.html', devices=devices)

@app.route('/switch')
def switch_device():
    pin = int(request.query.pin)
    devices[pin].switch()
    return "OK"


@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./public')

run(app, host='0.0.0.0', port=8080)