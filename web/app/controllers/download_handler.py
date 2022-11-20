# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

import web
import re
import os
import tempfile
import simplejson
from . import render
from . import csrf_protected, db, get_session, put_session, portsById as ports
from app.tools.utils import auth_user, audit_log
from .tasks import (
    _Q,
    _P ,
    MyDocTemplate,
    remove_file
)
from .celeryconfig import (
    APP_LINK,
    pdf_sections,
    arrival_questions,
    departure_questions,
)
# from .tasks import

# ReportLab imports
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm, cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame, Table, Image, PageBreak
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab_qrcode import QRCodeImage


class Download:
    def GET(self, entry_id):
        params = web.input()
        ses = get_session()
        lang = params.get('lang', 'en_US')
        ses.lang = lang
        put_session(ses)
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
        downloads_dir = os.getcwd() + "/static/downloads"
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

        f = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir=downloads_dir)
        file_name = f.name

        doc = MyDocTemplate(file_name)
        doc.multiBuild(story)
        # remove file after 60 seconds
        remove_file.s(file_name).apply_async(countdown=60, expires=120)
        return web.seeother("/static/downloads/{0}".format(os.path.basename(file_name)))

