# coding=utf-8

from bottle import Bottle, run, static_file, request, template
from settings import devices, server_params

app = Bottle()

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