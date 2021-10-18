# -*- coding: utf-8 -*-

"""Mako template options which are used, basically, by all handler modules in
controllers of the app.
"""

# from web.contrib.template import render_mako
import web
import json
import datetime
import settings
import gettext
import pyqrcode
from web.contrib.template import render_jinja
from settings import (absolute, config)

db_host = config['db_host']
db_name = config['db_name']
db_user = config['db_user']
db_passwd = config['db_passwd']
db_port = config['db_port']

db = web.database(
    dbn='postgres',
    user=db_user,
    pw=db_passwd,
    db=db_name,
    host=db_host,
    port=db_port
)

# i18n directory.
localedir = absolute('app') + '/i18n'

# Object used to store all translations.
allTranslations = web.storage()

SESSION = ''
APP = None

rs = db.query("SELECT id, name, alpha_2_code FROM countries")
ourCountries = []
for c in rs:
    ourCountries.append({'id': c['id'], 'name': c['name'], 'alpha_2_code': c['alpha_2_code']})


ports = db.query("SELECT id, name, dhis2_code FROM ports ORDER BY form_order, name")
ourPorts = []
for p in ports:
    ourPorts.append({'id': p['id'], 'name': p['name'], 'dhis2_code': p['dhis2_code']})

airports = db.query("SELECT id, name, country_code, iata_code FROM airports")
ourAirPorts = []
for a in airports:
    ourAirPorts.append({
        'id': a['id'], 'name': a['name'], 'country_code': a['country_code'],
        'iata_code': a['iata_code']})

def put_app(app):
    global APP
    APP = app


def get_app():
    global APP
    return APP


def get_session():
    global SESSION
    return SESSION


def datetimeformat(value, fmt='%Y-%m-%d'):
    if not value:
        return ''
    return value.strftime(fmt)


def datetimeformat2(value, fmt='%Y-%m-%d %H:%M'):
    if not value:
        return ''
    return value.strftime(fmt)

def renderQrCode(data):
    qrCodesImagesFolder = absolute('static/qrcodes')
    file_obj = tempfile.NamedTemporaryFile(delete=False, dir=qrCodesImagesFolder, suffix='.png')
    filename = file_obj.name
    print("File Name: ", filename)
    our_qrcode = pyqrcode.create(data, error='L', version=27, mode='binary')
    our_qrcode.png(filename, scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
    our_qrcode.show()
    return """
<div class="card card-success">
    <div class="card-header">
        <h3 class="card-title">Registration QR Code</h3>
    </div>
    <div class="card-body">
        <div class="row">
            <div class="col-md-12 col-lg-6 col-xl-4">
                <div class="card mb-2">
                    <img class="card-img-top" src="static/qrcodes/{0}" alt="QR Code">
                </div>
            </div>
        </div>
    </div>
</div>
""".format(filename)

Permissions = []

myFilters = {
    "renderQrCode": renderQrCode
}

# Jinja2 Template options
render = render_jinja(
    absolute('app/views'),
    encoding='utf-8'
)

def put_session(session):
    global SESSION
    SESSION = session
    render._lookup.globals.update(ses=session)


def get_translations(lang='en_US'):
    # Init translation.
    if 'lang' in allTranslations:
        translation = allTranslations[lang]
    elif lang is None:
        translation = gettext.NullTranslations()
    else:
        try:
            translation = gettext.translation(
                    'messages',
                    localedir,
                    languages=[lang],
                    )
        except IOError:
            translation = gettext.NullTranslations()
    return translation


def load_translations(lang):
    """Return the translations for the locale."""
    lang = str(lang)
    translation  = allTranslations.get(lang)
    if translation is None:
        translation = get_translations(lang)
        allTranslations[lang] = translation

        # Delete unused translations.
        try:
            for lk in allTranslations.keys():
                if lk != lang:
                    del allTranslations[lk]
        except:
            pass
    return translation


def custom_gettext(string):
    """Translate a given string to the language of the application."""
    ses = get_session()
    translation = load_translations(ses.get('lang'))
    if translation is None:
        return unicode(string)
    #return translation.ugettext(string)
    return translation.gettext(string)

def csrf_token():
    session = get_session()
    if 'csrf_token' not in session:
        from uuid import uuid4
        session.csrf_token = uuid4().hex
    return session.csrf_token


def csrf_protected(f):
    def decorated(*args, **kwargs):
        inp = web.input()
        session = get_session()
        if not ('csrf_token' in inp and inp.csrf_token == session.pop('csrf_token', None)):
            raise web.HTTPError(
                "400 Bad request",
                {'content-type': 'text/html'},
                """Cross-site request forgery (CSRF) attempt (or stale browser form).
<a href="/"></a>.""")  # Provide a link back to the form
        return f(*args, **kwargs)
    return decorated


def require_login(f):
    """usage
    @require_login
    def GET(self):
        ..."""
    def decorated(*args, **kwargs):
        session = get_session()
        if not session.loggedin:
            session.logon_err = "Please Logon"
            return web.seeother("/")
        else:
            session.logon_err = ""
        return f(*args, **kwargs)

    return decorated

render._lookup.globals.update(
    ses=get_session(), permissions=Permissions,
    year=datetime.datetime.now().strftime('%Y'),
    countries=ourCountries,
    ports=ourPorts,
    airports=ourAirPorts,
    _=custom_gettext,
)
render._lookup.filters.update(myFilters)


