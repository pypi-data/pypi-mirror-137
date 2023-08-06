# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
class DatabaseConnector:
    def __enter__(self):
        import mysql.connector as db
        from co2mpas_dice.server.config import conf
        self.cnx = db.connect(**conf['db'])
        self.cursor = self.cnx.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.cnx.close()
