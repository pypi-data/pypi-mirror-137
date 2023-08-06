# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
import os
import zipfile
import textwrap
import smtplib
import os.path as osp
from co2mpas_dice.server.db import DatabaseConnector
from co2mpas_dice.server.config import conf, _get_path
from email.message import EmailMessage


def render_template(fpath, **kwargs):
    from jinja2 import Template
    with open(osp.join(conf['dice']['mail_folder'], fpath)) as f:
        return Template(f.read()).render(**kwargs)


def _get_to(user):
    with DatabaseConnector() as conn:
        conn.cursor.execute(
            "SELECT company_id, mail FROM users WHERE id = %s LIMIT 1", (user,)
        )

        company, mail = conn.cursor.fetchone()
        to = {mail}
        if os.environ.get('DICE_TESTING') != 'True' and company > 0:
            conn.cursor.execute(
                "SELECT mail_to FROM companies WHERE id IN (-1, %s) LIMIT 2",
                (company,)
            )
            for mails, in conn.cursor.fetchall():
                to.update(m for m in (mails or '').split(',') if m)

        return to


def send_mail(to, subject, text, html, filename=None):
    if to and os.environ.get('DICE_MAIL_DISABLED') != 'True':
        mail, msg = conf['mail'], EmailMessage()
        msg.set_content(text)
        msg.add_alternative(html, subtype='html')
        msg['Subject'], msg['From'], msg['To'] = subject, mail['sender'], to

        if filename:
            with open(_get_path(filename, dir='attachment'), 'rb') as f:
                msg.add_attachment(
                    f.read(), maintype='application', subtype='zip',
                    filename=filename
                )

        SMTP = smtplib.SMTP_SSL if mail['ssl'] == 'True' else smtplib.SMTP

        with SMTP(mail['host'], int(mail['port'])) as s:
            if mail['password']:
                s.login(mail['user'], mail['password'])
            s.send_message(msg)


def _wrap_text(text):
    return '\n'.join(textwrap.wrap(str(text), 64))


def _wrap_table(table):
    return [tuple(map(_wrap_text, v)) for v in table]


def format_receipt(data, status_random, data_type):
    from .. import get_company_name, get_user_mail
    from tabulate import tabulate
    db = data['database']
    files = [(
        db['user'], db['uploaded_fname'], db['hash__ta_file'],
        db['hash__input_file'], db.get('hash__output_file'), db['hash__tot'],
        db.get('deviation__nedc_h'), db.get('deviation__nedc_l')
    )]
    if db['bifuel']:
        with DatabaseConnector() as conn:
            conn.cursor.execute(
                "SELECT user, uploaded_fname, hash__ta_file, "
                "hash__input_file, hash__output_file, hash__tot, "
                "deviation__nedc_h, deviation__nedc_l FROM dice "
                "WHERE valid = 1 AND vehicle_family_id = %s "
                "ORDER BY time_upload DESC LIMIT 1", (db['vehicle_family_id'],)
            )
            files.extend(conn.cursor)
    users = [v[0] for v in files]

    files = list(zip(*(
            [('Company Name', 'User Mail', 'Uploaded Filename',
              'Hash of *.%s.ta File' % data_type, 'Hash of *.input.xlsx File',
              'Hash of *.output.xlsx File',
              '%s Hash (i.e., *.%s.zip)' % (
                  data_type == 'co2mpas' and 'Correlation' or 'JET', data_type
              ),
              'Deviation NEDC-H', 'Deviation NEDC-L')] + [
                (get_company_name(v[0]), get_user_mail(v[0])) + v[1:-2] +
                tuple(x is None and '-' or ('%.2f %%' % x) for x in v[-2:])
                for v in files
            ]
    )))

    info = [
        ('Vehicle Family ID', db['vehicle_family_id']),
        ('Parent Vehicle Family ID', data['ta_id']['parent_vehicle_family_id']),
        ('WLTP Retest', db['wltp_retest']),
        ('Is Bi-fuel', db['bifuel']),
        ('Input type', db['input_type']),
        ('Is Extension', db['extension']),
        ('Is Incomplete Vehicle', db['incomplete']),
        ('Is Small Volume OEM', db['small_volume_oem']),
    ]

    rnd = data['random']
    keys = (
        'server_random', 'server_random_signature',
        'server_random_signature_hash', 'user_random', 'random'
    )
    deviations = list(zip(*([files[2]] + files[-2:])))
    if data_type == "jet":
        files, keys, deviations = files[:-4] + [files[-3]], keys[2:-1], None
    random = [
        (k.replace('_', ' ').replace('random', 'random number').title(), rnd[k])
        for k in keys
    ]
    tables = {k: _wrap_table(v) for k, v in dict(
        info=info, files=files, random=random
    ).items()}
    message = render_template(
        'message.rst', status_random=status_random, tabulate=tabulate, **tables
    )
    from co2mpas_dice.crypto import sign_data, get_RSA_keys
    signature, hash = sign_data(get_RSA_keys()['private']['server'], message)
    hash = db['hash__dice_receipt'] = hash.hex()
    file = render_template(
        'attachment.rst', hash=_wrap_text(hash), tabulate=tabulate,
        signature=_wrap_text(signature.hex()), message=message,
        server_pub_key=rnd['server_pub_key'], data_type=data_type
    )
    return file, users, deviations


def prepare_attachment(filename, receipt_id, data, status_random, data_type):
    receipt, users, deviations = format_receipt(data, status_random, data_type)

    fp = _get_path(filename, dir='attachment')
    os.makedirs(osp.dirname(fp), exist_ok=True)
    with zipfile.ZipFile(fp, 'w', zipfile.ZIP_DEFLATED) as zf:
        file, fn = '%s.dice' % receipt_id, 'verification.py'
        zf.writestr(file, receipt)
        zf.writestr(fn, render_template(fn, **locals()))
        zf.writestr('README.rst', render_template('README.rst', **locals()))

    return users, deviations


def prepare_mail(
        data, data_type, status_random=0, prev_valid=None, parent=None):
    from tabulate import tabulate
    from docutils.core import publish_string
    splitext = osp.splitext
    receipt_id, mail = splitext(data['database']['file'])[0], {}
    if status_random != 2:
        mail['filename'] = filename = '%s.zip' % receipt_id
        users, deviations = prepare_attachment(
            filename, receipt_id, data, status_random, data_type
        )
    else:
        deviations = None
        users = [data['database']['user']]
    rst = render_template('text.rst', **locals())
    mail.update(dict(
        to=','.join(sorted(set().union(*map(_get_to, users)))),
        subject=render_template('subject.txt', **locals()),
        text=rst,
        html=publish_string(rst, writer_name='html').decode()
    ))
    return mail, deviations
