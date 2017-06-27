import requests
import json
import sys
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from colorclass import Color

from terminaltables import AsciiTable

VITTLIFY_URL = 'http://127.0.0.1:8000/vittlify/'
PRIVATE_KEY_FILENAME = '/home/yokley/.ssh/id_rsa'
USERNAME = 'yokley'

with open(PRIVATE_KEY_FILENAME, 'rb') as f:
    PRIVATE_KEY = f.read()

rsaObj = serialization.load_pem_private_key(PRIVATE_KEY, None, default_backend())

class VittlifyError(Exception):
    pass

def _send_request(data):
    message = json.dumps(data)
    encoded_sig = _get_encoded_signature(message)

    payload = {'message': message,
               'signature': encoded_sig}
    resp = requests.get(VITTLIFY_URL + 'vt/',
                        json=payload)

    if resp.status_code == 409:
        raise VittlifyError(resp.json())

    resp.raise_for_status()
    return resp.json()

def _get_all_shopping_lists():
    data = {'method': 'GET',
            'endpoint': 'all lists',
            'username': USERNAME}

    return _send_request(data)

def _get_shopping_list_info(guid):
    data = {'method': 'GET',
            'endpoint': 'list',
            'guid': guid,
            'username': USERNAME}
    return _send_request(data)

def _get_shopping_list_items(guid):
    data = {'method': 'GET',
            'endpoint': 'list items',
            'guid': guid,
            'username': USERNAME}
    return _send_request(data)

def _get_item(guid):
    data = {'method': 'GET',
            'endpoint': 'item',
            'guid': guid,
            'username': USERNAME}
    return _send_request(data)

def display_shopping_list(guid, show_done=False, extended=False):
    shopping_list = _get_shopping_list_info(guid)
    data = []
    for item in _get_shopping_list_items(guid):
        if (not show_done and not item['done']) or show_done:
            name = '+ ' + item['name'] if item['comments'] else '  ' + item['name']
            row = [Color('{autoblue}%(guid)s{/autoblue}' % {'guid': item['guid'][:8]}),
                   name]
            if extended:
                row.append(item['comments'])

            data.append(row)

    print_table(data, title=shopping_list['name'])

def display_item(guid):
    item = _get_item(guid)
    data = []
    data.append([Color('{autoblue}%(guid)s{/autoblue}' % {'guid': item['guid'][:8]}),
                 item['name'],
                 item['comments']])
    print_table(data)

def display_all_shopping_lists():
    shopping_lists = _get_all_shopping_lists()
    data = []
    for shopping_list in shopping_lists:
        data.append([Color('{autoblue}%(guid)s{/autoblue}' % {'guid': shopping_list['guid'][:8]}),
                     shopping_list['name']])

    print_table(data, title='All Lists')

def print_table(data, title=None):
    if data:
        table = AsciiTable(data)
        if title:
            table.title = Color("{autoyellow}%(title)s{/autoyellow}" % {'title': title})
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
            if len(sys.argv) not in (4, 5):
                raise ValueError('Incorrect number of arguments')
            try:
                if len(sys.argv) == 5 and sys.argv[4].lower() == 'extended':
                    display_shopping_list(sys.argv[3], extended=True)
                else:
                    display_shopping_list(sys.argv[3])
            except VittlifyError as e:
                print(Color("{autored}%s{/autored}" % e))
        elif sys.argv[2].lower() == 'lists':
            try:
                display_all_shopping_lists()
            except VittlifyError as e:
                print(Color("{autored}%s{/autored}" % e))
        elif sys.argv[2].lower() == 'item':
            if len(sys.argv) != 4:
                raise ValueError('Incorrect number of arguments')
            try:
                display_item(sys.argv[3])
            except VittlifyError as e:
                print(Color("{autored}%s{/autored}" % e))

if __name__ == '__main__':
    main()
