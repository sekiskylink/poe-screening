# -*- coding: utf-8 -*-
import os
"""Default options for the application.
"""

config = {
    'db_name': 'poe',
    'db_host': 'localhost',
    'db_user': '',
    'db_passwd': '',
    'db_port': '5432',
}

# DHIS 2 Tracker Program Settings
DHIS2_TRACKER_PROGRAM_CONF = {
        'program': 'IMV1L4a09tc',
        'trackedEntityType': 'MCPQUTHX1Ze', # Person
        'attributes': {
            'arrivalOrDeparture': 'vbR9HyvLXWd',
            'name': 'sB1IHYu2xQT',
            'sex': 'FZzQbW8AWVd',  # Gender aka Sex
            'nationality': 'XvETY1aTxuB',
            'email': 'BJ6XIkuzk3J',
            'dateOfBirth': 'g4LJbkM0R24',
            'age': 'UezutfURtQG',
            # 'dateOfArival': '',
            'dateOfDeparture': 'szXspz3z0RA',
            'ugPhysicalAddress': 'ooK7aSiAaGq',
            'passportNumber': 'oUqWGeHjj5C', # Can be NIN
            'passportExpiryDate': 'rsFsoleZSHA',
            'flightOrVesselNumber': 'h6aZFN4DLcR',
            'seatNumber': 'XX8NZilra7b',
            'ugPhoneNumber': 'E7u9XdW24SP',
            'nextOfKin': 'j6sEr8EcULP',
            'countryOfResidence': 'hBcoBCZBWFb',
            'countryOfDeparture': 'cW0UPEANS5t',
            'travellingTo': 'pxcXhmjJeMv',
            'modeOfTransport': 'rBXloP7CJ9M',
            'purposeOfTrip': 'QIGSvZYCi4g',
            'freeFromSymptoms': 'EWWNozu6TVd',
            'dateOfLastCovidVaccination': 'hG66PSsqVkf',
            'beenCovidVaccinated': 'WypSLyCzzlH',
            'yellowFeverCardNumber': 'MbGcWAhHOPc',
            # 'embarkmentCountry': '',
            'ugPhysicalAddress': 'ooK7aSiAaGq',
            'durationOfStay': 'VpsljpwkXcD',
            'dateOfYellowFeverVaccination': 'ng1OlE99F97',
            # 'hasNegativePCRTest': '',
            'pcrTestedDate': 'HLVG1JirIs7'
        },
        'stages': {
            'travelLocator': {
                'uid': 'r7k02JBxge6',
                'dataelements': {
                    'timeAtCheckPoint': 'aN2fgA52IrU',
                    'nameOfCheckPoint': 'hcdSE7aTbQT',
                }
            },

        },
}

