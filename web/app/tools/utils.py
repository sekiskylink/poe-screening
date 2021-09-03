import requests
import json
import web
import re
import base64
import phonenumbers
import simplejson
import datetime
import psycopg2.extras
import os
from settings import (
    config,
    DHIS2_TRACKER_PROGRAM_CONF as programConf,
    DHIS2_USERNAME,
    DHIS2_USERNAME)


def format_msisdn(msisdn=None):
    """ given a msisdn, return in E164 format """
    if not msisdn and len(msisdn) < 10:
        return None
    msisdn = msisdn.replace(' ', '')
    num = phonenumbers.parse(msisdn, getattr(config, 'country', 'UG'))
    is_valid = phonenumbers.is_valid_number(num)
    if not is_valid:
        return None
    return phonenumbers.format_number(
        num, phonenumbers.PhoneNumberFormat.E164)


def lit(**keywords):
    return keywords


def default(*args):
    p = [i for i in args if i or i == 0]
    if p.__len__():
        return p[0]
    if args.__len__():
        return args[args.__len__() - 1]
    return None


def auth_user(db, username, password):
    sql = (
        "SELECT a.id, a.firstname, a.lastname, b.name as role, a.districts "
        "FROM users a, user_roles b "
        "WHERE username = $username AND password = crypt($passwd, password) "
        "AND a.user_role = b.id AND is_active = 't'")
    res = db.query(sql, {'username': username, 'passwd': password})
    if not res:
        return False, "Wrong username or password"
    else:
        return True, res[0]


def audit_log(db, log_dict={}):
    sql = (
        "INSERT INTO audit_log (logtype, actor, action, remote_ip, detail, created_by) "
        " VALUES ($logtype, $actor, $action, $ip, $descr, $user) "
    )
    db.query(sql, log_dict)
    return None


def get_basic_auth_credentials():
    auth = web.ctx.env.get('HTTP_AUTHORIZATION')
    if not auth:
        return (None, None)
    auth = re.sub('^Basic ', '', auth)
    username, password = base64.decodestring(auth).split(':')
    return username, password


def post_data_to_dhis2(url, data, params={}, method="POST"):
    user_pass = '{0}:{1}'.format(DHIS2_USERNAME, DHIS2_PASSWORD)
    coded = base64.b64encode(user_pass.encode())
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + coded.decode()
    }
    if method == "PUT":
        payload = json.loads(data).pop('enrollments')
        response = requests.put(
            url, data=json.dumps(payload), headers=headers,
            verify=False, params=params
        )
    elif method == "GET":
        response = requests.get(url, headers=headers, verify=False)
    else:
        response = requests.post(
            url, data=data, headers=headers,
            verify=False, params=params
        )
    return response


def compose_tracked_entity_instance_payload(values, orgUnitId):
    payload = {
        'trackedEntityType': programConf['trackedEntityType'],
        'orgUnit': orgUnitId,
        'attributes': [],
        'enrollments': [{
            'orgUnit': orgUnitId,
            'program': programConf['program'],
            'enrollmentDate': datetime.datetime.now().strftime('%Y-%m-%d'),
            'incidentDate': datetime.datetime.now().strftime('%Y-%m-%d')
        }]

    }

    # values['firstname'] = ' '.join(values.get('name', '').split()[:1])
    # values['lastname'] = ' '.join(values.get('name', '').split()[1:])

    for k, v in values.items():
        if k in programConf.get('attributes'):
            payload['attributes'].append({
                'attribute': programConf['attributes'][k],
                'value': v
            })
    return json.dumps(payload)


def compose_event_payload_list(values, orgUnitId, trackedEntityInstance):
    """Returns a list of payloads for different stages in the program"""
    payload = {
        'program': programConf['program'],
        'orgUnit': orgUnitId,
        'trackedEntityInstance': trackedEntityInstance,
        'eventDate': datetime.datetime.now().strftime('%Y-%m-%d'),
        'status': 'COMPLETED',
        'completedDate': datetime.datetime.now().strftime('%Y-%m-%d'),
        'storedBy': DHIS2_USERNAME,
        'dataValues': []
    }
    programEventsPayloadList = []
    for stage, stageConf in programConf['stages'].items():
        stub = payload.copy()
        stub['programStage'] = stageConf['uid']
        for k, v in stageConf['dataelements'].items():
            if k in values:
                stub['dataValues'].append({'dataElement': v, 'value': values[k]})
        programEventsPayloadList.append(stub)

    return programEventsPayloadList


def get_tracked_entity_instance_reference(responseObj):
    """returns the reference i.e UID of trackedEntityInstance from DHIS2 response"""
    try:
        response = responseObj.get('response')
        if response:
            if response.get("importSummaries"):
                if len(response["importSummaries"]):
                    importSummary = response["importSummaries"][0]
                    reference = importSummary["reference"]
                    return reference
    except Exception as e:
        print(str(e))
    return ''


def get_tracked_entity_instance_details(responseObj):
    """returns demorgraphic details for a TEI from DHIS2 response"""
    try:
        resp = {}
        # orgUnit = responseObj.get("orgUnit", "")
        attributes = responseObj.get("attributes", [])
        for attr in attributes:
            if attr['attribute'] in programConf['attributes'].values():
                key = get_key(programConf['attributes'], attr['attribute'])
                resp[key] = attr['value']
        return resp

    except Exception as e:
        print(str(e))
    return None
