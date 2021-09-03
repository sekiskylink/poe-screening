# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

import web
import json
import simplejson
import psycopg2.extras
from . import render
from . import csrf_protected, db, get_session, put_session
from app.tools.utils import auth_user, audit_log


class Poe:
    def GET(self):
        ses = get_session()
        params = web.input(ed="",d_id="")
        lang = params.get('lang', 'en_US')
        ses.lang = lang
        put_session(ses)
        countries_1 = db.query("SELECT id, name FROM countries")
        countries_2 = db.query("SELECT id, name FROM countries")
        countries_3 = db.query("SELECT id, name FROM countries")
        countries_4 = db.query("SELECT id, name FROM countries")

        ports = db.query("SELECT id, name, dhis2_code FROM ports")
        airports = db.query("SELECT id, name, country_code, iata_code FROM airports")
        l = locals()
        del l['self']
        return render.poe2(**l)

    def POST(self):
        params = web.input(
            name="", nationality="", portOfEntry="", dateOfArrival="",
            age="", gender="", passportNumber="", embarkmentAirport="",
            embarkmentCountry="", flightOrVesselNumber="", countriesVisited=[],
            ugPhysicalAddress="", durationOfStay="", ugPhoneNumber="",
            nextOfKin="", beenToChina="", beenToAffectedCountries="",
            affectedCountriesVisited=[], hasFever="", hasHeadache="",
            hasCough="", hasSoreThroat="", hasFatigue="", hasBreathingDifficulty="",
            hasDiarrhoea="", vomits="", hasBloodInCoughOrStool="",
            hasAbdominalPain="", hasSkinRash="", bleedsFromBodyParts="",
            beenToEbolaAffectedCountry="",  yellowFeverVaccinationCert="", ed="", d_id=""
        )

        allow_edit = False
        try:
            edit_val = int(params.ed)
            allow_edit = True
        except:
            pass

        with db.transaction():
            if params.ed and allow_edit:
                pass
            else:
                # inserting
                fields = {
                    'name':params.name,
                    'nationality':params.nationality,
                    'portOfEntry':params.portOfEntry,
                    'dateOfArrival':params.dateOfArrival,
                    'age':params.age,
                    'gender':params.gender,
                    'passportNumber':params.passportNumber,
                    'embarkmentAirport':params.embarkmentAirport,
                    'embarkmentCountry':params.embarkmentCountry,
                    'flightOrVesselNumber':params.flightOrVesselNumber,
                    'countriesVisited':params.countriesVisited,
                    'ugPhysicalAddress':params.ugPhysicalAddress,
                    'durationOfStay':params.durationOfStay,
                    'ugPhoneNumber':params.ugPhoneNumber,
                    'beenToChina':params.beenToChina,
                    'beenToAffectedCountries':params.beenToAffectedCountries,
                    'affectedCountriesVisited':params.affectedCountriesVisited,
                    'hasFever':params.hasFever,
                    'hasHeadache':params.hasHeadache,
                    'hasCough':params.hasCough,
                    'hasSoreThroat':params.hasSoreThroat,
                    'hasFatigue':params.hasFatigue,
                    'hasBreathingDifficulty':params.hasBreathingDifficulty,
                    'hasDiarrhoea':params.hasDiarrhoea,
                    'vomits':params.vomits,
                    'hasBloodInCoughOrStool':params.hasBloodInCoughOrStool,
                    'hasAbdominalPain':params.hasAbdominalPain,
                    'hasSkinRash':params.hasSkinRash,
                    'bleedsFromBodyParts':params.bleedsFromBodyParts,
                    'beenToEbolaAffectedCountry':params.beenToEbolaAffectedCountry,
                    'yellowFeverVaccinationCert': params.yellowFeverVaccinationCert,
                }
                res = db.query(
                    "INSERT INTO entries (fields) VALUES ($fields) RETURNING id",
                    {'fields': psycopg2.extras.Json(fields, dumps=simplejson.dumps)}
                )
                if res:
                    r = res[0]
                    saved_record = "%s" % r.id
                    print("Record saved")
        l = locals()
        del l['self']
        return render.qrcode(**l)
