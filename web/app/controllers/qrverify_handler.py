# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

import web
import re
import psycopg2.extras
import simplejson
from . import render
from . import csrf_protected, db, get_session, put_session
from app.tools.utils import auth_user, audit_log
from .tasks import (
    compose_tracked_entity_instance_payload,
    post_data_to_dhis2,
    get_tracked_entity_instance_reference)
from .celeryconfig import DHIS2_TEI_ENDPOINT


def auth_entry(db, pin, entry_id):
    sql = (
        "SELECT id  FROM ports "
        "WHERE dhis2_code = (SELECT fields->>'portOfEntry' FROM entries WHERE "
        " id = $entry_id) AND pin = crypt($pin, pin)")
    res = db.query(sql, {'pin': pin, 'entry_id': entry_id})
    if not res:
        return False, "Wrong pin for Entry"
    else:
        return True, res[0]


class QRVerify:
    def GET(self, verification_code):
        params = web.input()
        ses = get_session()
        lang = params.get('lang', 'en_US')
        ses.lang = lang
        put_session(ses)
        verification_code = verification_code
        res = db.query("SELECT fields->>'colorCode' AS color_code FROM entries WHERE id = $id", {
            'id': verification_code
        })
        color_code = '#000000'
        if res:
            color_code = res[0]['color_code']

        l = locals()
        del l['self']
        return render.qrcode_verify(**l)

    def POST(self, verification_code):
        params = web.input(qrcode_value="", pin="")
        print("PIN:", params.pin, " RECORD ID:", params.qrcode_value)
        authenticated, _ = auth_entry(db, params.pin, params.qrcode_value)
        if authenticated:
            web.seeother("/verify/" + params.qrcode_value)
        l = locals()
        del l['self']
        web.seeother("/qr-verify/" + verification_code)
        # return render.test(**l)
