# coding=utf-8

# user control script

import argparse
import sqlite3


class DbSession:
    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.conn.commit()


def list_sessions(args):
    """Lists sessions in the database file."""

    with DbSession(args.file) as c:
        print "Sessions in the database %s:\n\nSESSION ID\tCOMMENT (optional)" % args.file
        for session in c.execute('SELECT session_id, comment FROM sessions;'):
            print "%s\t%s" % session


def add_session(args):
    """Adds session to the database file."""

    # FIXME: it's ugly right now, wrap it in the 'with' statement - #5

    with DbSession(args.file) as c:
        try:
            c.execute('INSERT INTO sessions (session_id, comment) VALUES (?, ?)', (args.session_id, args.comment))

            print "Session %s added." % args.session_id
        except sqlite3.IntegrityError:
            print "Session with id %s already exists." % args.session_id


def delete_session(args):
    """Deletes session from the database file."""

    with DbSession(args.file) as c:
        c.execute('DELETE FROM sessions WHERE session_id = ?', (args.session_id,))
        if c.rowcount == 0:
            print 'No such session %s.' % args.session_id
        else:
            print 'Session id %s deleted.' % args.session_id


def init_db(args):
    """Initialises database file."""

    with DbSession(args.file) as c:
        c.execute("CREATE TABLE IF NOT EXISTS [sessions] ([session_id] VARCHAR PRIMARY KEY NOT NULL UNIQUE, [comment] VARCHAR);")

    print "Database in file %s initialized." % args.file


argparser = argparse.ArgumentParser(description="homectr - user database manipulation")

subparsers = argparser.add_subparsers(help='available actions')

list_parser = subparsers.add_parser('list', help='List users')
list_parser.add_argument('--file', '-f', default='./users.db', action='store', help='database file')
list_parser.set_defaults(func=list_sessions)

add_parser = subparsers.add_parser('add', help='Add session id')
add_parser.add_argument('session_id', action='store', help='session id (recommended: 32 characters)')
add_parser.add_argument('--comment', '-c', action='store', help="comment to the session")
add_parser.add_argument('--file', '-f', default='./users.db', action='store', help='database file')
add_parser.set_defaults(func=add_session)

delete_parser = subparsers.add_parser('delete', help='Delete session id')
delete_parser.add_argument('session_id', action='store', help='session id to delete')
delete_parser.add_argument('--file', '-f', default='./users.db', action='store', help='database file')
delete_parser.set_defaults(func=delete_session)

init_parser = subparsers.add_parser('init', help='Init users database')
init_parser.add_argument('--file', '-f', default='./users.db', action='store', help='database file')
init_parser.set_defaults(func=init_db)

args = argparser.parse_args()
try:
    args = args.func(args)
except sqlite3.OperationalError:
    print 'No database file. Initialize it first.'




