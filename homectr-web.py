# coding=utf-8

from bottle import Bottle, run, static_file, request
from models import Device, DeviceWrongAction

app = Bottle()

device = {}
device[14] = Device(name='device1', pin=14, action=Device.ACTION_SWITCH)
device[15] = Device(name='device2', pin=15, action=Device.ACTION_SWITCH)
device[18] = Device(name='device3', pin=18, action=Device.ACTION_PULSE)

@app.route('/')
def index():
    return static_file('index.html', root='./public')

@app.route('/switch')
def switch_device():
    pin = int(request.query.pin)
    device[pin].switch()
    return "OK"


@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./public')

run(app, host='0.0.0.0', port=8080)