#!/usr/bin/env python3
"""Provides a lightweight Python lib around the box.com API

All configurations should be stored in the box.cfg file
"""

import requests
import jwt
import datetime
import uuid
import configparser
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend

config = configparser.ConfigParser()
config.read('box.cfg')
CLIENT_ID = config.get('box', 'CLIENT_ID') # aka the API key
CLIENT_SECRET= config.get('box', 'CLIENT_SECRET')
PUBLIC_KEY_ID=config.get('box', 'PUBLIC_KEY_ID') # you must create a public/private key pair
PRIVATE_KEY_FILE=config.get('box', 'PRIVATE_KEY_FILE')
PRIVATE_KEY_PASSCODE=config.get('box', 'PRIVATE_KEY_PASSCODE').encode('ascii')
ENTERPRISE_USER=config.get('box', 'ENTERPRISE_USER')

# https://developer.box.com/v2.0/docs/construct-jwt-claim-manually

def debug():
    import http.client as http_client
    import logging
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
#debug()

def get_auth_token(user_id=None):
    """Gets an auth token for either the enterprise or a user.
    If user_id is null then it is assumed you are after the
    enterprise token.
    """

    box_sub_type = 'enterprise'
    if user_id is None:
        user_id = ENTERPRISE_USER
    else:
        box_sub_type = 'user'

    # extract private key
    with open(PRIVATE_KEY_FILE, 'rb') as kfile:
        pkeydata = kfile.read()
    pkey = load_pem_private_key(pkeydata, password=PRIVATE_KEY_PASSCODE, backend=default_backend())

    # encode payload
    ejwt = jwt.encode({
        'iss': CLIENT_ID,
        'sub': user_id,
        'box_sub_type': box_sub_type,
        'aud': 'https://api.box.com/oauth2/token',
        'jti': str(uuid.uuid1()),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
        }, headers={
        'kid': PUBLIC_KEY_ID,
        'typ': 'JWT',
        'alg': 'RS256'
        }, key=pkey, algorithm='RS256')

    r = requests.post('https://api.box.com/oauth2/token', data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': ejwt,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
        })

    r.raise_for_status()
    return r.json()['access_token']

def create_app_user(user_name):
    headers = { 'Authorization': 'Bearer {}'.format(get_auth_token()) }
    data = '{{"name": "{}", "is_platform_access_only": true}}'.format(user_name)
    r = requests.post('https://api.box.com/2.0/users', data=data, headers=headers)
    r.raise_for_status()
    return r

def get_folders(user_id):
    headers = { 'Authorization': 'Bearer {}'.format(get_auth_token(user_id)), }
    r = requests.get('https://api.box.com/2.0/folders/0', headers=headers)
    r.raise_for_status()
    return r

def upload_file(user_id, filename, boxfilename, directory_id=0):
    headers = { 'Authorization': 'Bearer {}'.format(get_auth_token(user_id)), }
    data = '{{"name": "{}", "parent": {{ "id": "{}" }}}}'.format(boxfilename, directory_id)
    files = [ ('attributes', (None, data)),
              ('file', ('file', open(filename, 'rb')))]
    r = requests.post('https://upload.box.com/api/2.0/files/content', headers=headers, files=files)
    r.raise_for_status()
    return r

if __name__ == "__main__":
    print(get_auth_token())
