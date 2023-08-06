# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
import re
import os
import time
import secrets
import tempfile
import itertools
import os.path as osp
import schedula as sh
from co2mpas_dice.server.config import _get_path
from co2mpas_dice.err import DiceError

dice = sh.BlueDispatcher(raises=True)
RANDOM_FILENAME = 'random.tar.bz2'
UPLOAD_FILENAME = 'data.tar.bz2'


@sh.add_function(dice, outputs=['company', 'user'])
def register_company_user(company_name, user_mail, ecas_id):
    """
    Get company and user.

    :param company_name:
        Company name.
    :type company_name: str

    :param user_mail:
        User email.
    :type user_mail: str

    :param ecas_id:
        ECAS id.
    :type ecas_id: str

    :return:
        Company and User ids.
    :rtype: int, int
    """
    from .db import DatabaseConnector
    with DatabaseConnector() as conn:
        params = dict(name=company_name, mail=user_mail, ecas=ecas_id)
        conn.cursor.execute(
            "INSERT IGNORE INTO companies (name) "
            "SELECT %(name)s FROM users WHERE NOT EXISTS "
            "(SELECT * FROM users WHERE mail = %(mail)s OR ecas_id = %(ecas)s "
            "LIMIT 1)", params
        )
        conn.cnx.commit()
        conn.cursor.execute(
            "INSERT IGNORE INTO users (company_id, mail, ecas_id) "
            "SELECT id, %(mail)s, %(ecas)s FROM companies WHERE name=%(name)s "
            "LIMIT 1", params
        )
        conn.cnx.commit()
        conn.cursor.execute(
            "SELECT companies.id, users.id FROM companies, users "
            "WHERE companies.id=users.company_id AND companies.name = %(name)s "
            "AND users.mail=%(mail)s AND users.ecas_id = %(ecas)s LIMIT 1",
            params
        )
        res = conn.cursor.fetchone()
        if res:
            return res
        raise DiceError('Wrong registration (user not match that in database)!')


@sh.add_function(dice, outputs=['company', 'user'], weight=1)
def get_company_user(ecas_id):
    """
    Get company and user.

    :param ecas_id:
        ECAS id.
    :type ecas_id: str

    :return:
        Company and User ids.
    :rtype: int, int
    """
    from .db import DatabaseConnector
    with DatabaseConnector() as conn:
        conn.cursor.execute(
            "SELECT company_id, id FROM users WHERE ecas_id = %s LIMIT 1",
            (ecas_id,)
        )
        res = conn.cursor.fetchone()
        if not res:
            raise DiceError('User not authorized!')
        return res


@sh.add_function(dice, outputs=['company_name'])
def get_company_name(user):
    """
    Get company name.

    :param user:
       User id.
    :type user: int

    :return:
       Company name.
    :rtype: str
    """
    from .db import DatabaseConnector
    with DatabaseConnector() as conn:
        conn.cursor.execute(
            "SELECT name FROM companies "
            "WHERE id=(SELECT company_id FROM users WHERE id = %s LIMIT 1) "
            "LIMIT 1", (user,)
        )
        return conn.cursor.fetchone()[0]


@sh.add_function(dice, outputs=['user_mail'])
def get_user_mail(user):
    """
    Get user mail.

    :param user:
       User id.
    :type user: int

    :return:
       User mail.
    :rtype: str
    """
    from .db import DatabaseConnector
    with DatabaseConnector() as conn:
        conn.cursor.execute(
            "SELECT mail FROM users WHERE id = %s LIMIT 1", (user,)
        )
        return conn.cursor.fetchone()[0]


