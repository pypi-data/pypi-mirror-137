#  -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
r"""
It provides data to configure the dice model.
"""

import os
import re
import json
import configparser
import pkg_resources
import os.path as osp


class ConfigParser(configparser.ConfigParser):
    def get(self, *args, **kwargs):
        try:
            return super(ConfigParser, self).get(*args, **kwargs)
        except (KeyError, configparser.NoOptionError) as ex:
            if args[1]:
                raise ex
            args, d = list(args), {}
            for p in self._unify_values(args[0], kwargs.get('vars')):
                args[1] = p
                d[p] = super(ConfigParser, self).get(*args, **kwargs)
            return json.dumps(d)


_re_env = re.compile(r"%\((?P<key>\w+)(?:-(?P<default>[^)]*))?\)")


class ExtendedInterpolation(configparser.ExtendedInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        while True:
            m = _re_env.search(value)
            if not m:
                break
            k = m.group(0)
            value = value.replace(k, os.environ.get(**m.groupdict(k)))
            value = super(ExtendedInterpolation, self).before_get(
                parser, section, option, value, defaults
            )
        value = super(ExtendedInterpolation, self).before_get(
            parser, section, option, value, defaults
        )
        if _re_env.search(value):
            value = self.before_get(parser, section, option, value, defaults)
        return value


conf = ConfigParser(interpolation=ExtendedInterpolation())
conf.read(pkg_resources.resource_filename(__name__, 'app.ini'))


def _get_path(*p, dir='temp'):
    return osp.abspath(osp.join(conf['dice']['%s_folder' % dir], *p))
