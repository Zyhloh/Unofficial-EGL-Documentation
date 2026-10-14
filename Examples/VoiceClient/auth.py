import base64
import json
import os
import time

import httpx

TOKEN_URL = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
REDIRECT_URL = 'https://www.epicgames.com/id/api/redirect?clientId={}&responseType=code'


class Auth:
    def __init__(self, config):
        self.client_id = config['client']['id']
        self.client_secret = config['client']['secret']
        self.path = os.path.expanduser(config['tokenFile'])

    def basic(self):
        return 'basic ' + base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()

    def request(self, **form):
        form['token_type'] = 'eg1'
        r = httpx.post(TOKEN_URL, data=form, headers={'Authorization': self.basic()}, timeout=30)
        if r.status_code != 200:
            raise RuntimeError(f'token request failed {r.status_code}: {r.text}')
        token = r.json()
        token['saved_at'] = time.time()
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(token, f)
        return token

    def load(self):
        if not os.path.exists(self.path):
            return None
        with open(self.path, encoding='utf-8') as f:
            token = json.load(f)
        if token.get('client_id') != self.client_id:
            return None
        if time.time() < token['saved_at'] + token['expires_in'] - 300:
            return token
        if time.time() < token['saved_at'] + token['refresh_expires'] - 60:
            return self.request(grant_type='refresh_token', refresh_token=token['refresh_token'])
        return None

    def token(self):
        token = self.load()
        if token is not None:
            return token
        print('Sign in at https://www.epicgames.com, then open:')
        print(REDIRECT_URL.format(self.client_id))
        code = input('authorizationCode: ').strip().strip('"')
        return self.request(grant_type='authorization_code', code=code)
