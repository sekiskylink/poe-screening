# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

import web
import simplejson
import tempfile
import psycopg2.extras
from . import render
from . import csrf_protected, db, get_session, put_session
from app.tools.utils import auth_user, audit_log


class Registration:
    def GET(self):
        ses = get_session()
        params = web.input(ed="",d_id="")
        lang = params.get('lang', 'en_US')
        ses.lang = lang
        districts_1 = db.query("SELECT id, name, dhis2_code FROM orgunits WHERE dhis2_level = 3")
        # if lang == 'fr':
        #     update_icon('flag-icon-fr')
        # elif lang == 'cn':
        #     update_icon('flag-icon-cn')
        # elif lang == 'tz':
        #     update_icon('flag-icon-tz')
        # else:
        #     update_icon('flag-icon-us')
        put_session(ses)
        print("LANGUAGE++++++++", lang)

        l = locals()
        del l['self']
        return render.registration2(**l)

    def POST(self):
        params = web.input(
            name="", nationality="", portOfEntry="", dateOfArrival="", dateOfDeparture="",
            age="", sex="", dateOfBirth="", passportNumber="", embarkmentAirport="",
            embarkmentCountry="", countryOfResidence="", countryOfDeparture="",
            flightOrVesselNumber="", seatNumber="", modeOfTransport="", purposeOfTrip="",
            ugPhysicalAddress="", durationOfStay="", phoneNumber="", travellingTo="",
            disembarkmentAirport="", nextOfKin="", freeFromSymptoms="", pcrTestedDate="",
            beenCovidVaccinated="", dateOfLastCovidVaccination="", yellowFeverCardNumber="",
            hasNegativePCRTest="", dateOfYellowFeverVaccination="", ed="", d_id="",
            covidVaccinationCert={}, pcrTestCopy={},
            hasFever="", hasHeadache="", hasCough="", hasSoreThroat="", hasFatigue="",
            hasBreathingDifficulty="", hasDiarrhoea="", vomits="", hasBloodInCoughOrStool="",
            hasAbdominalPain="", hasSkinRash="", bleedsFromBodyParts="",
            districtsVisited="", wasExposedToBlood="", providedCare="", hasWorkedInLab="",
            hasHandledTheDead="", hasSpentTimeInSameRoom="", beenStuck="", wasInterviewdAsContact="",
            hasLivedInSameHousehold=""
        )

        allow_edit = False
        try:
            edit_val = int(params.ed)
            allow_edit = True
        except:
            pass
        freeFromSymptoms = "Yes"
        # qrcode_color = '#00ff66'
        qrcode_color = '#000000'
        color_code = "#3db489"
        if "Yes" in [
            params.hasFever, params.hasCough, params.hasDiarrhoea,params.hasFatigue,
            params.hasSkinRash, params.hasSoreThroat, params.bleedsFromBodyParts, params.vomits,
                params.hasSoreThroat]:
            color_code = '#ffcc00'
            freeFromSymptoms = "No"
        if "Yes" in [
            params.hasBloodInCoughOrStool, params.hasHandledTheDead,
            params.providedCare, params.hasWorkedInLab, params.wasInterviewdAsContact,
            params.wasExposedToBlood, params.beenStuck, params.hasAbdominalPain,
                params.hasLivedInSameHousehold]:
            freeFromSymptoms = "No"
            if color_code == '#ffcc00':
                color_code = '#ff0000'
            else:
                color_code = '#ffcc00'
            # qrcode_color = '#ff0000'
        ALLOWED_CTYPES = ['application/pdf', 'image/png', 'image/jpg', 'image/jpeg']
        # covid_cert_file_name = ""
        # pcr_test_file_name =""

        # covid_certificate_fp = params.covidVaccinationCert
        # covid_cert_ctype = getattr(covid_certificate_fp, 'type')

        # if covid_cert_ctype in ALLOWED_CTYPES:
        #     # proceed and save it
        #     suffix = covid_cert_ctype.split("/")[-1:][0]
        #     f = tempfile.NamedTemporaryFile(suffix=".{0}".format(suffix), delete=False)
        #     f.write(covid_certificate_fp.file.read())
        #     covid_cert_file_name = f.name
        #     f.close()

        # pcr_test_fp = params.pcrTestCopy
        # pcr_test_ctype = getattr(pcr_test_fp, 'type')

        # if pcr_test_ctype in ALLOWED_CTYPES:
        #     # save it some where on disk
        #     surffix = pcr_test_ctype.split("/")[-1:][0]
        #     f = tempfile.NamedTemporaryFile(suffix=".{0}".format(suffix), delete=False)
        #     f.write(pcr_test_fp.file.read())
        #     pcr_test_file_name = f.name
        #     f.close()

        # print("CERT File: {0}, PCR Test File: {1}".format(covid_cert_file_name, pcr_test_file_name))

        with db.transaction():
            if params.ed and allow_edit:
                pass
            else:
                # inserting
                # Do some server side validation
                #
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
                    'gender': params.sex,
                    'email': params.email,
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
                    'phoneNumber': params.phoneNumber.replace(' ', ''),
                    'nextOfKin': params.nextOfKin,
                    'freeFromSymptoms': freeFromSymptoms,
                    'beenCovidVaccinated': params.beenCovidVaccinated,
                    'dateOfLastCovidVaccination': params.dateOfLastCovidVaccination,
                    'hasNegativePCRTest': params.hasNegativePCRTest,
                    'pcrTestedDate': params.pcrTestedDate,
                    'yellowFeverCardNumber': params.yellowFeverCardNumber,
                    'dateOfYellowFeverVaccination': params.dateOfYellowFeverVaccination,
                    'districtsVisited': params.districtsVisited,
                    'wasExposedToBlood': params.wasExposedToBlood,
                    'providedCare': params.providedCare,
                    'hasWorkedInLab': params.hasWorkedInLab,
                    'hasHandledTheDead': params.hasHandledTheDead,
                    'hasLivedInSameHousehold': params.hasLivedInSameHousehold,
                    'hasSpentTimeInSameRoom': params.hasSpentTimeInSameRoom,
                    'beenStuck': params.beenStuck,
                    'wasInterviewdAsContact': params.wasInterviewdAsContact,
                    # symptoms
                    'hasFever': params.hasFever,
                    'hasCough': params.hasCough,
                    'hasBreathingDifficulty': params.hasBreathingDifficulty,
                    'hasFatigue': params.hasFatigue,
                    'hasSoreThroat': params.hasSoreThroat,
                    'hasHeadache': params.hasHeadache,
                    'hasBloodInCoughOrStool': params.hasBloodInCoughOrStool,
                    'hasSkinRash': params.hasSkinRash,
                    'bleedsFromBodyParts': params.bleedsFromBodyParts,
                    'vomits': params.vomits,
                    'hasAbdominalPain': params.hasAbdominalPain,
                    'hasDiarrhoea': params.hasDiarrhoea,
                    'colorCode': color_code
                }
                # if covid_cert_file_name:
                #     fields['covidVaccinationCertFile'] = covid_cert_file_name
                # if pcr_test_file_name:
                #     fields['pcrTestFile'] = pcr_test_file_name

                res = db.query(
                    "INSERT INTO entries (fields) VALUES ($fields) RETURNING id",
                    {'fields': psycopg2.extras.Json(fields, dumps=simplejson.dumps)}
                )
                if res:
                    r = res[0]
                    saved_record = "%s" % r.id
                    print("Record saved")
                    return render.qrcode({'saved_record': saved_record, 'qrcode_color': qrcode_color})
        l = locals()
        del l['self']
        return render.registration2(**l)
