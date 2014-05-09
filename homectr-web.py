# coding=utf-8

from bottle import Bottle, run, static_file

app = Bottle()

@app.route('/')
def index():
    return static_file('index.html', root='./public')

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./public')

run(app, host='localhost', port=8080)