@sh.add_function(dice, outputs=['rand_hash', 'session'], weight=sh.inf(2, 0))
def generate_random(company, user, company_name, user_mail):
    """
    Generate a random number and hash its signature.

    :param company:
        Company id.
    :type company: int

    :param user:
        User id.
    :type user: int

    :param company_name:
        Company name.
    :type company_name: str

    :param user_mail:
        User mail.
    :type user_mail: str

    :return:
        Hash of the random number signature and the session id.
    :rtype: hex, str
    """
    from co2mpas_dice.tar import save_data
    from co2mpas_dice.crypto import get_RSA_keys, sign_data, make_hash, \
        format_public_RSA_key
    folder = _get_path()
    os.makedirs(folder, exist_ok=True)
    folder = tempfile.mkdtemp(
        prefix=time.strftime("%Y%m%d%H%M%S-", time.localtime(time.time())),
        dir=folder
    )
    num = secrets.randbelow(100)
    key = get_RSA_keys()['private']['server']
    signature = sign_data(key, num)[0]
    signature_hash = make_hash(signature).hex()

    save_data(
        osp.join(folder, RANDOM_FILENAME),
        server_random=num,
        server_random_signature=signature.hex(),
        server_random_signature_hash=signature_hash,
        server_pub_key=format_public_RSA_key(key.public_key()),
        company=company,
        user=user,
        company_name=company_name,
        user_mail=user_mail
    )
    return signature_hash, osp.basename(folder)


def _get_dice_report_data(dice_report):
    res = {'info__%s' % k: v for k, v in sh.selector((
        'datetime', 'CO2MPAS_version', 'DICE_version', 'JET_version',
        'SCHEMA_version', 'INPUT_version'
    ), dice_report['info'], allow_miss=True).items()}

    keys = [
        ('alternator_model', 'alternator_currents'),
        ('alternator_model', 'battery_currents'),
        ('at_model', 'gears'),
        ('clutch_torque_converter_model', 'engine_speeds_out'),
        ('co2_params', 'identified_co2_emissions'),
        ('engine_cold_start_speed_model', 'engine_speeds_out'),
        ('engine_coolant_temperature_model', 'engine_coolant_temperatures'),
        ('engine_speed_model', 'engine_speeds_out'),
        ('start_stop_model', 'engine_starts'),
        ('start_stop_model', 'on_engine'),
        # CO2MPAS 4.1.x
        ('electrics_model', 'service_battery_currents'),
        ('electrics_model', 'alternator_currents'),
        ('electrics_model', 'drive_battery_currents'),
        ('electrics_model', 'dcdc_converter_currents'),
        ('after_treatment_model', 'engine_speeds_base'),
        ('control_model', 'engine_starts'),
        ('control_model', 'on_engine'),
    ]
    if sh.are_in_nested_dicts(dice_report, 'model_scores', 'scores'):
        scores = sh.get_nested_dicts(dice_report, 'model_scores', 'scores')
        for k, v in sh.stack_nested_keys(scores, depth=2):
            for d in v:
                i = d['model_id'], d['param_id']
                if i in keys:
                    j = '__'.join(k + i).replace('temperature', 'temp')
                    res[j] = float(d['score'])

    it = list(itertools.product(
        ('nedc_h', 'nedc_l', 'wltp_h', 'wltp_l'),
        (('engine_is_turbo', bool), ('fuel_type', str),
         ('engine_capacity', float), ('gear_box_type', str),
         ('engine_max_power', float), ('engine_speed_at_max_power', float),
         ('delta_state_of_charge', float),
         ('service_battery_delta_state_of_charge', float),
         ('drive_battery_delta_state_of_charge', float))
    ))
    common = {
        'engine_is_turbo', 'fuel_type', 'engine_capacity', 'gear_box_type',
        'engine_max_power', 'engine_speed_at_max_power'
    }
    for cycle, (param, func) in it:
        k = 'vehicle', cycle, param
        if sh.are_in_nested_dicts(dice_report, *k):
            val = func(sh.get_nested_dicts(dice_report, *k))
            if param in common:
                k = 'vehicle__%s' % param
                if k in res and res[k] != val:
                    raise DiceError('Wrong vehicle param %s is not identical '
                                    'for all cycles.' % param)
                res[k] = val
            else:
                res['%s__%s' % (cycle, param)] = val

    for i in ('deviation', 'ratios', 'gears'):
        for k, v in sh.stack_nested_keys(dice_report.get(i, {}), (i,)):
            res['__'.join(k)] = float(v)

    return res


