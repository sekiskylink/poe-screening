# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

import web
from . import render
from . import csrf_protected, db, get_session, put_session
from app.tools.utils import auth_user, audit_log


class Verify:
    def GET(self, verification_code):
        # params = web.input()
        # db.query("SELECT fields FROM entries WHERE id = $id")
        l = locals()
        del l['self']
        return render.test(**l)

    def POST(self):
        l = locals()
        del l['self']
        return render.test(**l)
