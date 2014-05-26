# coding=utf-8

import datetime

from bottle import Bottle, run, static_file, request, template, response, redirect

from settings import devices_definitions, server_params, session_db_file, cookie_secret
from models import Device, DeviceWrongAction
from utils import DbSession

app = Bottle()

devices = {}

for d in devices_definitions:
    devices[d['pin']] = Device(name=d['name'], pin=d['pin'], action=d['action'])


@app.route('/')
def index():
    session_id = request.get_cookie('session_id', secret=cookie_secret)
    if session_id is None:
        response.status = 403
        return 'Missing session_id.'
    with DbSession(session_db_file) as c:
        result = c.execute('SELECT session_id FROM sessions WHERE session_id = ?;', (session_id,)).fetchone()
        if result is None:
            response.status = 403
            return 'Wrong session_id.'
    return template('public/index.html', devices=devices)

@app.route('/switch')
def switch_device():
    session_id = request.get_cookie('session_id', secret=cookie_secret)
    if session_id is None:
        response.status = 403
        return 'Missing session_id.'
    with DbSession(session_db_file) as c:
        result = c.execute('SELECT session_id FROM sessions WHERE session_id = ?;', (session_id,)).fetchone()
        if result is None:
            response.status = 403
            return 'Wrong session_id.'
    pin = int(request.query.pin)
    devices[pin].switch()
    return "OK"

@app.route('/register_session/<session_id>')
def register_session(session_id):
    with DbSession(session_db_file) as c:
        result = c.execute('SELECT session_id, email, comment FROM sessions WHERE session_id = ?;', (session_id,)).fetchone()
        if result is None:
            response.status = 403
            return 'Wrong session_id.'
        else:
            response.set_cookie('session_id', session_id, expires=datetime.datetime.now() + datetime.timedelta(days=365), path="/", secret=cookie_secret)
            redirect('/')




@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./public')

run(app, host=server_params['host'], port=server_params['port'])