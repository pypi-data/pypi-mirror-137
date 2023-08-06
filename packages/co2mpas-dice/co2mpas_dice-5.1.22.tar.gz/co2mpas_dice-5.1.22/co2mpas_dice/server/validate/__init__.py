# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
import re
from co2mpas_dice.err import DiceError


def verify_encrypted_data(data):
    from co2mpas_dice.crypto import get_RSA_keys, verify_AES_key
    if not verify_AES_key(get_RSA_keys()['private'], **data):
        raise DiceError("Old keys, please update.")


def verify_hashes(data):
    import json
    from co2mpas_dice.crypto import make_hash, _json_default
    for k in ('dice_report', 'encrypted_data'):
        message = json.dumps(
            data[k], default=_json_default, sort_keys=True
        ).encode()
        verify = data['ta_id']['hash'][k]
        verify = bytes.fromhex(verify) if isinstance(verify, str) else verify
        if make_hash(message) != verify:
            raise DiceError('Invalid hash for %s.' % k)


def verify_fuel_type(data):
    if data['ta_id']['fuel_type'] != data['database']['vehicle__fuel_type']:
        raise DiceError('Mismatch of `fuel_type`.')


def verify_user(user, database):
    if user != database['user']:
        raise DiceError('Unauthorized user to the given session.')


def validate_data(user, raw_data):
    """
    Validate the raw data and check if to return the random number.

    :param user:
        User id.
    :type user: int

    :param raw_data:
         DICE data.
    :type raw_data: dict

    :return:
        Verified data and if to return a the random number.
    :rtype: dict, bool
    """
    from co2mpas_dice import verify_ta_id
    for k, v in raw_data.items():
        _validate(v, '%s.json' % k)
    verify_user(user, raw_data['database'])
    verify_ta_id(raw_data['ta_id'])
    verify_encrypted_data(raw_data['encrypted_data'])
    verify_hashes(raw_data)
    verify_fuel_type(raw_data)
    return raw_data


def _validate(data, fschema):
    import os
    import json
    import os.path as osp
    from jsonschema import validate, ValidationError
    from co2mpas_dice.server.config import conf
    versions = {
        'CO2MPAS_version': os.environ.get('DICE_CO2MPAS_VERSIONS', ''),
        'JET_version': os.environ.get('DICE_JET_VERSIONS', ''),
        'SCHEMA_version': os.environ.get('DICE_SCHEMA_VERSIONS', '')
    }

    with open(osp.join(conf['dice']['validation_folder'], fschema)) as file:
        try:
            schema = json.load(file)
            if fschema == 'dice_report.json':
                d = schema['properties']['info']['properties']
                for k, v in versions.items():
                    if v:
                        d[k]['oneOf'][0]['pattern'] = r'^\s*(%s)\s*$' % (
                            re.escape(v).replace(',', '|')
                        )
            validate(data, schema)
        except ValidationError as ex:
            raise DiceError('Schema %s: %s' % (fschema, ex.message))
    return data


def _to_hex(value):
    return value.hex() if isinstance(value, bytes) else value


