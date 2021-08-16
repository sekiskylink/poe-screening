# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

import web
from . import render
from . import csrf_protected, db, get_session, put_session
from app.tools.utils import auth_user, audit_log


class Index:
    def GET(self):
        l = locals()
        del l['self']
        return render.login(**l)

    def POST(self):
        l = locals()
        del l['self']
        return render.login(**l)


class Logout:
    def GET(self):
        session = get_session()
        log_dict = {
            'logtype': 'Web', 'action': 'Logout', 'actor': session.username,
            'ip': web.ctx['ip'], 'descr': 'User %s logged out' % session.username,
            'user': session.sesid
        }
        audit_log(db, log_dict)
        session.kill()
        return web.seeother("/")
