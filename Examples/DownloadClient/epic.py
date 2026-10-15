import json

import httpx

LIBRARY = 'https://library-service.live.use1a.on.epicgames.com/library/api/public'
CATALOG = 'https://catalog-public-service-prod06.ol.epicgames.com/catalog/api/shared/namespace'
LAUNCHER = 'https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public'
ACCOUNT = 'https://account-public-service-prod.ol.epicgames.com/account/api'
ECOMMERCE = 'https://ecommerceintegration-public-service-ecomprod02.ol.epicgames.com/ecommerceintegration/api/public'
STORE_CONTENT = 'https://store-content.ak.epicgames.com/api'
USER_AGENT = 'EpicGamesLauncher/0.95.2+gfa9ad49 (windows)'


class Epic:
    def __init__(self, token, platform='Windows', label='Live'):
        self.token = token
        self.platform = platform
        self.label = label
        self.http = httpx.Client(timeout=60, headers={'User-Agent': USER_AGENT})

    def request(self, method, url, ok=(200,), **kwargs):
        headers = {'Authorization': 'Bearer ' + self.token['access_token']}
        r = self.http.request(method, url, headers=headers, **kwargs)
        if r.status_code not in ok:
            raise EpicError(r.status_code, r.text, url)
        return r.json() if r.content else None

    def library(self):
        records = []
        cursor = None
        while True:
            params = {'includeMetadata': 'true', 'limit': '100'}
            if cursor:
                params['cursor'] = cursor
            page = self.request('GET', f'{LIBRARY}/v2/items', params=params)
            records += page['records']
            cursor = page.get('responseMetadata', {}).get('nextCursor')
            if not cursor:
                return records

    def catalog_items(self, namespace, item_ids, country='US', locale='en'):
        items = {}
        ids = list(dict.fromkeys(item_ids))
        for i in range(0, len(ids), 50):
            params = [('id', x) for x in ids[i:i + 50]]
            params += [('includeDLCDetails', 'true'), ('includeMainGameDetails', 'true'), ('country', country), ('locale', locale)]
            items.update(self.request('GET', f'{CATALOG}/{namespace}/bulk/items', params=params))
        return items

    def asset(self, namespace, item_id, app_name):
        url = f'{LAUNCHER}/assets/v2/platform/{self.platform}/namespace/{namespace}/catalogItem/{item_id}/app/{app_name}/label/{self.label}'
        return self.request('GET', url)['elements'][0]

    def app_info(self, apps):
        body = {'appKeys': [{'artifactId': a['appName'], 'catalogId': a['catalogItemId'], 'sandboxId': a['namespace']} for a in apps]}
        return self.request('POST', f'{LAUNCHER}/assets/platform/{self.platform}/label/{self.label}/appInfo', json=body)

    def sidecars(self, apps):
        body = [{'namespace': a['namespace'], 'catalogItemId': a['catalogItemId'], 'appName': a['appName']} for a in apps]
        return self.request('PUT', f'{LAUNCHER}/assets/bulk/sidecars', json=body)['data']

    def dependency_config(self, namespace, item_id, app_name, build_version):
        try:
            return self.request('GET', f'{LAUNCHER}/artifactDependencies/v1/config/{namespace}/{item_id}/{app_name}/{build_version}')
        except EpicError as e:
            if e.status == 404:
                return None
            raise

    def exchange_code(self):
        return self.request('GET', f'{ACCOUNT}/oauth/exchange')['code']

    def ownership_token(self, namespace, item_id):
        url = f'{ECOMMERCE}/platforms/EPIC/identities/{self.token["account_id"]}/ownershipToken'
        return self.request('POST', url, data={'nsCatalogItemId': f'{namespace}:{item_id}'}).get('token')

    def external_auths(self):
        return self.request('GET', f'{ACCOUNT}/public/account/{self.token["account_id"]}/externalAuths')

    def account(self):
        return self.request('GET', f'{ACCOUNT}/public/account/{self.token["account_id"]}')

    def product_mapping(self):
        r = self.http.get(f'{STORE_CONTENT}/content/productmapping')
        r.raise_for_status()
        return r.json()

    def product_content(self, slug, locale='en-US'):
        r = self.http.get(f'{STORE_CONTENT}/{locale}/content/products/{slug}')
        return r.json() if r.status_code == 200 else None

    def selective_download_meta(self, element):
        sd = element.get('selectiveDownload') or []
        if not sd:
            return None
        meta = sd[0]
        query = '&'.join(f"{q['name']}={q['value']}" for q in meta.get('queryParams', []))
        r = self.http.get(meta['uri'] + ('?' + query if query else ''))
        r.raise_for_status()
        return json.loads(r.content)


class EpicError(Exception):
    def __init__(self, status, body, url):
        super().__init__(f'{status} {url} {body[:300]}')
        self.status = status
        self.body = body
        try:
            self.code = json.loads(body).get('errorCode')
        except ValueError:
            self.code = None
