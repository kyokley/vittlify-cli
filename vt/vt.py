import requests
import json
#import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
#from cryptography.exceptions import InvalidSignature

VITTLIFY_URL = 'http://127.0.0.1:8000/vittlify/'
PRIVATE_KEY_FILENAME = '/home/yokley/.ssh/id_rsa'
USERNAME = 'yokley'

with open(PRIVATE_KEY_FILENAME, 'rb') as f:
    PRIVATE_KEY = f.read()

rsaObj = serialization.load_pem_private_key(PRIVATE_KEY, None, default_backend())

def get_items(list_name):
    data = {'method': 'GET',
            'endpoint': 'all lists',
            'username': USERNAME}

    message = json.dumps(data)
    signature = rsaObj.sign(message,
                            padding.PSS(mgf=padding.MGF1(hashes.SHA512()),
                                        salt_length=padding.PSS.MAX_LENGTH),
                            hashes.SHA512())
    encoded_sig = base64.b64encode(signature)
    payload = {'message': message,
               'signature': encoded_sig}
    resp = requests.get(VITTLIFY_URL + 'vt/',
                        json=payload)
    import pdb; pdb.set_trace()
    print resp

if __name__ == '__main__':
    get_items('work')
