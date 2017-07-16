from __future__ import print_function
import os
import base64
import re

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from colorclass import Color
from terminaltables import AsciiTable, BorderlessTable

class VittlifyError(Exception):
    pass

def print_table(data, title=None):
    if data:
        table = AsciiTable(data)
        if title:
            table.title = Color("{autoyellow}%(title)s{/autoyellow}" % {'title': title})
        table.inner_heading_row_border = False
        print(table.table)
    else:
        print(Color("{autored}No data found.{/autored}"))

def _apply_strikethrough(string):
    string = re.sub(r'(?:^|(?<=[\s}]))(\S+)(?=[\s{]|$)', r'{strike}\1{/strike}', string)
    return string

def format_row(item, include_comments=False):
    row = []

    comments = item.get('comments')

    if comments:
        name = '+ %s' % item['name']
    else:
        name = '  %s' % item['name']

    if item.get('done'):
        guid = '{autoblue}%s{/autoblue}' % _apply_strikethrough(item['guid'][:8])
        name = '{automagenta}%s{/automagenta}' % _apply_strikethrough(name)
        if comments:
            comments = _apply_strikethrough(comments)
    else:
        guid = '{autoblue}%s{/autoblue}' % item['guid'][:8]
        name = '{automagenta}%s{/automagenta}' % name

    row.extend([Color(guid), Color(name)])

    if include_comments and comments:
        comments = Color(comments)
        row.append(comments)
    return row

def get_encoded_signature(message):
    PRIVATE_KEY_FILENAME = os.environ.get('VT_PRIVATE_KEY') or os.path.expanduser('~/.ssh/id_rsa')

    try:
        with open(PRIVATE_KEY_FILENAME, 'rb') as f:
            PRIVATE_KEY = f.read()
    except IOError:
        raise VittlifyError('Could not find private key at %s' % PRIVATE_KEY_FILENAME)

    rsaObj = serialization.load_pem_private_key(PRIVATE_KEY, None, default_backend())

    signature = rsaObj.sign(message,
                            padding.PSS(mgf=padding.MGF1(hashes.SHA512()),
                                        salt_length=padding.PSS.MAX_LENGTH),
                            hashes.SHA512())
    return base64.b64encode(signature)

def parse_options(raw_options):
    options = {}
    for val in raw_options:
        arg = val.strip()
        if arg.startswith('--'):
            if arg == '--extended':
                options['extended'] = True
            elif arg == '--quiet':
                options['quiet'] = True
        elif arg.startswith('-'):
            if 'e' in arg:
                options['extended'] = True

            if 'q' in arg:
                options['quiet'] = True

    return options
