import os
import requests
import json

from utils import get_encoded_signature

VITTLIFY_URL = os.environ.get('VT_URL') or 'http://127.0.0.1:8000/vittlify/'
USERNAME = os.environ.get('VT_USERNAME') or os.environ.get('USER')

class VittlifyError(Exception):
    pass

def _send_request(data):
    message = json.dumps(data)
    encoded_sig = get_encoded_signature(message)

    payload = {'message': message,
               'signature': encoded_sig}
    resp = requests.get(VITTLIFY_URL + 'vt/',
                        json=payload)

    if resp.status_code in (404, 409):
        raise VittlifyError(resp.json())

    resp.raise_for_status()
    return resp.json()

def get_all_shopping_lists():
    data = {'method': 'GET',
            'endpoint': 'all lists',
            'username': USERNAME}

    return _send_request(data)

def get_shopping_list_info(guid):
    data = {'method': 'GET',
            'endpoint': 'list',
            'guid': guid,
            'username': USERNAME}
    return _send_request(data)

def get_shopping_list_items(guid):
    data = {'method': 'GET',
            'endpoint': 'list items',
            'guid': guid,
            'username': USERNAME}
    return _send_request(data)

def get_item(guid):
    data = {'method': 'GET',
            'endpoint': 'item',
            'guid': guid,
            'username': USERNAME}
    return _send_request(data)

