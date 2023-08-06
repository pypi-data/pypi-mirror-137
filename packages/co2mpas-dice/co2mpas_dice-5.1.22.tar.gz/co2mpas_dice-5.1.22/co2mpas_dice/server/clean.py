# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
import re
import time
import glob
import shutil
import logging
import threading
import os.path as osp
from . import _get_path
from co2mpas_dice.server.config import conf

log = logging.getLogger(__name__)
_re_dir = re.compile(r'^\d{12,14}-')


def _clean_task():
    delay, path = int(conf['dice']['clean_delay']), _get_path('*')
    while True:
        t_str = time.strftime(
            "%Y%m%d%H%M%S", time.localtime(time.time() - delay)
        )
        rm = []
        for dpath in glob.glob(path):
            name = osp.basename(dpath)
            if _re_dir.match(name) and name < t_str:
                shutil.rmtree(dpath, True)
                rm.append(name)
        if rm:
            log.info('Removed the following temp folders:\n%s' % '\n'.join(rm))
        time.sleep(delay)


def start_cron():
    """
    Clean temp folder with a cron job.
    """
    thread = threading.Thread(target=_clean_task)
    thread.daemon = True
    thread.start()