def verify_db(
        company, database, vehicle_family_id, fuel_type, hash,
        extension=False, bifuel=False, wltp_retest='-',
        parent_vehicle_family_id='', broken_submission_receipt='',
        input_type='Pure ICE', **kwargs):
    from co2mpas_dice.server.db import DatabaseConnector
    status, parent = 0 if input_type == 'Pure ICE' else 3, None
    hash_inputs_meta = _to_hex(hash['inputs']), _to_hex(hash['meta'])

    with DatabaseConnector() as conn:
        if broken_submission_receipt:
            args = '^%s\\.' % broken_submission_receipt,
            args += (vehicle_family_id,) * 2 + hash_inputs_meta
            conn.cursor.execute(
                "SELECT id, `file`, valid "
                "FROM dice "
                "WHERE `file` REGEXP %s AND ("
                "(vehicle_family_id=%s AND valid<>-1 AND valid<>-3) OR "
                "(valid=-4) OR "
                "(vehicle_family_id<>%s AND hash__inputs=%s AND hash__meta=%s "
                " AND valid=-1))", args
            )
            prev_valid = conn.cursor.fetchone()
            if not prev_valid:
                raise DiceError(
                    "The submission receipt does not exist or it is not broken, "
                    "please correct or contact us."
                )
        else:
            conn.cursor.execute(
                "SELECT id, `file`, valid "
                "FROM dice "
                "WHERE (vehicle_family_id=%s AND valid<>-1 AND valid<>-3) OR "
                "(vehicle_family_id<>%s AND hash__inputs=%s AND hash__meta=%s "
                " AND valid=-1) ORDER BY time_upload DESC LIMIT 1",
                (vehicle_family_id,) * 2 + hash_inputs_meta
            )
            prev_valid = conn.cursor.fetchone()

        if parent_vehicle_family_id:
            if parent_vehicle_family_id == vehicle_family_id:
                raise DiceError(
                    "Vehicle family ID coincides with the parent one, "
                    "please correct or contact us."
                )
            status, p, s, e = 1, hash_inputs_meta, 'hash__inputs', 'Inputs'
            if 'input' in hash and 'target_nedc' in hash:
                p = _to_hex(hash['input']), _to_hex(hash['target_nedc']), p[1]
                s = 'hash__input, hash__target_nedc'
                e = "Input, target NEDC,"

            conn.cursor.execute(
                "SELECT id, `file`, info__INPUT_version, {}, hash__meta "
                "FROM dice WHERE valid = 1 AND vehicle_family_id = %s "
                "AND fuel_type = %s AND input_type = %s "
                "ORDER BY time_upload DESC LIMIT 1".format(s),
                (parent_vehicle_family_id, fuel_type, input_type)
            )
            match = conn.cursor.fetchone()
            if not match:
                raise DiceError(
                    "Vehicle family ID of the parent is not in the database, "
                    "please correct or contact us."
                )
            elif all(v is None for v in match[3:]):
                pass  # Parent diced with DICE2.
            elif (match[2] or '').split('.')[:2] != database.get(
                    'info__INPUT_version', '').split('.')[:2]:
                pass  # Parent diced with older input file.
            elif match[3:] != p:
                raise DiceError(
                    "{} and meta does not match to those of the parent (#{}), "
                    "please correct or contact us.".format(e, match[0])
                )
            parent = match[:2]
        else:
            for k in ('inputs', 'input'):
                conn.cursor.execute(
                    'SELECT id FROM dice WHERE valid=1 AND '
                    'hash__{}=%s AND parent_vehicle_family_id IS NULL '
                    'LIMIT 1'.format(k), (_to_hex(hash.get(k, b'none')),)
                )
                match = conn.cursor.fetchone()
                if match:
                    raise DiceError(
                        "A file (#{}) with same inputs has already been "
                        "submitted, "
                        "please update or contact us.".format(match[0])
                    )
        if 'target_nedc' in hash and prev_valid and prev_valid[-1] == -2:
            conn.cursor.execute(
                "SELECT 1 FROM dice "
                "WHERE id=%s AND hash__target_nedc=%s "
                "ORDER BY time_upload DESC LIMIT 1",
                (prev_valid[0], _to_hex(hash['target_nedc']))
            )
            if conn.cursor.fetchone():
                raise DiceError(
                    "The NEDC targets are the same of the last submission (#{})"
                    ", please correct or contact us.".format(prev_valid[0])
                )

        if bifuel:
            conn.cursor.execute(
                "SELECT 1 FROM dice WHERE vehicle_family_id = %s "
                "AND valid = 1 AND fuel_type = %s AND input_type = %s LIMIT 1",
                (vehicle_family_id, fuel_type, input_type)
            )
        else:
            conn.cursor.execute(
                "SELECT 1 FROM dice WHERE vehicle_family_id = %s "
                "AND valid = 1 AND input_type = %s LIMIT 1",
                (vehicle_family_id, input_type)
            )

        if conn.cursor.fetchone():
            if not (extension or wltp_retest != '-'):
                raise DiceError(
                    "Duplicated Vehicle family ID, please update or contact us."
                )
        elif extension:
            raise DiceError(
                "Invalid extension (Vehicle family ID not in the database), "
                "please correct or contact us."
            )
        elif wltp_retest != '-':
            raise DiceError(
                "Invalid wltp_retest (Vehicle family ID not in the database), "
                "please correct or contact us."
            )

        if bifuel:
            conn.cursor.execute(
                "SELECT 1 FROM dice WHERE "
                "vehicle_family_id = %s AND valid = 1 AND bifuel = 0 LIMIT 1",
                (vehicle_family_id,)
            )
            if conn.cursor.fetchone():
                raise DiceError(
                    "Invalid bi-fuel (Vehicle family ID is not a bi-fuel), "
                    "please correct or contact us."
                )

            conn.cursor.execute(
                "SELECT fuel_type, COUNT(1) FROM dice WHERE "
                "vehicle_family_id = %s AND valid = 1 GROUP BY fuel_type",
                (vehicle_family_id,)
            )
            fuels = dict(conn.cursor.fetchall())
            fuels[fuel_type] = fuels.get(fuel_type, 0) + 1
            if len(fuels) > 2:
                raise DiceError(
                    "Too many fuels (%s) for Vehicle family ID, "
                    "please update or contact us." % ','.join(sorted(fuels))
                )
            dn = (lambda n1, n2=0: abs(n1 - n2))(*fuels.values())
            if dn > 1:
                fuels = len(fuels) == 2 and '(%s) ' % min(fuels, key=fuels.get)
                raise DiceError(
                    "Missing second fuel %sfor Vehicle family ID, "
                    "please update or contact us." % (fuels or '')
                )
            if dn == 0:
                conn.cursor.execute(
                    "SELECT dice.extension, dice.wltp_retest, "
                    "users.company_id, dice.incomplete, "
                    "dice.parent_vehicle_family_id "
                    "FROM dice, users WHERE dice.user = users.id AND "
                    "vehicle_family_id=%s AND valid=1 AND bifuel = 1 "
                    "ORDER BY time_upload DESC LIMIT 1", (vehicle_family_id,)
                )
                match = conn.cursor.fetchone()
                if match:
                    if match[-1] is not None:
                        conn.cursor.execute(
                            "SELECT vehicle_family_id FROM dice WHERE id=%s "
                            "LIMIT 1", (match[-1],)
                        )
                        match = match[:-1] + conn.cursor.fetchone()
                    keys = 'extension', 'wltp_retest', 'company', 'invalid'
                    values = (
                        extension, wltp_retest, company,
                        int(kwargs['dice'].get('incomplete', 0))
                    )
                    err = [k for k, v, m in zip(keys, values, match) if v != m]
                    if err:
                        raise DiceError(
                            "Invalid bi-fuel (%s is/are not matching "
                            "the previous submitted file), "
                            "please correct or contact us." % ', '.join(err)
                        )
            if dn == 1 and status == 3:
                status = 2
            else:
                status = max(status, int(dn == 1) * 2)
        if prev_valid and status == 0:
            if prev_valid[-1] in (-1, -2):
                status = 3 - prev_valid[-1]
            elif wltp_retest == 'a':
                status = 6
            elif prev_valid[-1] == 0:
                tool = 'CO2MPAS' if kwargs.get('co2mpas', True) else 'INPUT'
                key = 'info__%s_version' % tool
                version = database[key]
                conn.cursor.execute(
                    "SELECT 1 FROM dice "
                    "WHERE id=%s AND hash__inputs=%s AND "
                    "{}=%s "
                    "ORDER BY time_upload DESC LIMIT 1".format(key),
                    (prev_valid[0], _to_hex(hash['inputs']), version)
                )
                if conn.cursor.fetchone():
                    raise DiceError(
                        'Same data of the last invalid submission (#{}), '
                        'please correct or contact us.'.format(prev_valid[0])
                    )
                if 'target_nedc' in hash:
                    db = database
                    it = (('ROUND(`{}`,5)=ROUND(%s,5)'
                           if k in db else
                           '`{}` IS %s').format(k)
                          for k in ('deviation__nedc_h', 'deviation__nedc_l'))
                    conn.cursor.execute(
                        "SELECT 1 FROM dice "
                        "WHERE id=%s AND hash__target_nedc=%s AND "
                        "{}=%s AND {} "
                        "AND {} "
                        "ORDER BY time_upload DESC LIMIT 1".format(key, *it),
                        (prev_valid[0], _to_hex(hash['target_nedc']),
                         version,
                         database.get('deviation__nedc_h'),
                         database.get('deviation__nedc_l'))
                    )
                else:
                    conn.cursor.execute(
                        "SELECT 1 FROM dice "
                        "WHERE id=%s AND hash__input=%s AND "
                        "{}=%s "
                        "ORDER BY time_upload DESC LIMIT 1".format(key),
                        (prev_valid[0], _to_hex(hash['input']), version)
                    )
                if conn.cursor.fetchone():
                    status = 7

        return status, parent, prev_valid
