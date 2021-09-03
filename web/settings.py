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
        'program': 'nBWFG3fYC8N',
        'trackedEntityType': 'KWN8FUfvO5G', # Person
        'attributes': {
            'name': 'v38k0KDP9mE',
            'formId': 'yRfqBeCakkf',
            'printTravelPass': 'u2rh74FGZeN',
            'SystemId': 'n1XopDm7mCV',
            'gender': 'pRpGsL1IVfG',  # Gender aka Sex
            'nationality': 'xyqt7jx4hFT',
            'dateOfBirth': 'SpsFJYxJ5W8',
            'dateOfArival': 'uMGXozzQaOi',
            'PassportNumber': 'AuhPUybQMOf', # Can be NIN
            'flightOrVesselNumber': 'K1SjKeVnzHc',
            'seatNumber': 'tokcH3iFDCZ',
            'ugPhoneNumber': 'hb86PiUnfPN',
            'freeFromSymptoms': 'pIQpL7Ie1ow',
            'embarkmentCountry': 'c8uVQ8EIwES',
            'ugPhysicalAddress': 'pa2k9W1c6zC',
            'durationOfStay': 'VpsljpwkXcD',
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
    from local_settings import *
except ImportError:
    pass
