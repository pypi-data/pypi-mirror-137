#  -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
r"""
It contains DICE flask app.
"""
import os
import base64
import logging
import os.path as osp
import schedula as sh
from flask import Flask, jsonify, send_file, request, render_template
from co2mpas_dice.server.config import conf
from co2mpas_dice.err import DiceError

conf.read(os.environ.get('DICE_INI', ''))

app = Flask(
    __name__,
    static_folder=osp.abspath(conf['app']['static_folder']),
    template_folder=osp.abspath(conf['app']['template_folder'])
)
app.config['TEMPLATES_AUTO_RELOAD'] = True
log = logging.getLogger(__name__)


def safe_call(*args, **kwargs):
    from co2mpas_dice.server import dice
    try:
        res = {'data': dice(*args, **kwargs)}
    except sh.DispatcherError as ex:
        if isinstance(ex.args[2], DiceError):
            ex = ex.args[2]
            res = {'error': ex.args[0] % ex.args[1:]}
        else:
            raise ex
    return res


@app.template_global()
def template_include(filename):
    with open(osp.join(app.template_folder, filename), 'r') as f:
        return f.read()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def dice_index():
    return render_template('index.html', title='DICE back-end index')


@app.route('/sign_key', methods=['GET', 'POST'])
@app.route('/sign_key/<ecas_id>', methods=['GET', 'POST'])
def dice_sign_key(ecas_id=None):
    title = 'DICE - User Signature Key'
    return render_template('sign_key.html', title=title, ecas_id=ecas_id)


@app.route('/encrypt', methods=['GET', 'POST'])
def dice_encrypt():
    import json
    from co2mpas_dice import __version__, __jet_version__
    from co2mpas_dice.tar import load_data
    from co2mpas_dice.server import _get_path
    from co2mpas_dice.crypto import define_associated_data, load_RSA_keys
    keys_path = _get_path('dice.co2mpas.keys', dir='keys')
    kw = sh.map_dict({
        'secret/public.pem': 'secretPEM', 'server/public.pem': 'serverPEM'
    }, load_data(keys_path))
    kw['associatedDataHex'] = define_associated_data(load_RSA_keys(
        keys_path
    )['public']).hex()
    kw['__version__'] = __version__
    title = 'DICE - JRC Encryption Tool'
    response = render_template('encrypt.html', title=title, json=json, **kw)
    if request.args.get('download') != 'true':
        return response
    b64 = base64.b64encode(response.encode()).decode()
    return render_template(
        'download.html', uri=f'data:text/plain;base64,{b64}',
        fname=f'{title} - v{__jet_version__}.html', title=title + ' - Download'
    )


@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/<company_name>/<user_mail>', methods=['GET', 'POST'])
@app.route('/register/<company_name>/<user_mail>/<ecas_id>',
           methods=['GET', 'POST'])
def dice_register(company_name=None, user_mail=None, ecas_id=None):
    """
    Get the diced results for the given company.

    :param company_name:
        Company name.
    :type company_name: str

    :param user_mail:
        User mail.
    :type user_mail: str

    :param ecas_id:
        ECAS id.
    :type ecas_id: str

    :return:
         Data to be visualized to the user.
    :rtype: flask.Response
    """
    if company_name is None:
        company_name = request.args['company_name']
    if user_mail is None:
        user_mail = request.args['user_mail']
    if ecas_id is None:
        ecas_id = request.args.get('ecas_id')

    keys = ['ecas_id', 'company_name', 'user_mail', 'company', 'user']
    cxt = safe_call(
        inputs=dict(
            ecas_id=ecas_id, company_name=company_name, user_mail=user_mail
        ),
        outputs=keys,
        select_output_kw=dict(keys=keys)
    )

    if request.args.get('json') == 'true':
        return jsonify(cxt)
    title = 'DICE back-end register'
    return render_template('register.html', title=title, **cxt)


@app.route('/diced', methods=['GET', 'POST'])
@app.route('/diced/<ecas_id>', methods=['GET', 'POST'])
@app.route('/diced/<ecas_id>/<last_rows>', methods=['GET', 'POST'])
def dice_diced(ecas_id=None, last_rows=None):
    """
    Get the diced results for the given company.

    :param ecas_id:
        ECAS id.
    :type ecas_id: str

    :param last_rows:
        Number of database rows to extract.
    :type last_rows: int

    :return:
         Data to be visualized to the user.
    :rtype: flask.Response
    """
    if ecas_id is None:
        ecas_id = request.args['ecas_id']
    if last_rows is None:
        last_rows = request.args.get('last_rows', 25)

    keys = ['ecas_id', 'company_name', 'user_mail', 'diced']
    cxt = safe_call(
        inputs=dict(ecas_id=ecas_id, last_rows=last_rows), outputs=keys,
        select_output_kw=dict(keys=keys)
    )
    if request.args.get('json') == 'true':
        return jsonify(cxt)
    import pandas as pd
    pd.set_option('display.max_colwidth', 10000)
    title = 'DICE back-end diced'
    df = pd.DataFrame(**cxt['data']['diced'])
    df['random'][pd.isna(df['info__CO2MPAS_version'])] = ''
    return render_template('diced.html', title=title, df=df, **cxt)


