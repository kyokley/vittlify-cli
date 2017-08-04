import os
import requests
import json

from .utils import get_encoded_signature, VittlifyError

VITTLIFY_URL = os.environ.get('VT_URL') or 'http://127.0.0.1:8000/vittlify/'
USERNAME = os.environ.get('VT_USERNAME') or os.environ.get('USER')
PROXY = os.environ.get('VT_PROXY')
REQUEST_TIMEOUT = 5

def _get_proxy_dict(proxy):
    proxy_dict = {}
    if not proxy:
        return None

    split = proxy.split('://')
    if len(split) != 2:
        raise VittlifyError('Improperly formatted proxy')

    if split[0].lower() == 'socks5':
        proxy_dict.update({'http': proxy, 'https': proxy})
    else:
        proxy_dict[split[0]] = proxy
    return proxy_dict

def _send_request(method, data):
    data['username'] = USERNAME
    message = json.dumps(data)
    encoded_sig = get_encoded_signature(message.encode('utf-8'))

    payload = {'message': message,
               'signature': encoded_sig.decode('utf-8')}

    if method.lower() == 'get':
        resp = requests.get(VITTLIFY_URL + 'vt/',
                            json=payload,
                            proxies=_get_proxy_dict(PROXY),
                            timeout=REQUEST_TIMEOUT)
    elif method.lower() == 'put':
        resp = requests.put(VITTLIFY_URL + 'vt/',
                            json=payload,
                            proxies=_get_proxy_dict(PROXY),
                            timeout=REQUEST_TIMEOUT)
    elif method.lower() == 'post':
        resp = requests.post(VITTLIFY_URL + 'vt/',
                             json=payload,
                             proxies=_get_proxy_dict(PROXY),
                             timeout=REQUEST_TIMEOUT)

    if resp.status_code in (404, 409):
        raise VittlifyError(resp.json())

    resp.raise_for_status()
    return resp.json()

def get_all_shopping_lists():
    data = {'endpoint': 'all lists'}

    return _send_request('GET', data)

def get_shopping_list_info(guid):
    data = {'endpoint': 'list',
            'guid': guid,
            }
    return _send_request('GET', data)

def get_shopping_list_items(guid):
    data = {'endpoint': 'list items',
            'guid': guid,
            }
    return _send_request('GET', data)

def get_all_shopping_list_items(guid):
    data = {'endpoint': 'list all items',
            'guid': guid,
            }
    return _send_request('GET', data)

def get_completed():
    data = {'endpoint': 'completed',
            }
    return _send_request('GET', data)

def get_item(guid):
    data = {'endpoint': 'item',
            'guid': guid,
            }
    return _send_request('GET', data)

def complete_item(guid, uncomplete=False):
    data = {'endpoint': 'complete' if not uncomplete else 'uncomplete',
            'guid': guid,
            }
    return _send_request('PUT', data)

def modify_item(guid, comments):
    data = {'endpoint': 'modify',
            'guid': guid,
            'comments': comments}
    return _send_request('PUT', data)

def add_item(guid, name, comments=''):
    data = {'endpoint': 'add item',
            'guid': guid,
            'name': name,
            'comments': comments}
    return _send_request('POST', data)

def move_item(guid, to_guid):
    data = {'endpoint': 'move',
            'guid': guid,
            'to_list_guid': to_guid,
            }
    return _send_request('PUT', data)

def categorize_item(guid, category_name):
    data = {'endpoint': 'categorize',
            'guid': guid,
            'category_name': category_name,
            }
    return _send_request('PUT', data)
