from __future__ import print_function
import os
import base64

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from colorclass import Color
from terminaltables import AsciiTable

PRIVATE_KEY_FILENAME = os.environ.get('VT_PRIVATE_KEY') or os.path.expanduser('~/.ssh/id_rsa')

with open(PRIVATE_KEY_FILENAME, 'rb') as f:
    PRIVATE_KEY = f.read()

rsaObj = serialization.load_pem_private_key(PRIVATE_KEY, None, default_backend())

def print_table(data, title=None):
    if data:
        table = AsciiTable(data)
        if title:
            table.title = Color("{autoyellow}%(title)s{/autoyellow}" % {'title': title})
        table.inner_heading_row_border = False
        print(table.table)
    else:
        print(Color("{autored}No data found.{/autored}"))

def format_row(item, include_comments=False):
    row = []

    guid = '{autoblue}%s{/autoblue}' % item['guid'][:8]
    name = item['name']

    if item.get('comments'):
        name = '{automagenta}+ %s{/automagenta}' % name
    else:
        name = '{automagenta}  %s{/automagenta}' % name

    if item.get('done'):
        guid = '{strike}%s{/strike}' % guid
        name = '{strike}%s{/strike}' % name

    row.extend([Color(guid), Color(name)])

    if include_comments:
        comments = item.get('comments')

        if item.get('done'):
            comments = '{strike}%s{/strike}' % comments

        row.append(comments)
    return row

def get_encoded_signature(message):
    signature = rsaObj.sign(message,
                            padding.PSS(mgf=padding.MGF1(hashes.SHA512()),
                                        salt_length=padding.PSS.MAX_LENGTH),
                            hashes.SHA512())
    return base64.b64encode(signature)

