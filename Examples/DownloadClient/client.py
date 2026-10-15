import json
import os
import shlex
import subprocess
import sys
import uuid
from urllib.parse import quote

import manifest as mf
from engine import Engine, fetch_delta, fetch_manifest, merge_delta, select_files, verify
from epic import Epic, EpicError


def attrs(item):
    return {k: v.get('value') for k, v in (item.get('customAttributes') or {}).items()}


def flag(value):
    return value is True or str(value).lower() == 'true'


def categories(item):
    return [c['path'] for c in item.get('categories', [])]


def kind(item):
    cats = categories(item)
    a = attrs(item)
    if item.get('mainGameItem'):
        return 'addon'
    if 'ThirdPartyManagedApp' in a:
        return 'external:' + a['ThirdPartyManagedApp']
    if 'ThirdPartyManagedProvider' in a:
        return 'thirdparty:' + a['ThirdPartyManagedProvider']
    if any(c.startswith('engines') for c in cats):
        return 'engine'
    if any(c.startswith('plugins') for c in cats):
        return 'plugin'
    if 'software' in cats and 'games' not in cats:
        return 'app'
    return 'game'


class State:
    def __init__(self, path):
        self.path = os.path.expanduser(path)
        self.data = {'installs': {}}
        if os.path.exists(self.path):
            with open(self.path, encoding='utf-8') as f:
                self.data = json.load(f)

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def get(self, app_name):
        return self.data['installs'].get(app_name)

    def put(self, entry):
        self.data['installs'][entry['appName']] = entry
        self.save()

    def remove(self, app_name):
        self.data['installs'].pop(app_name, None)
        self.save()

    def children(self, installation_id):
        return [e for e in self.data['installs'].values() if e.get('parentInstallationId') == installation_id]


