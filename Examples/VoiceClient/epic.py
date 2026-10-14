import base64
import datetime
import uuid

import httpx

API = 'https://api.epicgames.dev'
PUBLIC_KEY_URL = 'https://publickey-service-prod.ecbc.live.use1a.on.epicgames.com/publickey/v2/publickey/'
USER_AGENT = 'EpicGamesLauncher/0.95.2+gfa9ad49 (windows)'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


class Epic:
    def __init__(self, token):
        self.token = token
        self.account_id = token['account_id']
        self.http = httpx.AsyncClient(base_url=API, timeout=30)

    def headers(self, **extra):
        return {
            'Authorization': 'Bearer ' + self.token['access_token'],
            'X-Epic-Agent': 'epic-social',
            'X-EPIC-CORRELATION-ID': str(uuid.uuid4()),
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT,
            **extra,
        }

    async def request(self, method, url, json=None, params=None, headers=None, ok=(200, 204)):
        r = await self.http.request(method, url, json=json, params=params, headers=headers or self.headers())
        if r.status_code not in ok:
            raise RuntimeError(f'{method} {url} -> {r.status_code} {r.text}')
        return r.json() if r.content else None

    async def party_summary(self):
        return await self.request('GET', f'/epic/party/internal/v2/users/{self.account_id}')

    async def leave_current_party(self):
        current = (await self.party_summary()).get('current')
        if current:
            await self.leave_party(current['id'])
        return current

    async def create_party(self, connection_id, connection_meta):
        body = {
            'config': {'joinability': 'INVITE_ONLY', 'max_size': 16},
            'meta': {'created_by': self.account_id},
            'join_info': {'connection': {'id': connection_id, 'deployment_id': '_', 'meta': connection_meta}},
        }
        return await self.request('POST', '/epic/party/internal/v2/parties', json=body)

    async def leave_party(self, party_id):
        return await self.request('DELETE', f'/epic/party/internal/v2/parties/{party_id}/members/{self.account_id}', ok=(200, 204, 404))

    async def invite(self, account_id):
        return await self.request('POST', f'/epic/party/internal/v2/users/{account_id}/invites/{self.account_id}', params={'auto': 'false'})

    async def set_presence(self, connection_id, party):
        body = {'status': 'online', 'party': party, 'conn': {'props': {}}}
        headers = self.headers(**{'X-HTTP-Method-Override': 'PATCH'})
        return await self.request('POST', f'/epic/presence/internal/v1/_/{self.account_id}/presence/{connection_id}', json=body, headers=headers)

    async def voice_credentials(self, party_id):
        r = await self.request('POST', f'/epic/party/internal/v2/parties/{party_id}/members/{self.account_id}/conferences/connection')
        return r['providers']['rtcp']

    async def update_member_meta(self, party_id, revision, connection_id, update, in_voice_room):
        body = {
            'revision': revision,
            'update': update,
            'connection': {'id': connection_id, 'deployment_id': '_', 'active_in_party_voice_room': in_voice_room},
        }
        return await self.request('PATCH', f'/epic/party/internal/v2/parties/{party_id}/members/{self.account_id}/meta', json=body)

    async def register_public_key(self, public_key):
        body = {'algorithm': 'ed25519', 'key': base64.b64encode(public_key).decode()}
        headers = {'Authorization': 'Bearer ' + self.token['access_token'], 'Content-Type': 'application/json'}
        return (await self.request('POST', PUBLIC_KEY_URL, json=body, headers=headers))['jwt']

    async def close(self):
        await self.http.aclose()
