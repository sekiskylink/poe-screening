import json
import web
from . import db


class Entries:
    """Returns Children for a node """
    def GET(self):
        web.header("Content-Type", "application/json; charset=utf-8")
        ret = []
        rs = db.query(
            "SELECT fields FROM entries WHERE fields->>'portOfEntry' = 'YTr0VOD4rea'")
        if rs:
            for r in rs:
                ret.append(r['fields'])
        return json.dumps(ret)
