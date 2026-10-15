import datetime
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys

import httpx

import manifest as mf


def known_folder(guid):
    if sys.platform != 'win32':
        return None
    import ctypes
    from ctypes import wintypes

    class GUID(ctypes.Structure):
        _fields_ = [('Data1', wintypes.DWORD), ('Data2', wintypes.WORD), ('Data3', wintypes.WORD), ('Data4', ctypes.c_ubyte * 8)]

    parts = guid.split('-')
    g = GUID(int(parts[0], 16), int(parts[1], 16), int(parts[2], 16), (ctypes.c_ubyte * 8)(*bytes.fromhex(parts[3] + parts[4])))
    path = ctypes.c_wchar_p()
    if ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(g), 0, None, ctypes.byref(path)) != 0:
        return None
    value = path.value
    ctypes.windll.ole32.CoTaskMemFree(path)
    return value


def variables(account_id, install_dir):
    home = os.path.expanduser('~')
    return {
        'epicid': account_id,
        'installdir': install_dir or '',
        'userdir': known_folder('FDD39AD0-238F-46AF-ADB4-6C85480369C7') or os.path.join(home, 'Documents'),
        'appdata': os.environ.get('LOCALAPPDATA') or os.path.join(home, 'AppData', 'Local'),
        'userprofile': home,
        'usersavedgames': known_folder('4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4') or os.path.join(home, 'Saved Games'),
        'userlibrary': '',
    }


def expand(template, values):
    def repl(m):
        key = m.group(1).lower()
        if key not in values:
            raise ValueError(f'unknown cloud save variable {m.group(0)}')
        if not values[key]:
            raise ValueError(f'empty cloud save variable {m.group(0)}')
        return values[key]
    return os.path.normpath(re.sub(r'\{([^}]+)\}', repl, template))


def patterns(value):
    return [p.strip().lower() for p in (value or '').split(',') if p.strip()]


def matches(path, pattern):
    if '*' in pattern or '?' in pattern:
        return fnmatch.fnmatchcase(path, pattern)
    if pattern.endswith('/'):
        return pattern in path or path.startswith(pattern)
    return path.endswith(pattern)


def selected(path, include, exclude):
    p = path.lower()
    if include and not any(matches(p, i) for i in include):
        return False
    return not any(matches(p, e) for e in exclude)


