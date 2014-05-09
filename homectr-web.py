# coding=utf-8

from bottle import Bottle, run, static_file, request
from models import Device, DeviceWrongAction

app = Bottle()

@app.route('/')
def index():
    return static_file('index.html', root='./public')

@app.route('/switch')
def hello():
    pin = int(request.query.pin)
    device = Device(name='device1', pin=pin, action=Device.ACTION_SWITCH)
    device.switch()
    return "OK"


@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./public')

run(app, host='localhost', port=8080)