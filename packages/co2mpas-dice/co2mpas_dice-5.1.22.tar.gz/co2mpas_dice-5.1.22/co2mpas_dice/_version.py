# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

__all__ = ['__version__', '__updated__', '__jet_version__']

#: Authoritative project's PEP 440 version.
__version__ = version = "5.1.22"  # Also update README.rst,
__jet_version__ = jet_version = "1.0.16"

# Please UPDATE TIMESTAMP WHEN BUMPING VERSIONS AND BEFORE RELEASE.
#: Release date.
__updated__ = updated = "2021-12-13 18:30:00"

if __name__ == '__main__':
    import sys

    out = ';'.join(
        eval(a[2:].replace('-', '_')) for a in sys.argv[1:] if a[:2] == '--'
    )
    sys.stdout.write(out)