arrival_questions = {
    "portOfEntry": {
        "qn":"Port Of Departure",
        "col": 0,
        "row": 0,
    },
    "countryOfResidence":{
        "qn": "",
        "col": 2,
        "row": 0,
    },

    "name": {
        "qn":"Name of Traveller",
        "col": 0,
        "row": 1,
    },
    "nationality": {
        "qn": "Nationality",
        "col": 2,
        "row": 1,
    },

    "dateOfBirth": {
        "qn": "Date of Birth",
        "col": 0,
        "row": 2,
    },
    "age": {
        "qn": "Age",
        "col": 2,
        "row": 2,
    },

    "sex": {
        "qn": "Sex",
        "col": 0,
        "row": 3,
    },
    "email": {
        "qn": "Email",
        "col": 2,
        "row": 3,
    },

    "passportNumber": {
        "qn": "Passport Number/ National ID",
        "col": 0,
        "row": 4,
    },
    "passportExpiryDate": {
        "qn": "Passport Expiry Date",
        "col": 2,
        "row": 4,
    },

    "dateOfArival": {
        "qn": "Arrival Date",
        "col": 0,
        "row": 5,
    },
    "embarkmentCountry": {
        "qn": "Country of Embarkment",
        "col": 2,
        "row": 5,
    },

    "modeOfTransport": {
        "qn": "Mode of Transport",
        "col": 0,
        "row": 6,
    },
    "disembarkmentAirport": {
        "qn": "Airport of Disembarkment",
        "col": 2,
        "row": 6,
    },

    "flightOrVesselNumber": {
        "qn": "Flight / Vessel No.",
        "col": 0,
        "row": 7,
    },
    "purposeOfTrip": {
        "qn": "Purpose of Travel",
        "col": 2,
        "row": 7,
    },

    "durationOfStay": {
        "qn": "Physical Address While in Uganda",
        "col": 0,
        "row": 8,
    },
    "ugPhysicalAddress": {
        "qn": "Physical Address While in Uganda",
        "col": 2,
        "row": 8,
    },
    # "seatNumber": {
    #     "qn": "Seat Number",
    #     "col": 2,
    #     "row": 8,
    # },
    "phoneNumber": {
        "qn": "Phone Number",
        "col": 0,
        "row": 9,
    },
    "nextOfKin": {
        "qn": "Next of Kin",
        "col": 2,
        "row": 9,
    },
}

departure_questions = {
    "portOfEntry": {
        "qn":"Port Of Departure",
        "col": 0,
        "row": 0,
    },
    "countryOfResidence":{
        "qn": "Country of Residence",
        "col": 2,
        "row": 0,
    },
    "name": {
        "qn":"Name of Traveller",
        "col": 0,
        "row": 1,
    },
    "nationality": {
        "qn": "Nationality",
        "col": 2,
        "row": 1,
    },
    "dateOfBirth": {
        "qn": "Date of Birth",
        "col": 0,
        "row": 2,
    },
    "age": {
        "qn": "Age",
        "col": 2,
        "row": 2,
    },

    "sex": {
        "qn": "Sex",
        "col": 0,
        "row": 3,
    },
    "email": {
        "qn": "Email",
        "col": 2,
        "row": 3,
    },
    "passportNumber": {
        "qn": "Passport No/ NIN",
        "col": 0,
        "row": 4,
    },
    "passportExpiryDate": {
        "qn": "Passport Expiry",
        "col": 2,
        "row": 4,
    },

    "dateOfDeparture": {
        "qn": "Departure Date",
        "type": "",
        "col": 0,
        "row": 5,
    },
    "embarkmentCountry": {
        "qn": "Departure Country",
        "col": 2,
        "row": 5,
    },

    "travellingTo": {
        "qn": "Destination",
        "col": 0,
        "row": 6,
    },
     "modeOfTransport": {
        "qn": "Mode of Transport",
        "col": 2,
        "row": 6,
    },

    "embarkmentAirport": {
        "qn": "Airport",
        "col": 0,
        "row": 7,
    },
    "flightOrVesselNumber": {
        "qn": "Flight / Vessel No.",
        "col": 2,
        "row": 7,
    },
    # "seatNumber": {
    #     "qn": "Seat Number",
    #     "col": 0,
    #     "row": 8,
    # },
     "ugPhysicalAddress": {
        "qn": "Physical Address",
        "col": 0,
        "row": 8,
    },
    "phoneNumber": {
        "qn": "Phone Number",
        "col": 2,
        "row": 8,
    },
    "nextOfKin": {
        "qn": "Next of Kin",
        "col": 0,
        "row": 9,
    },
    "purposeOfTrip": {
        "qn": "Purpose of Travel",
        "col": 2,
        "row": 9,
    },
    # "freeFromSymptoms": {
    #     "qn": "Free from Symptoms",
    #     "col": 0,
    #     "row": 10,
    # },

}

