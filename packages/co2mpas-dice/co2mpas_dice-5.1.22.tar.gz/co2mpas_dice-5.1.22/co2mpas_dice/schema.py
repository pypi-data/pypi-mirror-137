# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
import functools
import schedula as sh


@functools.lru_cache(None)
def define_dice_schema(read=True):
    """
    Define DICE schema.

    :param read:
        Schema for reading?
    :type read: bool

    :return:
        DICE schema.
    :rtype: schema.Schema
    """
    import re
    from schema import Or, And, Use, Optional, Schema, SchemaError
    from co2mpas.core.load.schema import (
        _string, _type, _compare_str, _select, Empty
    )

    vehicle_family_id_pattern = r'''
        (?:
            (IP|RL|RM|PR) - (\d{2}) - ([A-Z0-9_]{2,3}) - (\d{4}) - (\d{4})
        )
        |
        (?:
            IP - ([A-Z0-9_]{2,15}) - ([A-Z0-9_]{3}) - ([01])
        )
    '''
    _vehicle_family_id_regex = re.compile(
        '(?x)^%s$' % vehicle_family_id_pattern
    )
    submission_receipt_pattern = r'''
        (?:
            (\d{4}) - (IP|RL|RM|PR) - (\d{2}) - ([A-Z0-9_]{2,3}) - (\d{4}) - (\d{4})
        )
        |
        (?:
            (\d{4}) - IP - ([A-Z0-9_]{2,15}) - ([A-Z0-9_]{3}) - ([01])
        )
    '''
    _submission_receipt_regex = re.compile(
        '(?x)^%s$' % submission_receipt_pattern
    )
    invalid_vehicle_family_id_msg = (
        "Invalid VF_ID '%s'!"
        "\n  New format is 'IP-nnn-WMI-x', where nnn is (2, 15) chars "
        "of A-Z, 0-9, or underscore(_),"
        "\n  (old format 'FT-ta-WMI-yyyy-nnnn' is still acceptable)."
    )

    def _vehicle_family_id(error=None, **kwargs):
        def _m(s):
            if not _vehicle_family_id_regex.match(s):
                raise SchemaError(invalid_vehicle_family_id_msg % s)
            return True

        return And(_string(**kwargs), _m, error=error)

    def _submission_receipt(error=None, **kwargs):
        def _m(s):
            if not _submission_receipt_regex.match(s):
                raise SchemaError("Invalid DICE submission receipt '%s'!" % s)
            return True

        return And(_string(**kwargs), _m, error=error)

    string = _string(read=read)
    _bool = _type(type=bool, read=read)
    _float = _type(type=float, read=read)
    schema = {
        _compare_str('vehicle_family_id'): _vehicle_family_id(read=read),
        _compare_str('broken_submission_receipt'): _submission_receipt(
            read=read
        ),
        _compare_str('bifuel'): _bool,
        _compare_str('extension'): _bool,
        _compare_str('incomplete'): _bool,
        _compare_str('small_volume_oem'): _bool,
        _compare_str('regulation'): string,
        _compare_str('comments'): string,
        _compare_str('atct_family_correction_factor'): _float,
        _compare_str('wltp_retest'): _select(
            types=('-', 'a', 'b', 'c', 'd', 'ab', 'ac', 'ad', 'bc', 'bd', 'cd',
                   'abc', 'abd', 'abcd'), read=read),
        _compare_str('parent_vehicle_family_id'): _vehicle_family_id(read=read),
        _compare_str('input_type'): _select(types=(
            'Pure ICE', 'NOVC-HEV', 'OVC-HEV'
        ), read=read),
        str: Or(Use(float), object)
    }

    schema = {Optional(k): Or(Empty(), v) for k, v in schema.items()}

    if not read:
        def _f(x):
            return x is sh.NONE

        schema = {k: And(v, Or(_f, Use(str))) for k, v in schema.items()}

    return Schema(schema)
