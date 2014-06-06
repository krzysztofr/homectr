# coding=utf-8

import sqlite3
from functools import wraps

from bottle import request, response


class DbSession:
    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.conn.commit()


def session_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from settings import cookie_secret, session_db_file
        session_id = request.get_cookie('session_id', secret=cookie_secret)
        if session_id is None:
            response.status = 403
            return 'Missing session_id.'
        with DbSession(session_db_file) as c:
            result = c.execute('SELECT session_id FROM sessions WHERE session_id = ?;', (session_id,)).fetchone()
            if result is None:
                response.status = 403
                return 'Wrong session_id.'
        return func(*args, **kwargs)
    return wrapper