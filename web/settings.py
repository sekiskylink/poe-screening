# -*- coding: utf-8 -*-
import os
"""Default options for the application.
"""

DEBUG = False

SESSION_TIMEOUT = 3600  # 1 Hour

HASH_KEY = ''
VALIDATE_KEY = ''
ENCRYPT_KEY = ''
SECRET_KEY = ''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# No of items to show on each page
PAGE_LIMIT = 25

def absolute(path):
    """Get the absolute path of the given file/folder.

    ``path``: File or folder.
    """
    import os
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(PROJECT_DIR, path))

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
        },
        'stages': {
            'travelLocator': {
                'uid': 'rOSOXE9BGXL',
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
    from local_settings import *
except ImportError:
    pass
