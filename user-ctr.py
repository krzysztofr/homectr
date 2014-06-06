# coding=utf-8

# user control script

import argparse
import sqlite3
import smtplib
from email.mime.text import MIMEText

import settings

from utils import DbSession
from models import Session


def send_session_id(email, session_id):
    print 'Sending registration e-mail to %s... ' % email,
    s = smtplib.SMTP(settings.smtp['host'])
    s.login(settings.smtp['user'], settings.smtp['pass'])

    msg = MIMEText("Register your session to homectr at: %s/register_session/%s" % (settings.app_address, session_id))
    msg['Subject'] = "homectr session register"
    msg['From'] = settings.smtp['from']
    msg['To'] = email
    s.sendmail(settings.smtp['from'], [email], msg.as_string())
    s.quit()
    print 'OK'


def list_sessions(args):
    """Lists sessions in the database file."""

    with DbSession(args.file) as c:
        print "Sessions in the database %s:\n\nSESSION ID\tEMAIL (optional)\tCOMMENT (optional)" % args.file
        for session in c.execute('SELECT session_id, email, comment FROM sessions;'):
            print "%s\t%s\t%s" % session


def add_session(args):
    """Adds session to the database file."""

    if args.id is None:
        import uuid
        args.id = str(uuid.uuid4()).replace('-', '')

    with DbSession(args.file) as c:
        try:
            c.execute('INSERT INTO sessions (session_id, comment, email) VALUES (?, ?, ?)', (args.id, args.comment, args.email))

            print "Session %s added." % args.id

            if args.send and args.email is not None:
                send_session_id(args.email, args.id)

        except sqlite3.IntegrityError:
            print "Session with id %s already exists." % args.id


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

    Session.init_db_file(args.file)

    print "Database in file %s initialized." % args.file


argparser = argparse.ArgumentParser(description="homectr - user database manipulation")

subparsers = argparser.add_subparsers(help='available actions')

list_parser = subparsers.add_parser('list', help='List users')
list_parser.add_argument('--file', '-f', default=settings.session_db_file, action='store', help='database file')
list_parser.set_defaults(func=list_sessions)

add_parser = subparsers.add_parser('add', help='Add session id (generated randomly if not given)')
add_parser.add_argument('--id', '-i', action='store', help='session id (recommended: 32 characters)')
add_parser.add_argument('--email', '-e', action='store', help="email address")
add_parser.add_argument('--send', action='store_true', help="send session id to given e-mail")
add_parser.add_argument('--comment', '-c', action='store', help="comment to the session")
add_parser.add_argument('--file', '-f', default=settings.session_db_file, action='store', help='database file')
add_parser.set_defaults(func=add_session)

delete_parser = subparsers.add_parser('delete', help='Delete session id')
delete_parser.add_argument('session_id', action='store', help='session id to delete')
delete_parser.add_argument('--file', '-f', default=settings.session_db_file, action='store', help='database file')
delete_parser.set_defaults(func=delete_session)

init_parser = subparsers.add_parser('init', help='Init users database')
init_parser.add_argument('--file', '-f', default=settings.session_db_file, action='store', help='database file')
init_parser.set_defaults(func=init_db)

args = argparser.parse_args()
try:
    args = args.func(args)
except sqlite3.OperationalError:
    print 'No database file. Initialize it first.'