def _define_random(session, data):
    from co2mpas_dice.tar import load_data
    rnd = load_data(_get_path(session, RANDOM_FILENAME))
    u = rnd['user_random'] = data['ta_id'].get('user_random', 0)
    rnd['random'] = (u + rnd['server_random']) % 100
    return rnd


def _get_db_data(user, file, data):
    import json
    from .db import DatabaseConnector
    from co2mpas_dice.crypto import make_hash, _json_default
    from co2mpas_dice.tar import get_filename
    kv = {
        '__'.join(k): v.hex() if isinstance(v, bytes) else v
        for k, v in sh.stack_nested_keys(data['ta_id'])
    }
    kv.update(_get_dice_report_data(data['dice_report']))
    kv['hash__tot'] = make_hash(json.dumps(sh.selector(
        ('ta_id', 'dice_report', 'encrypted_data'), data, allow_miss=True
    ), default=_json_default, sort_keys=True).encode()).hex()
    kv['uploaded_fname'] = get_filename(file)
    file.stream.seek(0)
    kv['hash__ta_file'] = make_hash(file.stream.read()).hex()
    kv['user'] = user
    kv['input_type'] = data['ta_id']['dice'].get('input_type', 'Pure ICE')
    kv['random'] = data['random']['random']
    kv['user_random'] = data['random']['user_random']
    kv['server_random'] = data['random']['server_random']
    kv['incomplete'] = int(data['ta_id']['dice'].get('incomplete', 0))
    kv['small_volume_oem'] = int(
        data['ta_id']['dice'].get('small_volume_oem', 0))
    kv.pop('parent_vehicle_family_id')
    kv.pop('broken_submission_receipt', None)
    with DatabaseConnector() as conn:
        conn.cursor.execute('SHOW COLUMNS FROM dice')
        return {k: kv[k] for k in {v[0] for v in conn.cursor}.intersection(kv)}


def _str2bytes(x):
    return (x.encode() if isinstance(x, str) else x).replace(b'\r\n', b'\n')


def _check_user_pub_sign_key(user, key):
    from co2mpas_dice.crypto import make_hash
    from .db import DatabaseConnector
    with DatabaseConnector() as conn:
        conn.cursor.execute("SELECT hash_key FROM users WHERE id = %s", (user,))
        key_hash = conn.cursor.fetchone()[0]
        if not key_hash:
            conn.cursor.execute(
                "UPDATE `users` SET `hash_key`=%s WHERE id=%s",
                (make_hash(_str2bytes(key)).hex(), user)
            )
            conn.cnx.commit()
        elif key_hash != make_hash(_str2bytes(key)).hex():
            raise DiceError('Invalid user key, please correct or contact us.')


@sh.add_function(dice, outputs=['data'], weight=sh.inf(1, 0))
def upload_data(company, user, session, file):
    """
    Check and upload the data to the session folder.

    :param company:
        Company id.
    :type company: int

    :param user:
        User id.
    :type user: int

    :param session:
        Session id.
    :type session: str

    :param file:
        File to upload.
    :type file: werkzeug.datastructures.FileStorage | str

    :return:
        DICE data.
    :rtype: dict
    """
    from co2mpas_dice.tar import (
        load_data as _load_data, save_data, get_filename
    )
    from .validate import validate_data, verify_db
    fname = get_filename(file).lower()
    if not (fname.endswith('.co2mpas.ta') or fname.endswith('.jet.ta')):
        raise DiceError(
            'Wrong file extension (.%s), please provide a '
            '.jet.ta file!' % '.'.join(fname.split('.')[1:])
        )
    data = _load_data(file)
    data['type'] = data['ta_id'].get('co2mpas', True) and 'co2mpas' or 'jet'
    data['random'] = _define_random(session, data)
    data['database'] = _get_db_data(user, file, data)
    data = validate_data(data['random']['user'], data)
    verify_db(company, data['database'], **data['ta_id'])
    _check_user_pub_sign_key(user, data['ta_id']['pub_sign_key'])
    save_data(_get_path(session, UPLOAD_FILENAME), **data)
    os.remove(_get_path(session, RANDOM_FILENAME))
    return data