class CloudSaves:
    def __init__(self, client):
        self.client = client
        self.epic = client.epic
        self.root = os.path.join(os.path.dirname(os.path.expanduser(client.config['stateFile'])), 'cloudsaves', self.epic.token['account_id'])

    def config(self, record):
        attrs = {k: v.get('value') for k, v in (record['item'].get('customAttributes') or {}).items()}
        template = attrs.get('CloudSaveFolder')
        if not template:
            return None
        entry = self.client.state.get(record['appName'])
        folder = expand(template + (attrs.get('CloudSaveCustomPathSuffix') or ''), variables(self.epic.token['account_id'], entry['dir'] if entry else None))
        return {
            'template': template,
            'folder': folder,
            'include': patterns(attrs.get('CloudIncludeList')),
            'exclude': patterns(attrs.get('CloudExcludeList')),
            'custom': {k: v for k, v in (('CloudSaveFolder', template), ('CloudSaveFolder_Mac', attrs.get('CloudSaveFolder_MAC')), ('CloudSaveFolder_Linux', attrs.get('CloudSaveFolder_Linux'))) if v},
        }

    def state_path(self, app):
        return os.path.join(self.root, app, 'sync.json')

    def read_state(self, app):
        try:
            with open(self.state_path(app), encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def write_state(self, app, baseline, raw):
        folder = os.path.join(self.root, app)
        os.makedirs(os.path.join(folder, 'manifests'), exist_ok=True)
        with open(os.path.join(folder, 'manifests', baseline), 'wb') as f:
            f.write(raw)
        with open(self.state_path(app), 'w', encoding='utf-8') as f:
            json.dump({'baseline': baseline, 'lastSyncedAt': datetime.datetime.now(datetime.timezone.utc).isoformat()}, f, indent=2)

    def baseline_manifest(self, app, state):
        if not state.get('baseline'):
            return None
        path = os.path.join(self.root, app, 'manifests', state['baseline'])
        if not os.path.exists(path):
            return None
        with open(path, 'rb') as f:
            return mf.parse(f.read())

    def remote(self, app):
        files = self.epic.savesync_list(app).get('files', {})
        prefix = f'savesync/{self.epic.token["account_id"]}/{app}/'
        rel = {k[len(prefix):]: v for k, v in files.items() if k.startswith(prefix)}
        manifests = sorted(k.split('/', 1)[1] for k in rel if k.startswith('manifests/'))
        return rel, manifests

    def local(self, cfg):
        out = {}
        if not os.path.isdir(cfg['folder']):
            return out
        for root, _, names in os.walk(cfg['folder']):
            for name in names:
                path = os.path.join(root, name)
                rel = os.path.relpath(path, cfg['folder']).replace(os.sep, '/')
                if selected(rel, cfg['include'], cfg['exclude']):
                    with open(path, 'rb') as f:
                        out[rel] = f.read()
        return out

    def status(self, record):
        cfg = self.config(record)
        if not cfg:
            return None
        app = record['appName']
        state = self.read_state(app)
        rel, manifests = self.remote(app)
        base = self.baseline_manifest(app, state)
        local = self.local(cfg)
        local_hashes = {k: hashlib.sha1(v).hexdigest() for k, v in local.items()}
        base_hashes = {f['filename']: f['sha1'] for f in base['files']['list']} if base else None
        latest = manifests[-1] if manifests else None
        if base is None and latest and local:
            raw = httpx.get(rel['manifests/' + latest]['readLink'], timeout=60).content
            cloud_hashes = {f['filename']: f['sha1'] for f in mf.parse(raw)['files']['list']}
            if cloud_hashes == local_hashes:
                self.write_state(app, latest, raw)
                state = self.read_state(app)
                base_hashes = cloud_hashes
        return {
            'folder': cfg['folder'],
            'localFiles': len(local),
            'cloudManifests': manifests,
            'baseline': state.get('baseline'),
            'localChanged': bool(local) and local_hashes != base_hashes,
            'cloudChanged': latest is not None and latest != state.get('baseline'),
            'cfg': cfg,
            'remote': rel,
            'local': local,
        }

    def pull(self, record, st=None):
        st = st or self.status(record)
        app = record['appName']
        name = st['cloudManifests'][-1]
        raw = httpx.get(st['remote']['manifests/' + name]['readLink'], timeout=60).content
        m = mf.parse(raw)
        data = {}
        for c in m['chunks']['list']:
            blob = httpx.get(st['remote'][mf.chunk_path(m, c)]['readLink'], timeout=60).content
            _, payload = mf.parse_chunk(blob)
            if hashlib.sha1(payload).hexdigest() != c['sha1']:
                raise RuntimeError(f'save chunk {c["guid"]} failed its hash check')
            data[c['guid']] = payload
        if st['local']:
            backup = os.path.join(self.root, app, 'backups', datetime.datetime.now(datetime.timezone.utc).strftime('%Y.%m.%d-%H.%M.%S'))
            shutil.copytree(st['folder'], backup)
        for f in m['files']['list']:
            content = b''.join(data[p['guid']][p['offset']:p['offset'] + p['size']] for p in f['chunkParts'])
            if hashlib.sha1(content).hexdigest() != f['sha1']:
                raise RuntimeError(f'save file {f["filename"]} failed its hash check')
            target = os.path.join(st['folder'], f['filename'])
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, 'wb') as out:
                out.write(content)
        self.write_state(app, name, raw)
        return {'pulled': name, 'files': len(m['files']['list'])}

    def push(self, record, st=None, keep=3):
        st = st or self.status(record)
        app = record['appName']
        if not st['local']:
            return {'pushed': None, 'reason': 'no local saves'}
        name = datetime.datetime.now(datetime.timezone.utc).strftime('%Y.%m.%d-%H.%M.%S') + '.manifest'
        if st['cloudManifests'] and name <= st['cloudManifests'][-1]:
            raise RuntimeError('cloud has a newer save than this clock allows')
        raw, chunks = mf.build(app + self.epic.token['account_id'], name[:-len('.manifest')], sorted(st['local'].items()), st['cfg']['custom'])
        m = mf.parse(raw)
        paths = {c['guid']: mf.chunk_path(m, c) for c in m['chunks']['list']}
        links = self.epic.savesync_links(app, list(paths.values()) + ['manifests/' + name])['files']
        prefix = f'savesync/{self.epic.token["account_id"]}/{app}/'
        def put(rel, blob):
            link = (links.get(rel) or links[prefix + rel])['writeLink']
            r = httpx.put(link, content=blob, timeout=120)
            if r.status_code not in (200, 204):
                raise RuntimeError(f'upload of {rel} failed: {r.status_code} {r.text[:200]}')
        for guid, blob in chunks.items():
            put(paths[guid], blob)
        put('manifests/' + name, raw)
        self.write_state(app, name, raw)
        for old in sorted(st['cloudManifests'] + [name])[:-keep]:
            self.epic.savesync_delete(app, 'manifests/' + old)
        return {'pushed': name, 'files': len(st['local']), 'chunks': len(chunks), 'deletedChunks': self.clean_chunks(app)}

    def clean_chunks(self, app, min_age_seconds=3600):
        rel, manifests = self.remote(app)
        used = set()
        for name in manifests:
            m = mf.parse(httpx.get(rel['manifests/' + name]['readLink'], timeout=60).content)
            used |= {mf.chunk_path(m, c) for c in m['chunks']['list']}
        now = datetime.datetime.now(datetime.timezone.utc)
        deleted = 0
        for path, info in rel.items():
            if path.startswith('manifests/') or path in used or not info.get('lastModified'):
                continue
            modified = datetime.datetime.fromisoformat(info['lastModified'].replace('Z', '+00:00'))
            if (now - modified).total_seconds() > min_age_seconds:
                self.epic.savesync_delete(app, path)
                deleted += 1
        return deleted

    def sync(self, record, prefer=None, force=None):
        st = self.status(record)
        if st is None:
            return {'result': 'title has no cloud saves'}
        if force == 'push':
            return self.push(record, st)
        if force == 'pull':
            return self.pull(record, st)
        if st['cloudChanged'] and st['localChanged'] and not prefer:
            return {'result': 'conflict', 'folder': st['folder'], 'cloud': st['cloudManifests'][-1], 'localFiles': st['localFiles'], 'hint': 'run again with --prefer cloud or --prefer local'}
        if st['cloudChanged'] and (prefer == 'cloud' or not st['localChanged']):
            return self.pull(record, st)
        if st['localChanged']:
            return self.push(record, st)
        return {'result': 'in sync', 'baseline': st['baseline']}
