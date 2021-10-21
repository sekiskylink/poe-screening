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

DHIS2_USERNAME = 'admin'
DHIS2_PASSWORD = 'district'
DHIS2_TEI_ENDPOINT = 'https://ugandaeidsr.org/api/trackedEntityInstances'
DHIS2_EVENTS_ENDPOINT = 'https://ugandaeidsr.org/api/events'

try:
    from .local_celeryconfig import *
except ImportError:
    pass