@sh.add_function(dice, outputs=['rand_hash'])
def get_server_random_signature_hash(data):
    """
    Get the hash of server random number signature from DICE data.

    :param data:
        DICE data.
    :type data: dict

    :return:
        Hash of the random number signature.
    :rtype: str
    """
    return sh.get_nested_dicts(data, 'random', 'server_random_signature_hash')


@sh.add_function(dice, outputs=['data_type'])
def get_data_type(data):
    """
    Get the data type from DICE data.

    :param data:
        DICE data.
    :type data: dict

    :return:
        DICE data type.
    :rtype: str
    """
    return data.get('type', 'co2mpas')


@sh.add_function(dice, outputs=['tables'])
def get_tables(data):
    """
    Extract tables data from DICE data.

    :param data:
        DICE data.
    :type data: dict

    :return:
         Tables data.
    :rtype: dict
    """
    import pandas as pd
    dr = data['dice_report']
    tables = {
        'ratios': pd.DataFrame([dr.get('ratios', {})]).to_dict(orient='split'),
        'info': pd.DataFrame([sh.combine_dicts(
            dr['info'],
            base={'uploaded_file_name': data['database']['uploaded_fname']}
        )]).T.to_dict(orient='split'),
        'vehicle': pd.DataFrame(sh.combine_nested_dicts(
            dr['vehicle'], base={
                k: {'co2_deviation': v} for k, v in
                dr.get('deviation', {}).items()
            }
        )).to_dict(orient='split'),
        'hash': pd.DataFrame({
            k[6:]: [v] for k, v in data['database'].items()
            if k.startswith('hash__')
        }).T.to_dict(orient='split')
    }

    if sh.are_in_nested_dicts(dr, 'model_scores', 'scores'):
        tables['scores'] = pd.concat(
            {k: pd.DataFrame(v).set_index(['model_id', 'param_id'])['score']
             for k, v in sh.stack_nested_keys(dr['model_scores']['scores'])},
            axis=1
        ).to_dict(orient='split')

    return tables


def load_data_dom(user, session):
    """
    Check if the DICE data are uploaded in the session folder.

    :param user:
        User id.
    :type user: int

    :param session:
        Session id.
    :type session: str

    :return:
        If to execute the `load_data` function.
    :rtype: bool
    """
    return osp.isfile(_get_path(session, UPLOAD_FILENAME))


@sh.add_function(dice, outputs=['data'], input_domain=load_data_dom)
def load_data(user, session):
    """
    Load th uploaded data.

    :param user:
        User id.
    :type user: int

    :param session:
        Session id.
    :type session: str

    :return:
        DICE data.
    :rtype: dict
    """
    from .validate import validate_data as validate
    from co2mpas_dice.tar import load_data as load
    return validate(user, load(_get_path(session, UPLOAD_FILENAME)))


def _get_safe_fpath(vehicle_family_id, data_type):
    from .db import DatabaseConnector
    fp = _get_path('%04d-{}.{}.ta'.format(
        vehicle_family_id, data_type
    ), dir='diced')
    with DatabaseConnector() as conn:
        conn.cursor.execute(
            "SELECT file FROM dice WHERE "
            "file REGEXP '\d*-{}\.{}\.ta$'".format(vehicle_family_id, data_type)
        )
        _re_file = re.compile(r'\d*(?=-.*\.{}\.ta$)'.format(data_type))
        i = max([int(_re_file.match(v).group()) for v, in conn.cursor] + [-1])
        while True:
            i += 1
            fpath = fp % i
            if not osp.exists(fpath):
                return fpath