health_questions = {
    "hasFever":{
        "qn": "Fever",
        "col": 0,
        "row": 0,
    },
    "hasHeadache":{
        "qn": "Headache",
        "col": 0,
        "row": 1,
    },
    "hasCough":{
        "qn": "Cough",
        "col": 0,
        "row": 2,
    },
    "hasSoreThroat":{
        "qn": "Sore Throat",
        "col": 0,
        "row": 3,
    },
    "hasFatigue":{
        "qn": "General body weakness",
        "col": 0,
        "row": 4,
    },
    "hasBreathingDifficulty":{
        "qn": "Difficulty in breathing",
        "col": 0,
        "row": 5,
    },
    "hasDiarrhoea":{
        "qn": "Diarrhoea",
        "col": 2,
        "row": 0,
    },
    "vomits":{
        "qn": "Vomiting",
        "col": 2,
        "row": 1,
    },
    "hasBloodInCoughOrStool":{
        "qn": "Blood in cough or stool or vomitus",
        "col": 2,
        "row": 2,
    },
    "hasAbdominalPain":{
        "qn": "Abdominal pain",
        "col": 2,
        "row": 3,
    },
    "hasSkinRash":{
        "qn": "Skin rash",
        "col": 2,
        "row": 4,
    },
    "bleedsFromBodyParts":{
        "qn": "Bleeding from body parts",
        "col": 2,
        "row": 5,
    },
}

last21days_questions = {
    "districtsVisited":{
        "qn": "Districts visited in Uganda",
        "col": 0,
        "row": 0,
    },
    "hasLivedInSameHousehold":{
        "qn": "Lived in the same household with a sick person",
        "col": 2,
        "row": 0,
    },
    "wasExposedToBlood":{
        "qn": "Exposed to blood or body fluids",
        "col": 0,
        "row": 1,
    },
    "hasSpentTimeInSameRoom":{
        "qn": "Spent time in the same room with a sick person",
        "col": 2,
        "row": 1,
    },

    "providedCare":{
        "qn": "Provided direct care the sick or died of unknown illness?",
        "col": 0,
        "row": 2,
    },
    "beenStuck":{
        "qn": "Exposed to sharp objects or body fluid of a sick person",
        "col": 2,
        "row": 2,
    },

    "hasWorkedInLab":{
        "qn": "Worked in a human or animal laboratory?",
        "col": 0,
        "row": 3,
    },
    "wasInterviewdAsContact":{
        "qn": "Identified or interviewed as a contact investigation of an ill person?",
        "col": 2,
        "row": 3,
    },
    "hasHandledTheDead":{
        "qn": "Participate in funeral or burial rites?",
        "col": 0,
        "row": 4,
    },
    # "beenCovidVaccinated": {
    #     "qn": "COVID 19 Vaccinated",
    #     "col": 2,
    #     "row": 4
    # },
}

pdf_sections = [
    {"details": {}, "title": "Travel Details", "display": True, "max_rows": 9, "max_cols": 3},
    {"details": health_questions, "title": "Health", "display": True, "max_rows": 5, "max_cols": 3},
    {"details": last21days_questions, "title": "In the last 21 days", "display": True, "max_rows": 4, "max_cols": 3},
    # {"details": {}, "title": "COVID19", "display": True, "max_rows": 1, "max_cols": 3},
    # {"details": {}, "title": "Yellow Fever", "display": True, "max_rows": 1, "max_cols": 3},
]

BROKER_URL = 'redis://localhost:6379/5'
APP_LINK = 'https://poe-screening.health.go.ug'

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = ''
SMTP_PASSWORD = ''
SMTP_STARTTLS = True
DEFAULT_FROM_EMAIL = ''

DHIS2_USERNAME = 'admin'
DHIS2_PASSWORD = 'district'
DHIS2_TEI_ENDPOINT = 'https://ugandaeidsr.org/api/trackedEntityInstances'
DHIS2_EVENTS_ENDPOINT = 'https://ugandaeidsr.org/api/events'

try:
    from .local_celeryconfig import *
except ImportError:
    pass
