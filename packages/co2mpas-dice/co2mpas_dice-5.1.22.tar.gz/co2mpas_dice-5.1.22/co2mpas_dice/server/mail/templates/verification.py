# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
import io
import re
import json
import tarfile
import zipfile
import os.path as osp
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import utils, padding


# --------------------------------- FUNCTIONS ---------------------------------


def get_row(text, key):
    """
    Get all values of a row from a formatted table.

    :param text:
        Text to be parsed.
    :type text: str

    :param key:
        Key value to search in the table.
    :type key: str

    :return:
        Parsed values.
    :rtype: list[str]
    """
    table = []
    p = r'\+-*\+-*\+\n\|\s*%s\s*\|\s*([0-9A-z\n\s|\.\-@_]*)\+-*\+-*\+' % key
    for row in (' | %s' % re.search(p, text).group(1)).strip('\n').split('\n'):
        table.append([v.strip(' ') for v in row.strip(' |').split('|')])
    return list(map(''.join, zip(*table)))


def get_section(text, start, stop):
    """
    Get section from formatted text.

    :param text:
        Text to be parsed.
    :type text: str

    :param start:
        Section start condition.
    :type start: str

    :param stop:
        Section stop condition.
    :type stop: str

    :return:
        Parsed value.
    :rtype: str
    """
    p = r'%s\n[\-=]*\n(.*)%s' % (start, stop)
    return re.search(p, text, re.DOTALL).group(1)


def make_hash(message):
    """
    Return the hash of the message.

    :param message:
        Message to hash.
    :type message: byte

    :return:
        Hash of the message.
    :rtype: byte
    """
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(message)
    return digest.finalize().hex()


def load_key(pem):
    """
    Loads a public key from PEM encoded data.

    :param pem:
        Key in PEM format.
    :type pem: byte

    :return:
        Public key.
    :rtype: cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey
    """
    return serialization.load_pem_public_key(pem.encode(), default_backend())


