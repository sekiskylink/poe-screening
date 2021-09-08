# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

import web
import re
from . import render
from . import csrf_protected, db, get_session, put_session
from app.tools.utils import auth_user, audit_log
from .tasks import (
    compose_tracked_entity_instance_payload,
    post_data_to_dhis2,
    get_tracked_entity_instance_reference)
from .celeryconfig import DHIS2_TEI_ENDPOINT


class Verify:
    def GET(self, verification_code):
        # params = web.input()

        res = db.query(
            "SELECT fields, tei, (created > now() - '24 hours'::interval OR "
            "updated > now() - '24 hours'::interval) AS valid "
            "FROM entries WHERE id = $id ",
            {'id': verification_code})
        if res:
            r = res[0]
            if r.valid:
                print("This is a valid verification %s" % r.fields)
                payload = compose_tracked_entity_instance_payload(r.fields, r.fields["portOfEntry"])
                print("PAYLOAD =>", payload)
                tei = r.tei
                if tei and re.match(r'[0-9a-zA-Z]{11}', tei):
                    url_suffix = "/{}".format(tei)
                else:
                    url_suffix = ""

                method = "PUT" if url_suffix else "POST"
                url = DHIS2_TEI_ENDPOINT
                if url_suffix:
                    url += url_suffix

                try:
                    resp = post_data_to_dhis2(url, payload, method=method)
                    reference = get_tracked_entity_instance_reference(resp.json())
                    print("+++++++", resp.json())
                    print(">>>>>>>>", reference)
                    if method == "POST":
                        db.query("UPDATE entries set tei = $tei WHERE id =$id", {'tei': reference, 'id': verification_code})
                    if not reference:
                        reference = url_suffix.replace("/", "")
                except Exception as e:
                    print("Trouble Submitting to DHIS 2: [URL:{0}][ERROR: {1}]".format(url, str(e)))
        l = locals()
        del l['self']
        return render.test(**l)

    def POST(self):
        l = locals()
        del l['self']
        return render.test(**l)