def _upload_data2db(**data):
    from .db import DatabaseConnector
    with DatabaseConnector() as conn:
        f = lambda s: ', '.join(map(s.format, sorted([
            k for k, v in data.items() if v is not None
        ])))
        conn.cursor.execute(
            'INSERT INTO dice (%s) VALUES (%s)' % (f('`{}`'), f('%({})s')), data
        )
        conn.cnx.commit()


@sh.add_function(dice, outputs=['submit'])
def push_data(company, session, data, data_type):
    """
    Push the data into the DICE db.

    :param company:
        Company id.
    :type company: int

    :param session:
        Session id.
    :type session: str

    :param data:
        DICE data.
    :type data: dict

    :param data_type:
        DICE data type.
    :type data_type: str

    :return:
        Random data.
    :rtype: dict
    """
    from co2mpas_dice.tar import save_data
    from .mail import send_mail, prepare_mail
    from .validate import verify_db

    db, rnd, ta_id, res = data['database'], data['random'], data['ta_id'], {}

    fpath = _get_safe_fpath(ta_id['vehicle_family_id'], data_type)
    db['file'] = osp.basename(fpath)

    status_random, parent, prev_valid = verify_db(
        company, data['database'], **data['ta_id']
    )
    if prev_valid:
        res['prev_valid'] = prev_valid
        if prev_valid[-1] not in (1, -3):
            db['broken_submission_receipt'] = prev_valid[0]
    db['parent_vehicle_family_id'] = None
    if parent:
        res['parent'] = parent
        db['parent_vehicle_family_id'] = parent[0]

    if data['ta_id'].get('broken_submission_receipt'):
        db['broken_submission_receipt'] = prev_valid[0]
    mail, deviations = prepare_mail(
        data, data_type, status_random, prev_valid, parent
    )
    data['mail'] = mail
    if status_random != 2:
        res['attachment'] = db['attachment'] = mail['filename']
        res['deviations'] = deviations
        res['vehicle_family_id'] = ta_id['vehicle_family_id']
        res['receipt_id'] = osp.splitext(mail.get('filename', '.'))[0]
        res['hash'] = db['hash__dice_receipt']
        if status_random == 1:
            res['parent_vehicle_family_id'] = ta_id['parent_vehicle_family_id']

    if status_random != 0:
        data['random']['random'] = db['random'] = None
    else:
        res['random'] = db['random']

    save_data(fpath, **data)

    _upload_data2db(**db)

    send_mail(**mail)

    import shutil
    shutil.rmtree(_get_path(session), True)
    return sh.combine_dicts(dict(
        status_random=status_random,
        user_mail=rnd['user_mail'],
        uploaded_fname=db['uploaded_fname']
    ), base=res)


@sh.add_function(dice, outputs=['diced'], weight=sh.inf(3, 0),
                 inputs_defaults=True)
def get_diced(company, last_rows=25):
    """
    Extract diced data from DICE database.

    :param company:
        Company id.
    :type company: int

    :param last_rows:
        Number of database rows to extract.
    :type last_rows: int

    :return:
         Diced data.
    :rtype: dict
    """
    from .db import DatabaseConnector
    with DatabaseConnector() as conn:
        conn.cursor.execute("SHOW COLUMNS FROM dice")
        columns = tuple(v[0] for v in conn.cursor)

        cmd = "SELECT %s FROM dice {} ORDER BY time_upload DESC LIMIT %d"
        cmd = (cmd % (','.join(columns), last_rows)).format
        if company > 0:
            conn.cursor.execute(cmd(
                'WHERE user IN (SELECT id FROM users WHERE company_id = %s) '
                'AND valid=1'
            ), (company,))
        else:
            conn.cursor.execute(cmd(''))

        return dict(data=list(conn.cursor), columns=columns)


if __name__ == '__main__':
    import shutil

    shutil.rmtree('../../build/temp', True)
    shutil.rmtree('../../build/diced', True)

    sol = dice({
        'company': 'company',
        'user': 'user',
        'file': '../file.co2mpas.ta'
    })
    sol.plot()