def verify_sign(key, signature, message):
    """
    Verify the signature of the message from a given keys.

    :param key:
        Public key.
    :type key: cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey

    :param signature:
        Signature of the hash of the message.
    :type signature: byte

    :param message:
        Message to verify.
    :type message: byte

    :return:
        If it is verified.
    :rtype: bool
    """
    try:
        key.verify(
            signature, bytes.fromhex(make_hash(message)),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            utils.Prehashed(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False


# ---------------------------------- INPUTS -----------------------------------
cdir = osp.dirname(__file__)
fpath_dice = osp.join(cdir, '{{file | safe}}')
if osp.isfile(fpath_dice):
    with open(fpath_dice, encoding='utf-8') as f:
        text = f.read()

{% if data_type == "jet" %}
keys = (
    'DICE Receipt Hash', 'DICE Receipt Signature', 'Uploaded Filename',
    r'Hash of \*\.jet\.ta File', r'Hash of \*\.input\.xlsx File',
    r'JET Hash \(i\.e\., \*\.jet\.zip\)'
)
{% elif status_random == 0 %}
keys = (
    'Server Random Number', 'Server Random Number Signature', 'Random Number',
    'Server Random Number Signature Hash', 'User Random Number',
    'DICE Receipt Hash', 'DICE Receipt Signature', 'Uploaded Filename',
    r'Hash of \*\.co2mpas\.ta File', r'Hash of \*\.input\.xlsx File',
    r'Hash of \*\.output\.xlsx File',
    r'Correlation Hash \(i\.e\., \*\.co2mpas\.zip\)'
)
{% else %}
keys = (
    'DICE Receipt Hash', 'DICE Receipt Signature', 'Uploaded Filename',
    r'Hash of \*\.co2mpas\.ta File', r'Hash of \*\.input\.xlsx File',
    r'Hash of \*\.output\.xlsx File',
    r'Correlation Hash \(i\.e\., \*\.co2mpas\.zip\)'
)
{% endif %}

# Load parameters to be verified.
params = {k: get_row(text, k) for k in keys}
params['DICE Receipt'] = [get_section(text, 'DICE RECEIPT', '\n\nVERIFICATION')]
key = load_key(get_section(text, 'Server Public Key', '$'))

# ------------------------------- VERIFICATION --------------------------------
{% if data_type == "co2mpas" and status_random == 0 %}
# Verify the hash of the random number signature.
error_message = 'The given hash is not equal to the signature hash!'
signature = bytes.fromhex(params['Server Random Number Signature'][0])
signature_hash = params['Server Random Number Signature Hash'][0]
assert make_hash(signature) == signature_hash, error_message
print('[VERIFIED] Hash of the random number signature.')

# Verify server random number.
error_message = 'The signature of the random number is not verified!'
message = ('[%s]' % params['Server Random Number'][0]).encode()
assert verify_sign(key, signature, message), error_message
print('[VERIFIED] Server random number.')

# Verify random number.
error_message = 'The final random number is not verified!'
n = int(params['Server Random Number'][0]) + int(params['User Random Number'][0])
assert n % 100 == int(params['Random Number'][0]), error_message
print('[VERIFIED] Random number.')
{% endif %}
# Verify the hash of the DICE RECEIPT.
error_message = 'The given hash is not equal to the signature hash!'
message = json.dumps(params['DICE Receipt']).encode()
message_hash = params['DICE Receipt Hash'][0]
assert make_hash(message) == message_hash, error_message
print('[VERIFIED] Hash of the DICE RECEIPT.')

# Verify signature of the DICE RECEIPT.
error_message = 'The signature of the DICE RECEIPT is not verified!'
signature = bytes.fromhex(params['DICE Receipt Signature'][0])
assert verify_sign(key, signature, message), error_message
print('[VERIFIED] Signature of the DICE RECEIPT.')

print('Well done! All data in the DICE RECEIPT (%s) are verified.' % fpath_dice)

# ------------------------ COMPLETE {{ data_type == 'co2mpas' and 'CORRELATION' or 'DICE' | safe }} FILE --------------------------

archive = {osp.basename(fpath_dice): text.encode()}
for i, fname in enumerate(params['Uploaded Filename']):
    name = '{}.%s'.format(osp.splitext(osp.basename(fname))[0])
    zp = name % 'zip'
    if not osp.isfile(osp.join(cdir, zp)):
        print("[WARNING] COMPLETE {{ data_type == 'co2mpas' and 'CORRELATION' or 'DICE' | safe }} FILE cannot be generated, "
              "because it is missing '%s' in '%s'." % (zp, cdir))
        break
    {% if data_type == "jet" %}
    files_hash = {
        name % 'ta': params[r'Hash of \*\.jet\.ta File'][i],
        name % 'input.xlsx': params[r'Hash of \*\.input\.xlsx File'][i],
        name % 'hash.txt': params[r'JET Hash \(i\.e\., \*\.jet\.zip\)'][i]
    }
    {% else %}
    files_hash = {
        name % 'ta': params[r'Hash of \*\.co2mpas\.ta File'][i],
        name % 'input.xlsx': params[r'Hash of \*\.input\.xlsx File'][i],
        name % 'output.xlsx': params[r'Hash of \*\.output\.xlsx File'][i],
        name % 'hash.txt': params[r'Correlation Hash \(i\.e\., \*\.co2mpas\.zip\)'][i]
    }
    {% endif %}
    # Verify hashes of the {{ data_type == 'co2mpas' and 'CORRELATION' or 'JET' | safe }} OUTPUT REPORT.
    with zipfile.ZipFile(osp.join(cdir, zp)) as zf:
        msg = "The content of the {{ data_type == 'co2mpas' and 'CORRELATION' or 'JET' | safe }} OUTPUT REPORT is not as expected!"
        assert {info.filename for info in zf.filelist} == set(files_hash), msg

        # Verify hashes of the {{ data_type == 'co2mpas' and 'CORRELATION' or 'JET' | safe }} OUTPUT REPORT.
        for fp, h in files_hash.items():
            with zf.open(fp, 'r') as f:
                archive[fp] = b = f.read()
            cond = fp.endswith('hash.txt') and b.decode() or make_hash(b) == h
            assert cond, "The file %s is corrupted due to '%s' hash!" % (zp, fp)

else:
    # Generate the COMPLETE {{ data_type == 'co2mpas' and 'CORRELATION' or 'DICE' | safe }} FILE.
    fpath = '%s.tar.bz2' % fpath_dice
    with tarfile.open(fpath, mode='w:bz2') as tar:
        for path, b in sorted(archive.items()):
            info = tarfile.TarInfo(path)
            info.size = len(b)
            tar.addfile(info, io.BytesIO(b))
        print("[INFO] Written COMPLETE {{ data_type == 'co2mpas' and 'CORRELATION' or 'DICE' | safe }} FILE (%s)." % fpath)
