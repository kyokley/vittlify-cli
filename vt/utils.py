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

def get_encoded_signature(message):
    signature = rsaObj.sign(message,
                            padding.PSS(mgf=padding.MGF1(hashes.SHA512()),
                                        salt_length=padding.PSS.MAX_LENGTH),
                            hashes.SHA512())
    return base64.b64encode(signature)

