import argparse
import requests
import json
import sys
#import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
#from cryptography.exceptions import InvalidSignature

from colorclass import Color

from terminaltables import AsciiTable
from pprint import pprint

VITTLIFY_URL = 'http://127.0.0.1:8000/vittlify/'
PRIVATE_KEY_FILENAME = '/home/yokley/.ssh/id_rsa'
USERNAME = 'yokley'

with open(PRIVATE_KEY_FILENAME, 'rb') as f:
    PRIVATE_KEY = f.read()

rsaObj = serialization.load_pem_private_key(PRIVATE_KEY, None, default_backend())

def _get_all_shopping_lists():
    data = {'method': 'GET',
            'endpoint': 'all lists',
            'username': USERNAME}

    message = json.dumps(data)
    encoded_sig = _get_encoded_signature(message)

    payload = {'message': message,
               'signature': encoded_sig}
    resp = requests.get(VITTLIFY_URL + 'vt/',
                        json=payload)
    resp.raise_for_status()
    return resp.json()

def _get_shopping_list_info(guid):
    data = {'method': 'GET',
            'endpoint': 'list',
            'guid': guid,
            'username': USERNAME}

    message = json.dumps(data)
    encoded_sig = _get_encoded_signature(message)

    payload = {'message': message,
               'signature': encoded_sig}
    resp = requests.get(VITTLIFY_URL + 'vt/',
                        json=payload)
    resp.raise_for_status()
    return resp.json()

def _get_shopping_list_items(guid):
    data = {'method': 'GET',
            'endpoint': 'list items',
            'guid': guid,
            'username': USERNAME}

    message = json.dumps(data)
    encoded_sig = _get_encoded_signature(message)

    payload = {'message': message,
               'signature': encoded_sig}
    resp = requests.get(VITTLIFY_URL + 'vt/',
                        json=payload)
    resp.raise_for_status()
    return resp.json()

def display_shopping_list(guid, show_done=False):
    shopping_list = _get_shopping_list_info(guid)
    data = []
    for item in _get_shopping_list_items(guid):
        if (not show_done and not item['done']) or show_done:
            data.append([Color('{autoblue}%(guid)s{/autoblue}' % {'guid': item['guid'][:8]}),
                         item['name']])

    if data:
        table = AsciiTable(data)
        table.title = Color("{autoyellow}%(name)s{/autoyellow}" % {'name': shopping_list['name']})
        table.inner_heading_row_border = False
        print(table.table)
    else:
        print(Color("{autored}No data found.{/autored}"))

def display_all_shopping_lists():
    shopping_lists = _get_all_shopping_lists()
    data = []
    for shopping_list in shopping_lists:
        data.append([Color('{autoblue}%(guid)s{/autoblue}' % {'guid': shopping_list['guid'][:8]}),
                     shopping_list['name']])

    if data:
        table = AsciiTable(data)
        table.title = Color("{autoyellow}%(name)s{/autoyellow}" % {'name': 'All Lists'})
        table.inner_heading_row_border = False
        print(table.table)
    else:
        print(Color("{autored}No data found.{/autored}"))

def _get_encoded_signature(message):
    signature = rsaObj.sign(message,
                            padding.PSS(mgf=padding.MGF1(hashes.SHA512()),
                                        salt_length=padding.PSS.MAX_LENGTH),
                            hashes.SHA512())
    return base64.b64encode(signature)

def main():
    if sys.argv[1].lower() == 'show':
        if sys.argv[2].lower() == 'list':
            if len(sys.argv) != 4:
                raise ValueError('Incorrect number of arguments')
            display_shopping_list(sys.argv[3])
        elif sys.argv[2].lower() == 'lists':
            display_all_shopping_lists()

if __name__ == '__main__':
    main()