@app.route('/new', methods=['GET', 'POST'])
@app.route('/new/<ecas_id>', methods=['GET', 'POST'])
def dice_new(ecas_id=None):
    """
    Open a new upload session and generate a new random number.

    :param ecas_id:
        ECAS id.
    :type ecas_id: str

    :return:
        Hash of the signature of the random number generated by the server and
        upload session id.
    :rtype: flask.Response
    """
    if ecas_id is None:
        ecas_id = request.args['ecas_id']
    keys = ['ecas_id', 'session', 'rand_hash']
    cxt = safe_call(
        inputs=dict(ecas_id=ecas_id), outputs=keys,
        select_output_kw=dict(keys=keys)
    )
    if request.args.get('json') == 'true':
        return jsonify(cxt)
    import pandas as pd
    pd.set_option('display.max_colwidth', 10000)
    return render_template('new.html', pd=pd, title='DICE back-end new', **cxt)


@app.route('/upload/<ecas_id>/<session>', methods=['POST'])
def dice_upload(ecas_id, session):
    """
    Upload the given file on the opened session id.

    :param ecas_id:
        ECAS id.
    :type ecas_id: str

    :param session:
        Session id.
    :type session: str

    :return:
         Data to be visualized to the user.
    :rtype: flask.Response
    """
    file = request.files['file']
    keys = ['ecas_id', 'session', 'rand_hash', 'tables', 'data_type']
    cxt = safe_call(
        inputs=dict(ecas_id=ecas_id, session=session, file=file),
        outputs=keys, select_output_kw=dict(keys=keys)
    )
    if request.args.get('json') == 'true':
        return jsonify(cxt)
    import pandas as pd
    pd.set_option('display.max_colwidth', 10000)
    title = 'DICE back-end upload'
    return render_template('upload.html', pd=pd, title=title, **cxt)


@app.route('/submit/<ecas_id>/<session>', methods=['GET', 'POST'])
def dice_submit(ecas_id, session):
    """
    Submit the opened session id to the dice-db.

    :param ecas_id:
        ECAS id.
    :type ecas_id: str

    :param session:
        Session id.
    :type session: str

    :return:
         Data to be visualized to the user.
    :rtype: flask.Response
    """
    keys = ['ecas_id', 'submit', 'data_type']
    cxt = safe_call(
        inputs=dict(ecas_id=ecas_id, session=session),
        outputs=keys, select_output_kw=dict(keys=keys)
    )
    if request.args.get('json') == 'true':
        return jsonify(cxt)
    import pandas as pd
    pd.set_option('display.max_colwidth', 10000)
    title = 'DICE back-end submit'
    return render_template(
        'submit.html', title=title, pd=pd, splitext=osp.splitext, **cxt
    )


@app.route('/keys/dice.co2mpas.keys', methods=['GET', 'POST'])
def download_keys():
    from co2mpas_dice.server import _get_path
    fname = 'dice.co2mpas.keys'
    return send_file(_get_path(fname, dir='keys'), mimetype='application/x-tar')


@app.route('/attachment/<fname>', methods=['GET', 'POST'])
def download_attachment(fname):
    from co2mpas_dice.server import _get_path
    return send_file(_get_path(fname, dir='attachment'))


@app.route('/mail/<fname>', methods=['GET', 'POST'])
def send_mail(fname):
    from co2mpas_dice.server import _get_path
    from co2mpas_dice.tar import load_data
    from co2mpas_dice.server.mail import send_mail as send
    fpath = _get_path(fname, dir='diced')
    if osp.isfile(fpath):
        mail = load_data(fpath).get('mail', {})
        if mail:
            send(**mail)
        else:
            e = 'File (%s) has no mail.' % fpath
    else:
        e = 'Missing file (%s).' % fpath
    return render_template('index.html', title='DICE back-end index', error=e)


if 'DICE_DEBUG' in os.environ and eval(os.environ.get('DICE_DEBUG', '')):
    from werkzeug.middleware.profiler import ProfilerMiddleware

    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[50])

if __name__ == '__main__':
    app.run(port=7001, debug=True)
