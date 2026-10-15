import asyncio
import hashlib
import os
import random
import shutil
import statistics
import time
from collections import deque

import httpx

import manifest as mf


def mirror_url(mirror, path=None):
    base = mirror['uri'] if path is None else mirror['uri'].rsplit('/', 1)[0] + '/' + path
    query = '&'.join(f"{p['name']}={p['value']}" for p in mirror.get('queryParams', []))
    return base + ('?' + query if query else '')


def fetch_manifest(element):
    errors = []
    for mirror in element['manifests']:
        host = mirror['uri'].split('/')[2]
        try:
            r = httpx.get(mirror_url(mirror), timeout=120)
        except httpx.HTTPError as e:
            errors.append(f'{type(e).__name__} {host}')
            continue
        if r.status_code == 200 and hashlib.sha1(r.content).hexdigest() == element['hash']:
            return r.content
        errors.append(f'{r.status_code} {host}')
    raise RuntimeError('manifest unavailable: ' + ', '.join(errors))


def fetch_delta(element, old_build_id, new_build_id):
    if not old_build_id or not new_build_id or old_build_id == new_build_id:
        return None
    for mirror in element['manifests']:
        url = mirror['uri'].rsplit('/', 1)[0] + f'/Deltas/{new_build_id}/{old_build_id}.delta'
        try:
            r = httpx.get(url, timeout=120)
        except httpx.HTTPError:
            continue
        if r.status_code == 200:
            return r.content
    return None


def merge_delta(new, delta):
    files = {f['filename']: f for f in delta['files']['list']}
    merged = dict(new)
    merged['files'] = dict(new['files'])
    merged['files']['list'] = [files[f['filename']] if f['filename'] in files and files[f['filename']]['sha1'] == f['sha1'] else f for f in new['files']['list']]
    chunks = {c['guid']: c for c in new['chunks']['list']}
    for c in delta['chunks']['list']:
        chunks.setdefault(c['guid'], c)
    merged['chunks'] = dict(new['chunks'])
    merged['chunks']['list'] = list(chunks.values())
    return merged


def select_files(manifest, tags=None):
    files = manifest['files']['list']
    if tags is None:
        return files
    wanted = set(tags) | {''}
    return [f for f in files if not f['installTags'] or wanted & set(f['installTags'])]


def file_ok(path, entry, deep=True):
    if not os.path.isfile(path) or os.path.getsize(path) != entry['size']:
        return False
    if not deep:
        return True
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest() == entry['sha1']


class RateLimit:
    def __init__(self, bytes_per_second):
        self.rate = bytes_per_second
        self.allowance = 0.0
        self.last = time.monotonic()
        self.lock = asyncio.Lock()

    async def take(self, n):
        if not self.rate:
            return
        async with self.lock:
            now = time.monotonic()
            self.allowance = min(self.rate, self.allowance + (now - self.last) * self.rate)
            self.last = now
            self.allowance -= n
            if self.allowance < 0:
                await asyncio.sleep(-self.allowance / self.rate)


class ChunkStore:
    def __init__(self, spill_dir, memory_limit):
        self.spill_dir = spill_dir
        self.memory_limit = memory_limit
        self.memory = {}
        self.memory_bytes = 0
        self.spilled = set()

    def put(self, guid, data):
        if self.memory_bytes + len(data) > self.memory_limit:
            os.makedirs(self.spill_dir, exist_ok=True)
            with open(os.path.join(self.spill_dir, guid), 'wb') as f:
                f.write(data)
            self.spilled.add(guid)
            return
        self.memory[guid] = data
        self.memory_bytes += len(data)

    def get(self, guid):
        if guid in self.memory:
            return self.memory[guid]
        with open(os.path.join(self.spill_dir, guid), 'rb') as f:
            return f.read()

    def drop(self, guid):
        if guid in self.memory:
            self.memory_bytes -= len(self.memory.pop(guid))
        elif guid in self.spilled:
            self.spilled.discard(guid)
            os.remove(os.path.join(self.spill_dir, guid))


