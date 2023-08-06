# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
import yaml
import os.path as osp


class DiceError(Exception):
    def __init__(self, *args):
        a = list(args)
        try:
            from .server.config import conf
            with open(osp.join(conf['dice']['error_folder'], 'err.yaml')) as f:
                a[0] = yaml.load(f.read(), Loader=yaml.CLoader).get(a[0], a[0])
        except ImportError:
            pass
        super(DiceError, self).__init__(*a)
