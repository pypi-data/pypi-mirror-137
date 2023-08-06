# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
import io
import os
import yaml
import tarfile
import os.path as osp


def write_tar(tar, path, obj):
    serialized_obj = yaml.dump(
        obj, encoding='utf-8', default_flow_style=False,
        Dumper=yaml.CSafeDumper
    )
    info = tarfile.TarInfo(path)
    info.size = len(serialized_obj)
    tar.addfile(info, io.BytesIO(serialized_obj))


def save_data(fpath, _write=True, **data):
    """
    Save data in a tar:bz2 file.

    :param fpath:
        File path to save the data or stream.
    :type fpath: str | io.BytesIO

    :param data:
        Data to be saved.
    :type data: object

    :rtype:
        File path to save the data or stream.
    :rtype: str | io.BytesIO
    """
    if isinstance(fpath, str):
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
    with tarfile.open(mode='w:bz2', fileobj=get_fileobj(fpath)) as tar:
        for k, v in data.items():
            write_tar(tar, k, v)
    return fpath


def get_fileobj(fpath):
    if isinstance(fpath, str):
        if not osp.isfile(fpath):
            return fpath
        with open(fpath, 'rb') as f:
            return io.BytesIO(f.read())
    if isinstance(fpath, io.BytesIO):
        return fpath
    from werkzeug.datastructures import FileStorage
    if isinstance(fpath, FileStorage):
        return io.BytesIO(fpath.stream.read())


def get_filename(fpath):
    if isinstance(fpath, str):
        return os.path.basename(fpath)
    from werkzeug.datastructures import FileStorage
    if isinstance(fpath, FileStorage):
        return fpath.filename


TAR_MODE_MAP = {
    b"\x1f\x8b\x08": 'r:gz',
    b"\x42\x5a\x68": 'r:bz2',
    b"\x50\x4b\x03\x04": 'r:zip'
}


def tarmode(fileobj):
    max_len = max(len(x) for x in TAR_MODE_MAP)
    file_start = fileobj.read(max_len)
    for magic, filetype in TAR_MODE_MAP.items():
        if file_start.startswith(magic):
            return filetype
    return 'r'


def load_data(file):
    data, fileobj = {}, get_fileobj(file)
    mode = tarmode(fileobj)
    fileobj.seek(0)
    with tarfile.open(mode=mode, fileobj=fileobj) as tar:
        for member in tar.getmembers():
            with tar.extractfile(member) as f:
                data[member.name] = yaml.load(f.read(), Loader=yaml.CLoader)
    return data
