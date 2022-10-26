# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

import web
from . import render
from . import csrf_protected, db, get_session, put_session
from app.tools.utils import auth_user, audit_log


class Test:
    def GET(self):
        l = locals()
        del l['self']
        return render.preview(**l)

    def POST(self):
        l = locals()
        del l['self']
        return render.preview(**l)
