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
        'program': 'nBWFG3fYC8N',
        'trackedEntityType': 'KWN8FUfvO5G', # Person
        'attributes': {
            'name': 'sB1IHYu2xQT',
            'formId': 'PVXhTjVdB92',
            'printTravelPass': 'Mnx6lj6roDz',
            'SystemId': 'CLzIR1Ye97b',
            'gender': 'Rq4qM2wKYFL',  # Gender aka Sex
            'nationality': 'XvETY1aTxuB',
            'dateOfBirth': 'g4LJbkM0R24',
            'dateOfArival': 'UJiu0P8GvHt',
            'PassportNumber': 'oUqWGeHjj5C', # Can be NIN
            'flightOrVesselNumber': 'h6aZFN4DLcR',
            'seatNumber': 'XX8NZilra7b',
            'ugPhoneNumber': 'E7u9XdW24SP',
            'freeFromSymptoms': 'EWWNozu6TVd',
            'embarkmentCountry': 'cW0UPEANS5t',
            'ugPhysicalAddress': 'ooK7aSiAaGq',
            'durationOfStay': 'eH7YTWgoHgo',
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
DHIS2_TEI_ENDPOINT = 'http://localhost:8080/api/trackedEntityInstances'
DHIS2_EVENTS_ENDPOINT = 'http://localhost:8080/api/events'

try:
    from .local_celeryconfig import *
except ImportError:
    pass
