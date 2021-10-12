# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

import web
from . import render
from . import csrf_protected, db, get_session, put_session
from app.tools.utils import auth_user, audit_log


class Registration:
    def GET(self):
        ses = get_session()
        params = web.input(ed="",d_id="")
        lang = params.get('lang', 'en_US')
        ses.lang = lang
        put_session(ses)

        l = locals()
        del l['self']
        return render.registration(**l)

    def POST(self):
        params = web.input(
            name="", nationality="", portOfEntry="", dateOfArrival="", dateOfDeparture="",
            age="", sex="", dateOfBirth="", passportNumber="", embarkmentAirport="",
            embarkmentCountry="", countryOfResidence="", countryOfDeparture="",
            flightOrVesselNumber="", seatNumber="", modeOfTransport="", purposeOfTrip="",
            ugPhysicalAddress="", durationOfStay="", PhoneNumber="", travellingTo="",
            disembarkmentAirport="", nextOfKin="", hasSymptoms="",
            beenCovidVaccinated="", dateOfLastCovidVaccination="", yellowFeverCardNumber="",
            hasNegativePCRTest="", dateOfYellowFeverVaccination="", ed="", d_id=""
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
                    'arrivalOrDeparture': params.arrivalOrDeparture,
                    'name': params.name,
                    'nationality': params.nationality,
                    'portOfEntry': params.portOfEntry,
                    'dateOfArrival': params.dateOfArrival,
                    'dateOfDeparture': params.dateOfDeparture,
                    'age': params.age,
                    'dateOfBirth': params.dateOfBirth,
                    'sex': params.sex,
                    'emai': params.email,
                    'passportNumber': params.passportNumber,
                    'passportExpiryDate': params.passportExpiryDate,
                    'embarkmentAirport': params.embarkmentAirport,
                    'embarkmentCountry': params.embarkmentCountry,
                    'disembarkmentAirport': params.disembarkmentAirport,
                    'flightOrVesselNumber': params.flightOrVesselNumber,
                    'seatNumber': params.seatNumber,
                    'modeOfTransport': params.modeOfTransport,
                    'countryOfResidence': params.countryOfResidence,
                    'countryOfDeparture': params.countryOfDeparture,
                    'travellingTo': params.travellingTo,
                    'ugPhysicalAddress': params.ugPhysicalAddress,
                    'durationOfStay': params.durationOfStay,
                    'purposeOfTrip': params.purposeOfTrip,
                    'PhoneNumber': params.ugPhoneNumber,
                    'nextOfKin': params.nextOfKin,
                    'hasSymptoms': params.hasSymptoms,
                    'beenCovidVaccinated': params.beenCovidVaccinated,
                    'dateOfLastCovidVaccination': params.dateOfLastCovidVaccination,
                    'hasNegativePCRTest': params.hasNegativePCRTest,
                    'yellowFeverCardNumber': params.yellowFeverCardNumber,
                    'dateOfYellowFeverVaccination': params.dateOfYellowFeverVaccination
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
        return render.registration(**l)
