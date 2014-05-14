# coding=utf-8

# user control script

import argparse
import sqlite3

def get_cursor(filename):
    """Provides database cursor."""

    conn = sqlite3.connect(filename)
    return conn.cursor()

def list_sessions(args):
    """Lists sessions in the database file."""

    print "Sessions in the database %s:\n\nSESSION ID\tCOMMENT (optional)" % args.file
    for session in get_cursor(args.file).execute('SELECT session_id, comment FROM sessions;'):
        print "%s\t%s" % session


def add_session(args):
    """Adds session to the database file."""
    print 'add'

def delete_session(args):
    """Deletes session from the database file."""
    print 'delete'

def init_db(args):
    """Initialises database file."""

    get_cursor(args.file).execute("CREATE TABLE IF NOT EXISTS [sessions] ([session_id] VARCHAR PRIMARY KEY NOT NULL UNIQUE, [comment] VARCHAR);")

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
args = args.func(args)