class CdnSelector:
    def __init__(self, mirrors):
        self.mirrors = list(mirrors)
        self.failures = [0] * len(self.mirrors)

    def ordered(self):
        order = sorted(range(len(self.mirrors)), key=lambda i: (self.failures[i], i))
        return [(i, self.mirrors[i]) for i in order]

    def failed(self, index):
        self.failures[index] += 1


class StallTimer:
    def __init__(self, floor=20.0, ceiling=60.0, window=100):
        self.floor = floor
        self.ceiling = ceiling
        self.samples = deque(maxlen=window)

    def timeout(self):
        if len(self.samples) < 2:
            return self.floor
        value = statistics.fmean(self.samples) + 4 * statistics.pstdev(self.samples)
        return min(max(self.floor, value), self.ceiling)

    def record(self, seconds):
        self.samples.append(seconds)


class Engine:
    def __init__(self, workers=24, retries=4, memory_limit_mb=1024, speed_limit=0, progress=None):
        self.workers = workers
        self.retries = retries
        self.memory_limit = memory_limit_mb << 20
        self.limit = RateLimit(speed_limit)
        self.progress = progress or (lambda event: None)

    async def download_chunk(self, client, cdn, stall, manifest, chunk):
        path = mf.chunk_path(manifest, chunk)
        errors = []
        for attempt in range(self.retries):
            if attempt:
                await asyncio.sleep(((1000 << (attempt - 1)) + random.randrange(500)) / 1000)
            for index, mirror in cdn.ordered():
                host = mirror['uri'].split('/')[2]
                started = time.monotonic()
                try:
                    r = await asyncio.wait_for(client.get(mirror_url(mirror, path)), stall.timeout())
                    if r.status_code != 200:
                        raise ValueError(f'HTTP {r.status_code}')
                    header, data = mf.parse_chunk(r.content)
                    if hashlib.sha1(data).hexdigest() != chunk['sha1']:
                        raise ValueError('sha1 mismatch')
                except (httpx.HTTPError, ValueError, asyncio.TimeoutError, OSError) as e:
                    cdn.failed(index)
                    errors.append(f'{host}: {e or type(e).__name__}')
                    continue
                stall.record(time.monotonic() - started)
                await self.limit.take(len(r.content))
                self.progress({'type': 'chunk', 'bytes': len(r.content), 'host': host})
                return data
        raise RuntimeError(f'chunk {chunk["guid"]} failed after {self.retries} attempts: {errors[-3:]}')

    def plan(self, new, install_dir, old=None, tags=None, old_tags=None, protected=frozenset(), check='size'):
        files = select_files(new, tags)
        old_files = {f['filename']: f for f in select_files(old, old_tags)} if old else {}
        keep, todo = [], []
        for f in files:
            target = os.path.join(install_dir, f['filename'])
            prev = old_files.get(f['filename'])
            unchanged = prev is not None and prev['sha1'] == f['sha1']
            if unchanged and file_ok(target, f, deep=check == 'hash'):
                keep.append(f)
            elif prev is None and file_ok(target, f, deep=True):
                keep.append(f)
            else:
                todo.append(f)
        wanted = {f['filename'] for f in files}
        removed = [name for name in old_files if name not in wanted and name not in protected]
        sources = {}
        for f in old_files.values():
            position = 0
            for p in f['chunkParts']:
                sources.setdefault(p['guid'], []).append((f['filename'], position, p['offset'], p['size']))
                position += p['size']
        chunks = {c['guid']: c for c in new['chunks']['list']}
        download, reuse = {}, 0
        for f in todo:
            for p in f['chunkParts']:
                if self.local_source(sources, p, install_dir):
                    reuse += p['size']
                    continue
                download.setdefault(p['guid'], chunks[p['guid']])
        return {
            'files': files,
            'keep': keep,
            'todo': todo,
            'removed': removed,
            'sources': sources,
            'download': download,
            'downloadSize': sum(c['fileSize'] for c in download.values()),
            'reuseSize': reuse,
            'installSize': sum(f['size'] for f in files),
        }

    def local_source(self, sources, part, install_dir):
        for filename, position, offset, size in sources.get(part['guid'], ()):
            if offset <= part['offset'] and part['offset'] + part['size'] <= offset + size:
                path = os.path.join(install_dir, filename)
                if os.path.isfile(path):
                    return path, position + part['offset'] - offset
        return None

    async def apply(self, element, new, plan, install_dir):
        staging = os.path.join(install_dir, '.egstore', 'staging')
        store = ChunkStore(os.path.join(install_dir, '.egstore', 'chunkcache'), self.memory_limit)
        refs = {}
        order = []
        for f in plan['todo']:
            for p in f['chunkParts']:
                if p['guid'] in plan['download']:
                    if p['guid'] not in refs:
                        order.append(p['guid'])
                    refs[p['guid']] = refs.get(p['guid'], 0) + 1
        loop = asyncio.get_running_loop()
        ready = {guid: loop.create_future() for guid in order}
        sem = asyncio.Semaphore(self.workers)
        lead = asyncio.Semaphore(self.workers * 8)
        first_use = set()
        handles = {}
        bad = []
        cdn = CdnSelector(element['manifests'])
        stall = StallTimer()
        async with httpx.AsyncClient(timeout=httpx.Timeout(60, connect=15), limits=httpx.Limits(max_connections=self.workers * 2)) as client:
            async def fetch(guid):
                try:
                    async with sem:
                        data = await self.download_chunk(client, cdn, stall, new, plan['download'][guid])
                    store.put(guid, data)
                    ready[guid].set_result(True)
                except Exception as e:
                    ready[guid].set_exception(e)

            async def schedule():
                tasks = []
                for guid in order:
                    await lead.acquire()
                    tasks.append(asyncio.create_task(fetch(guid)))
                await asyncio.gather(*tasks)

            scheduler = asyncio.create_task(schedule())
            for f in plan['todo']:
                target = os.path.join(staging, f['filename'])
                os.makedirs(os.path.dirname(target), exist_ok=True)
                h = hashlib.sha1()
                with open(target, 'wb') as out:
                    for p in f['chunkParts']:
                        if p['guid'] in plan['download']:
                            await ready[p['guid']]
                            if p['guid'] not in first_use:
                                first_use.add(p['guid'])
                                lead.release()
                            piece = store.get(p['guid'])[p['offset']:p['offset'] + p['size']]
                            refs[p['guid']] -= 1
                            if refs[p['guid']] == 0:
                                store.drop(p['guid'])
                        else:
                            path, position = self.local_source(plan['sources'], p, install_dir)
                            if path not in handles:
                                handles[path] = open(path, 'rb')
                            src = handles[path]
                            src.seek(position)
                            piece = src.read(p['size'])
                        out.write(piece)
                        h.update(piece)
                if h.hexdigest() != f['sha1']:
                    bad.append(f['filename'])
                self.progress({'type': 'file', 'name': f['filename'], 'size': f['size']})
            await scheduler
        for handle in handles.values():
            handle.close()
        if bad:
            raise RuntimeError(f'{len(bad)} files failed hash check: {bad[:5]}')
        for f in plan['todo']:
            target = os.path.join(install_dir, f['filename'])
            os.makedirs(os.path.dirname(target), exist_ok=True)
            os.replace(os.path.join(staging, f['filename']), target)
            if f['flags'] & 4:
                os.chmod(target, 0o755)
        for name in plan['removed']:
            path = os.path.join(install_dir, name)
            if os.path.isfile(path):
                os.remove(path)
        shutil.rmtree(staging, ignore_errors=True)
        shutil.rmtree(store.spill_dir, ignore_errors=True)


def verify(install_dir, manifest, tags=None):
    bad = []
    for f in select_files(manifest, tags):
        path = os.path.join(install_dir, f['filename'])
        if not os.path.isfile(path):
            bad.append(('missing', f['filename']))
        elif not file_ok(path, f):
            bad.append(('corrupt', f['filename']))
    return bad