class Client:
    def __init__(self, config, token, progress=None):
        self.config = config
        self.epic = Epic(token, config['platform'], config['label'])
        self.state = State(config['stateFile'])
        self.engine = Engine(
            workers=config['workers'],
            retries=config['retries'],
            memory_limit_mb=config['memoryLimitMB'],
            speed_limit=config['speedLimitBytesPerSecond'],
            progress=progress,
        )
        self.cache = None

    def library(self, refresh=False):
        if self.cache is not None and not refresh:
            return self.cache
        records = [r for r in self.epic.library() if r.get('appName') and r.get('catalogItemId')]
        by_namespace = {}
        for r in records:
            by_namespace.setdefault(r['namespace'], []).append(r['catalogItemId'])
        items = {}
        for namespace, ids in by_namespace.items():
            items.update(self.epic.catalog_items(namespace, ids))
        self.cache = [dict(r, item=items.get(r['catalogItemId'], {})) for r in records]
        return self.cache

    def find(self, query):
        lib = self.library()
        for r in lib:
            if r['appName'] == query or r['catalogItemId'] == query:
                return r
        q = query.lower()
        hits = [r for r in lib if q in r['item'].get('title', '').lower()]
        if len(hits) == 1:
            return hits[0]
        if not hits:
            raise SystemExit(f'not in library: {query}')
        raise SystemExit('ambiguous: ' + ', '.join(f"{h['item'].get('title')} ({h['appName']})" for h in hits[:10]))

    def parent_of(self, record):
        main = record['item'].get('mainGameItem')
        if not main:
            return None
        for r in self.library():
            if r['catalogItemId'] == main['id'] and r['namespace'] == record['namespace']:
                return r
        return None

    def addons(self, record):
        ids = [d['id'] for d in record['item'].get('dlcItemList') or []]
        if not ids:
            return []
        items = self.epic.catalog_items(record['namespace'], ids)
        out = []
        for item_id, item in items.items():
            app = next((ri['appId'] for ri in item.get('releaseInfo') or [] if self.epic.platform in (ri.get('platform') or [])), None)
            if not app:
                continue
            try:
                element = self.epic.asset(record['namespace'], item_id, app)
                status = 'available'
            except EpicError as e:
                element = None
                status = 'not entitled' if e.code == 'errors.com.epicgames.launcher.not_entitled' else f'error {e.status}'
            out.append({'title': item.get('title'), 'appName': app, 'catalogItemId': item_id, 'status': status, 'element': element, 'categories': categories(item), 'installed': bool(self.state.get(app))})
        return out

    def describe(self, record):
        try:
            element = self.epic.asset(record['namespace'], record['catalogItemId'], record['appName'])
        except EpicError as e:
            managed = attrs(record['item']).get('ThirdPartyManagedApp')
            if e.code == 'errors.com.epicgames.launcher.download_info_not_found' and managed:
                raise SystemExit(f"{record['item'].get('title')} has no Epic build, it is installed and launched through {managed}")
            raise
        raw = fetch_manifest(element)
        m = mf.parse(raw)
        files = m['files']['list']
        tags = sorted({t for f in files for t in f['installTags']})
        return {
            'title': record['item'].get('title'),
            'kind': kind(record['item']),
            'element': element,
            'manifest': m,
            'raw': raw,
            'tags': tags,
            'installSize': sum(f['size'] for f in files),
            'downloadSize': sum(c['fileSize'] for c in m['chunks']['list']),
            'attributes': attrs(record['item']),
            'components': self.components(element),
        }

    def components(self, element):
        meta = self.epic.selective_download_meta(element)
        if not meta:
            return []
        return [{'id': c['UniqueId'], 'title': c.get('Title'), 'tags': c.get('Tags', []), 'required': flag(c.get('IsRequired')), 'default': flag(c.get('IsDefaultSelected'))} for c in meta.get('Data', [])]

    def install_dir(self, record, base=None):
        parent = self.parent_of(record)
        if parent:
            installed = self.state.get(parent['appName'])
            if not installed:
                raise SystemExit(f"install the base game first: {parent['item'].get('title')} ({parent['appName']})")
            return installed['dir'], installed
        folder = attrs(record['item']).get('FolderName') or record['appName']
        return os.path.join(os.path.expanduser(base or self.config['installRoot']), folder), None

    def resolve_tags(self, info, tags=None, components=None):
        if tags is not None:
            return tags
        comps = info['components']
        if not comps:
            return None
        chosen = [c for c in comps if c['required'] or (c['id'] in components if components is not None else c['default'])]
        return sorted({t for c in chosen for t in c['tags']})

    def prepare(self, query, base=None, tags=None, components=None):
        record = self.find(query)
        info = self.describe(record)
        existing = self.state.get(record['appName'])
        target, parent = self.install_dir(record, base)
        if existing:
            target = existing['dir']
        old = None
        if existing:
            old_path = os.path.join(existing['dir'], '.egstore', existing['installationId'] + '.manifest')
            if os.path.exists(old_path):
                with open(old_path, 'rb') as f:
                    old = mf.parse(f.read())
            if tags is None and components is None:
                tags = existing.get('tags')
        selected = self.resolve_tags(info, tags, components)
        protected = self.owned_by_others(target, existing['installationId'] if existing else None)
        source = info['manifest']
        delta = None
        if old:
            delta = fetch_delta(info['element'], old['meta'].get('buildId'), info['manifest']['meta'].get('buildId'))
            if delta:
                source = merge_delta(info['manifest'], mf.parse(delta))
        plan = self.engine.plan(source, target, old, selected, existing.get('tags') if existing else None, protected, self.config['updateCheck'])
        summary = {
            'title': info['title'],
            'kind': info['kind'],
            'dir': target,
            'from': existing['version'] if existing else None,
            'to': info['element']['buildVersion'],
            'files': len(plan['files']),
            'unchanged': len(plan['keep']),
            'write': len(plan['todo']),
            'remove': len(plan['removed']),
            'chunks': len(plan['download']),
            'downloadSize': plan['downloadSize'],
            'reuseSize': plan['reuseSize'],
            'installSize': plan['installSize'],
            'tags': selected,
            'delta': bool(delta),
        }
        return {'record': record, 'info': info, 'source': source, 'plan': plan, 'dir': target, 'parent': parent, 'existing': existing, 'tags': selected, 'summary': summary}

    async def commit(self, job, run_prereqs=False):
        record, info, plan, target, parent, existing, selected = job['record'], job['info'], job['plan'], job['dir'], job['parent'], job['existing'], job['tags']
        os.makedirs(os.path.join(target, '.egstore'), exist_ok=True)
        await self.engine.apply(info['element'], job['source'], plan, target)
        installation_id = existing['installationId'] if existing else uuid.uuid4().hex.upper()
        with open(os.path.join(target, '.egstore', installation_id + '.manifest'), 'wb') as f:
            f.write(info['raw'])
        meta = info['manifest']['meta']
        entry = {
            'installationId': installation_id,
            'title': info['title'],
            'kind': info['kind'],
            'appName': record['appName'],
            'namespace': record['namespace'],
            'catalogItemId': record['catalogItemId'],
            'dir': target,
            'version': info['element']['buildVersion'],
            'tags': selected,
            'launchExecutable': meta.get('launchExe') or '',
            'launchCommand': meta.get('launchCommand') or '',
            'prereq': {'ids': meta.get('prereqIds') or [], 'path': meta.get('prereqPath') or '', 'args': meta.get('prereqArgs') or '', 'name': meta.get('prereqName') or ''},
            'uninstallAction': {'path': meta.get('uninstallActionPath') or '', 'args': meta.get('uninstallActionArgs') or ''},
            'attributes': info['attributes'],
            'parentInstallationId': parent['installationId'] if parent else None,
            'prereqsDone': existing.get('prereqsDone', []) if existing else [],
        }
        if run_prereqs:
            self.run_prereqs(entry)
        self.state.put(entry)
        return entry

    def import_egl(self, path=None):
        path = path or os.path.join(os.environ.get('LOCALAPPDATA', ''), 'com.epicgames.eglv2', 'installations.jsonl')
        latest = {}
        with open(path, encoding='utf-8') as f:
            for line in f.read().splitlines()[1:]:
                e = json.loads(line)
                if e.get('complete'):
                    latest[e['installationId']] = e
        imported = []
        for e in latest.values():
            manifest_path = os.path.join(e['dir'], '.egstore', e['installationId'] + '.manifest')
            if not os.path.exists(manifest_path):
                continue
            with open(manifest_path, 'rb') as f:
                meta = mf.parse(f.read())['meta']
            record = next((r for r in self.library() if r['appName'] == e['artifactId'] and r['catalogItemId'] == e['itemId']), None)
            item = record['item'] if record else {}
            self.state.put({
                'installationId': e['installationId'],
                'title': item.get('title', e['artifactId']),
                'kind': kind(item) if item else 'game',
                'appName': e['artifactId'],
                'namespace': e['namespace'],
                'catalogItemId': e['itemId'],
                'dir': e['dir'],
                'version': e['version'],
                'tags': [t for t in e.get('tags') or []] or None,
                'launchExecutable': e.get('launchExecutable') or meta.get('launchExe') or '',
                'launchCommand': e.get('launchCommand') or meta.get('launchCommand') or '',
                'prereq': {'ids': meta.get('prereqIds') or [], 'path': meta.get('prereqPath') or '', 'args': meta.get('prereqArgs') or '', 'name': meta.get('prereqName') or ''},
                'uninstallAction': {'path': meta.get('uninstallActionPath') or '', 'args': meta.get('uninstallActionArgs') or ''},
                'attributes': attrs(item),
                'parentInstallationId': e.get('parentInstallationId'),
                'prereqsDone': [],
            })
            imported.append(e['artifactId'])
        return imported

    def run_prereqs(self, entry):
        p = entry['prereq']
        if not p['path']:
            return
        key = ','.join(p['ids']) or p['path']
        if key in entry['prereqsDone']:
            return
        run_elevated(os.path.join(entry['dir'], p['path']), p['args'], entry['dir'])
        entry['prereqsDone'].append(key)

    def launch_args(self, record, entry, extra=None):
        a = attrs(record['item'])
        me = self.epic.token['account_id']
        account = self.epic.account()
        game = shlex.split(entry['launchCommand'], posix=False) if entry and entry['launchCommand'] else []
        additional = shlex.split(a.get('AdditionalCommandLine') or a.get('AdditionalCommandline') or '', posix=False)
        epicapp = next((x.split('=', 1)[1] for x in additional if x.lower().startswith('-epicapp=')), record['appName'])
        additional = [x for x in additional if not x.lower().startswith('-epicapp=')]
        args = [
            '-AUTH_LOGIN=unused',
            '-AUTH_PASSWORD=' + self.epic.exchange_code(),
            '-AUTH_TYPE=exchangecode',
        ]
        args += game + additional + (extra or [])
        args += ['-epicapp=' + epicapp, '-epicenv=Prod']
        if a.get('OwnershipToken') == 'true' and entry:
            args.append('-epicovt=' + self.write_ovt(record, entry))
        deployment = self.deployment_id(record)
        if deployment:
            args.append('-epicdeploymentid=' + deployment)
        args += [
            '-EpicPortal',
            '-epicusername=' + account['displayName'],
            '-epicuserid=' + me,
            '-epiclocale=' + self.config['locale'].split('-')[0],
            '-epicsandboxid=' + record['namespace'],
        ]
        return args

    def write_ovt(self, record, entry):
        token = self.epic.ownership_token(record['namespace'], record['catalogItemId'])
        folder = os.path.join(entry['dir'], '.egstore', self.epic.token['account_id'])
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, record['namespace'] + record['catalogItemId'] + '.ovt')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(token or '')
        return path

    def deployment_id(self, record):
        for sidecar in self.epic.sidecars([record]):
            if sidecar['appName'] == record['appName']:
                return json.loads(sidecar['config']).get('deploymentId')
        return None

    def partner_uri(self, record):
        a = attrs(record['item'])
        me = self.epic.token['account_id']
        if 'ThirdPartyManagedApp' in a:
            account = self.epic.account()
            query = f"AUTH_PASSWORD={self.epic.exchange_code()}&AUTH_TYPE=exchangecode&epicusername={quote(account['displayName'])}&epicuserid={me}&epiclocale={self.config['locale']}"
            return f"link2ea://launchgame/{record['appName']}?{query}{a.get('AdditionalCommandLine') or a.get('AdditionalCommandline') or ''}"
        if a.get('ThirdPartyManagedProvider') == 'UbisoftConnect' and a.get('GameID'):
            return f"uplay://launch/{a['GameID']}/0?exchangecode={self.epic.exchange_code()}&epicuid={me}&source=epic"
        return None

    def launch(self, query, extra=None, dry_run=False):
        record = self.find(query)
        uri = self.partner_uri(record)
        if uri:
            if not dry_run:
                os.startfile(uri)
            return {'uri': uri}
        entry = self.state.get(record['appName'])
        if not entry:
            raise SystemExit('not installed')
        exe = os.path.join(entry['dir'], entry['launchExecutable'])
        args = self.launch_args(record, entry, extra)
        if not dry_run:
            subprocess.Popen([exe] + args, cwd=os.path.dirname(exe))
        return {'exe': exe, 'args': args}

    def check_updates(self):
        installed = list(self.state.data['installs'].values())
        if not installed:
            return []
        apps = [{'appName': e['appName'], 'catalogItemId': e['catalogItemId'], 'namespace': e['namespace']} for e in installed]
        live = {a['appName']: a for a in self.epic.app_info(apps)}
        out = []
        for e in installed:
            remote = live.get(e['appName'])
            never = e['attributes'].get('NeverUpdate') == 'true'
            out.append({'appName': e['appName'], 'title': e['title'], 'installed': e['version'], 'live': remote['buildVersion'] if remote else None, 'update': bool(remote) and remote['buildVersion'] != e['version'] and not never, 'neverUpdate': never})
        return out

    def verify(self, query, repair=False):
        record = self.find(query)
        entry = self.state.get(record['appName'])
        if not entry:
            raise SystemExit('not installed')
        with open(os.path.join(entry['dir'], '.egstore', entry['installationId'] + '.manifest'), 'rb') as f:
            m = mf.parse(f.read())
        bad = verify(entry['dir'], m, entry['tags'])
        return bad

    async def repair(self, query):
        record = self.find(query)
        entry = self.state.get(record['appName'])
        with open(os.path.join(entry['dir'], '.egstore', entry['installationId'] + '.manifest'), 'rb') as f:
            m = mf.parse(f.read())
        bad = {name for _, name in verify(entry['dir'], m, entry['tags'])}
        if not bad:
            return 0
        element = self.epic.asset(entry['namespace'], entry['catalogItemId'], entry['appName'])
        if element['buildVersion'] != entry['version']:
            raise SystemExit('a newer build is live, run install to update instead')
        plan = self.engine.plan(m, entry['dir'], tags=entry['tags'])
        plan['todo'] = [f for f in plan['todo'] if f['filename'] in bad]
        chunks = {c['guid']: c for c in m['chunks']['list']}
        plan['download'] = {p['guid']: chunks[p['guid']] for f in plan['todo'] for p in f['chunkParts']}
        plan['sources'] = {}
        plan['removed'] = []
        await self.engine.apply(element, m, plan, entry['dir'])
        return len(bad)

    def uninstall(self, query, run_action=False):
        record = self.find(query)
        entry = self.state.get(record['appName'])
        if not entry:
            raise SystemExit('not installed')
        for child in self.state.children(entry['installationId']):
            self.remove_files(child)
            self.state.remove(child['appName'])
        action = entry['uninstallAction']
        if run_action and action['path']:
            subprocess.run([os.path.join(entry['dir'], action['path'])] + action['args'].split(), cwd=entry['dir'])
        self.remove_files(entry)
        self.state.remove(entry['appName'])

    def owned_by_others(self, directory, installation_id):
        owned = set()
        for other in self.state.data['installs'].values():
            if other['installationId'] == installation_id or os.path.normcase(os.path.abspath(other['dir'])) != os.path.normcase(os.path.abspath(directory)):
                continue
            path = os.path.join(other['dir'], '.egstore', other['installationId'] + '.manifest')
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    owned |= {x['filename'] for x in select_files(mf.parse(f.read()), other['tags'])}
        return owned

    def remove_files(self, entry):
        path = os.path.join(entry['dir'], '.egstore', entry['installationId'] + '.manifest')
        if not os.path.exists(path):
            return
        with open(path, 'rb') as f:
            m = mf.parse(f.read())
        protected = self.owned_by_others(entry['dir'], entry['installationId'])
        for f in select_files(m, entry['tags']):
            target = os.path.join(entry['dir'], f['filename'])
            if f['filename'] not in protected and os.path.isfile(target):
                os.remove(target)
        os.remove(path)
        for root, dirs, files in os.walk(entry['dir'], topdown=False):
            if not os.listdir(root):
                os.rmdir(root)

    def art(self, record, locale='en-US'):
        images = {k['type']: k['url'] for k in record['item'].get('keyImages', [])}
        out = {'cover': images.get('DieselGameBoxTall'), 'landscape': images.get('DieselGameBox'), 'wide': images.get('DieselGameBoxWide'), 'thumbnail': images.get('Thumbnail'), 'keyImages': images, 'slug': None, 'hero': None}
        slug = self.epic.product_mapping().get(record['namespace'])
        if not slug:
            return out
        out['slug'] = slug
        doc = self.epic.product_content(slug, locale)
        if not doc:
            return out
        pages = [p for p in doc.get('pages', []) if (p.get('data') or {}).get('hero')]
        hero = pages[0]['data']['hero'] if pages else {}
        out['hero'] = {
            'logo': (hero.get('logoImage') or {}).get('src'),
            'landscape': hero.get('backgroundImageUrl'),
            'portrait': hero.get('portraitBackgroundImageUrl'),
            'media': [(i.get('image') or {}).get('src') for p in pages for i in ((p['data'].get('carousel') or {}).get('items') or []) if (i.get('image') or {}).get('src')],
        }
        return out


def resized(url, width, height, quality='medium'):
    if not url:
        return None
    return f'{url}{"&" if "?" in url else "?"}resize=1&w={width}&h={height}&quality={quality}'


def run_elevated(path, args, cwd):
    if sys.platform != 'win32':
        subprocess.run([path] + shlex.split(args or ''), cwd=cwd, check=True)
        return
    script = f"$p = Start-Process -FilePath '{path}' -ArgumentList '{args or ' '}' -WorkingDirectory '{cwd}' -Verb RunAs -WindowStyle Hidden -Wait -PassThru; exit $p.ExitCode"
    result = subprocess.run(['powershell', '-NoProfile', '-Command', script])
    if result.returncode not in (0, 3010):
        raise RuntimeError(f'prerequisite {os.path.basename(path)} exited with {result.returncode}')
