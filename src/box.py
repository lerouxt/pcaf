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

class Box():

    def __init__(self, config=None):

        if not config:
            config = configparser.ConfigParser()
            config.read('box.cfg')
        self.CLIENT_ID = config.get('box', 'CLIENT_ID') # aka the API key
        self.CLIENT_SECRET= config.get('box', 'CLIENT_SECRET')
        self.PUBLIC_KEY_ID=config.get('box', 'PUBLIC_KEY_ID') # you must create a public/private key pair
        self.PRIVATE_KEY_FILE=config.get('box', 'PRIVATE_KEY_FILE')
        self.PRIVATE_KEY_PASSCODE=config.get('box', 'PRIVATE_KEY_PASSCODE').encode('ascii')
        self.ENTERPRISE_USER=config.get('box', 'ENTERPRISE_USER')


    def debug(self):
        import http.client as http_client
        import logging
        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
    #debug()

    def get_auth_token(self, user_id=None):
        """Gets an auth token for either the enterprise or a user.
        If user_id is null then it is assumed you are after the
        enterprise token.
        """

        # https://developer.box.com/v2.0/docs/construct-jwt-claim-manually

        box_sub_type = 'enterprise'
        if user_id is None:
            user_id = self.ENTERPRISE_USER
        else:
            box_sub_type = 'user'

        # extract private key
        with open(self.PRIVATE_KEY_FILE, 'rb') as kfile:
            pkeydata = kfile.read()
        pkey = load_pem_private_key(pkeydata, password=self.PRIVATE_KEY_PASSCODE, backend=default_backend())

        # encode payload
        ejwt = jwt.encode({
            'iss': self.CLIENT_ID,
            'sub': user_id,
            'box_sub_type': box_sub_type,
            'aud': 'https://api.box.com/oauth2/token',
            'jti': str(uuid.uuid1()),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            }, headers={
            'kid': self.PUBLIC_KEY_ID,
            'typ': 'JWT',
            'alg': 'RS256'
            }, key=pkey, algorithm='RS256')

        r = requests.post('https://api.box.com/oauth2/token', data={
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': ejwt,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET
            })

        r.raise_for_status()
        return r.json()['access_token']

    def create_app_user(self, user_name):
        headers = { 'Authorization': 'Bearer {}'.format(self.get_auth_token()) }
        data = '{{"name": "{}", "is_platform_access_only": true}}'.format(user_name)
        r = requests.post('https://api.box.com/2.0/users', data=data, headers=headers)
        r.raise_for_status()
        return r

    def get_folders(self, user_id):
        headers = { 'Authorization': 'Bearer {}'.format(self.get_auth_token(user_id)), }
        r = requests.get('https://api.box.com/2.0/folders/0', headers=headers)
        r.raise_for_status()
        return r

    def upload_file(self, user_id, directory_id, filename, boxfilename):
        headers = { 'Authorization': 'Bearer {}'.format(self.get_auth_token(user_id)), }
        data = '{{"name": "{}", "parent": {{ "id": "{}" }}}}'.format(boxfilename, directory_id)
        files = [ ('attributes', (None, data)),
                  ('file', ('file', open(filename, 'rb')))]
        r = requests.post('https://upload.box.com/api/2.0/files/content', headers=headers, files=files)
        r.raise_for_status()
        return r

    def upload_file_version(self, user_id, file_id, filename, boxfilename):
        headers = { 'Authorization': 'Bearer {}'.format(self.get_auth_token(user_id)), }
        data = '' if not filename else'{{"name": "{}"}}'.format(boxfilename)
        files = [ ('attributes', (None, data)),
                  ('file', ('file', open(filename, 'rb')))]
        r = requests.post('https://upload.box.com/api/2.0/files/{}/content'.format(file_id), headers=headers, files=files)
        r.raise_for_status()
        return r

if __name__ == "__main__":
    print(Box().get_auth_token())
