# coding=utf-8

from bottle import Bottle, run, static_file, request, template

from settings import devices_definitions, server_params
from models import Device, DeviceWrongAction

app = Bottle()

devices = {}

for d in devices_definitions:
    devices[d['pin']] = Device(name=d['name'], pin=d['pin'], action=d['action'])


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

run(app, host=server_params['host'], port=server_params['port'])