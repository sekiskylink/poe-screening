import requests
import json
import web
import re
import base64
import phonenumbers
import simplejson
import datetime
import os
import tempfile
from . import portsById
from celery import Celery
from .celeryconfig import (
    config,
    DHIS2_TRACKER_PROGRAM_CONF as programConf,
    DHIS2_USERNAME,
    DHIS2_PASSWORD,
    APP_LINK,
    pdf_sections,
    arrival_questions,
    departure_questions,
    DEFAULT_FROM_EMAIL,
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_STARTTLS,
    BROKER_URL
)

# ReportLab imports
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm, cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame, Table, Image, PageBreak
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab_qrcode import QRCodeImage


web.config.smtp_server = SMTP_SERVER
web.config.smtp_port = SMTP_PORT
web.config.smtp_username = SMTP_USERNAME
web.config.smtp_password = SMTP_PASSWORD
web.config.smtp_starttls = SMTP_STARTTLS

# celery -A app.controllers.tasks worker --loglevel=info
app = Celery("poe", broker=BROKER_URL)
# db = web.database(
#     dbn='postgres', db=config['db_name'], user=config['db_user'], pw=config['db_passwd'],
#     host=config['db_host'], port=config['db_port'])


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


def post_data_to_dhis2(url, data, params={}, method="POST"):
    user_pass = '{0}:{1}'.format(DHIS2_USERNAME, DHIS2_PASSWORD)
    coded = base64.b64encode(user_pass.encode())
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + coded.decode()
    }
    print("user:", DHIS2_USERNAME, "pass:", DHIS2_PASSWORD)
    if method == "PUT":
        payload = json.loads(data).pop('enrollments')
        response = requests.put(
            url, data=payload, headers=headers,
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

# Code for Generating PDF and emailing it Follows


class MyDocTemplate(BaseDocTemplate):
   def __init__(self, filename, **kw):
       self.allowSplitting = 0
       BaseDocTemplate.__init__(self, filename, **kw)
       template = PageTemplate('normal', [Frame(2.5*cm, 2.5*cm, 15*cm, 25*cm, id='F1', showBoundary=0)])
       self.addPageTemplates(template)


def _Q(text, size=8, spacer=0):
    return Paragraph(
        "<para spaceBefore={0}><font size='{1}' name='Courier'>{2}"
        "</font></para>".format(spacer, size, text))

def _P(text, size=8, spacer=0):
    color = "black"
    if text == "No":
        color = "black"
    elif text == "Yes":
        color = "red"
    return Paragraph(
        "<para spaceBefore={0}><font size='{1}' name='Courier' color={3}><b>{2}</b>"
        "</font></para>".format(spacer, size, text, color))


@app.task(name="generate_and_email_pdf")
def generate_and_email_pdf(entry_id, ports=portsById, db=None):
    print("Gona generate add email pdf for id:[{0}]".format(entry_id))
    db = web.database(
        dbn='postgres', db=config['db_name'], user=config['db_user'], pw=config['db_passwd'],
        host=config['db_host'], port=config['db_port'])

    rs = db.query("SELECT fields FROM entries WHERE id =$id", {'id': entry_id})
    fields = {}
    if rs:
        fields = rs[0]['fields']
        print(fields, "***")
    else:
        print("No record found with ID: [{0}]".format(entry_id))
        return
    styles = getSampleStyleSheet()
    styleH = styles['Heading2']

    story = []

    logo_path = os.getcwd() + "/static/dist/img/moh.png"
    I = Image(logo_path)
    I.drawHeight = 0.5 *inch * I.drawHeight / I.drawWidth
    I.drawWidth = 0.5 *inch

    qr = QRCodeImage(
        '{0}/qr-verify/{1}'.format(
            APP_LINK,
            entry_id),
        size=0.7 * inch, back_color='linen'
    )

    header = Table([[I, [
        Paragraph("Ministry of Health Uganda", style=styleH),
        Paragraph("<para align=center>Port Health</para>")], qr]], style=[
        # ('GRID', (0,0), (-1, -1), 0.1, colors.green),
        ('ALIGN', (0,0), (0, 0), 'LEFT'),
        ('VALIGN', (0,0), (0, 0), 'MIDDLE'),
        ('ALIGN', (1,0), (1, 0), 'CENTER'),
        ('VALIGN', (1,0), (1, 0), 'MIDDLE'),
        ('ALIGN', (2,0), (-1, -1), 'RIGHT'),
    ])
    header._argW[1] = 3 * inch

    story.append(header)

    if fields['arrivalOrDeparture'] == 'Departure':
        pdf_sections[0]['details'] = departure_questions
    else:
        pdf_sections[0]['details'] = arrival_questions
        pdf_sections[2]['display'] = False

    for section in pdf_sections:
        if section['display']:
            title = _P(section["title"], 9, 2 * mm)
            story.append(title)

            t_data = []
            max_i = section['max_cols']
            max_j = section['max_rows']
            questions_map = section['details']

            for i in range(max_j + 1):
                t_data.append(["" for x in range(max_i + 1)])
            for k in fields.keys():
                if k in questions_map:
                    row = questions_map[k]["row"]
                    col = questions_map[k]["col"]
                    # print(">", col, ">>", row, ">>>", k, ">>>>>>>>", questions_map[k]["qn"], ">>>>>", fields[k])
                    t_data[row][col] = _Q(questions_map[k]["qn"], 7.5)

                    if col == 0 and row == 0 and section["title"] == "Travel Details":
                        t_data[row][ col + 1 ] = _P(ports[fields[k]])
                    else:
                        t_data[row][ col + 1 ] = _P(fields[k])

            story.append(Table(
                t_data, style=[
                ('BOX', (0,0), (-1, -1), 0.4, colors.black),
                ('GRID', (0,0), (-1, -1), 0.1, colors.grey),
            ]))

    f = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    file_name = f.name

    doc = MyDocTemplate(file_name)
    doc.multiBuild(story)
    if fields['email']:
        web.sendmail(
            DEFAULT_FROM_EMAIL,
            fields['email'],
            'Travel Health Details -MoH UG: {0}'.format(fields['name']),
            "Dear {0},\nPlease see the attchment with your health travel document."
            "\n\nRegards,\n\nMinistry Of Health.".format(fields['name']),
            attachments=[file_name]
        )
    # try:
    #     db._ctx.db.close()
    # except:
    #     pass
    os.unlink(file_name)
