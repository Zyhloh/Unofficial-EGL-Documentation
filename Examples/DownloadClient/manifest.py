import hashlib
import io
import json
import struct
import zlib

MANIFEST_MAGIC = 0x44BEC00C
CHUNK_MAGIC = 0xB1FE3AA2


class Reader:
    def __init__(self, data):
        self.b = io.BytesIO(data)

    def u8(self):
        return struct.unpack('<B', self.b.read(1))[0]

    def u32(self):
        return struct.unpack('<I', self.b.read(4))[0]

    def i32(self):
        return struct.unpack('<i', self.b.read(4))[0]

    def u64(self):
        return struct.unpack('<Q', self.b.read(8))[0]

    def i64(self):
        return struct.unpack('<q', self.b.read(8))[0]

    def raw(self, n):
        return self.b.read(n)

    def fstring(self):
        n = self.i32()
        if n == 0:
            return ''
        if n < 0:
            return self.b.read(-n * 2).decode('utf-16-le').rstrip('\x00')
        return self.b.read(n).decode('utf-8', 'replace').rstrip('\x00')

    def guid(self):
        return '%08X%08X%08X%08X' % struct.unpack('<4I', self.b.read(16))

    def tell(self):
        return self.b.tell()

    def seek(self, pos):
        self.b.seek(pos)


def chunk_dir(feature_level):
    if feature_level < 3:
        return 'Chunks'
    if feature_level < 6:
        return 'ChunksV2'
    if feature_level < 15:
        return 'ChunksV3'
    return 'ChunksV4'


def parse_header(data):
    r = Reader(data)
    magic = r.u32()
    if magic != MANIFEST_MAGIC:
        raise ValueError('not a binary manifest')
    header = {
        'magic': magic,
        'headerSize': r.u32(),
        'dataSizeUncompressed': r.u32(),
        'dataSizeCompressed': r.u32(),
        'sha1': r.raw(20).hex(),
        'storedAs': r.u8(),
        'version': r.u32(),
    }
    return header


def parse(data):
    if data[:1] == b'{':
        return parse_json(data)
    header = parse_header(data)
    body = data[header['headerSize']:header['headerSize'] + header['dataSizeCompressed']]
    if header['storedAs'] & 2:
        raise ValueError('encrypted manifest')
    if header['storedAs'] & 1:
        body = zlib.decompress(body)
    if hashlib.sha1(body).hexdigest() != header['sha1']:
        raise ValueError('manifest body sha1 mismatch')
    r = Reader(body)
    meta = parse_meta(r)
    chunks = parse_chunks(r)
    files = parse_files(r)
    custom = parse_custom(r)
    return {'header': header, 'meta': meta, 'chunks': chunks, 'files': files, 'customFields': custom}


def parse_meta(r):
    start = r.tell()
    size = r.u32()
    m = {'dataSize': size, 'dataVersion': r.u8(), 'featureLevel': r.u32(), 'isFileData': bool(r.u8()), 'appId': r.u32()}
    m['appName'] = r.fstring()
    m['buildVersion'] = r.fstring()
    m['launchExe'] = r.fstring()
    m['launchCommand'] = r.fstring()
    m['prereqIds'] = [r.fstring() for _ in range(r.u32())]
    m['prereqName'] = r.fstring()
    m['prereqPath'] = r.fstring()
    m['prereqArgs'] = r.fstring()
    if m['dataVersion'] >= 1:
        m['buildId'] = r.fstring()
    if m['dataVersion'] >= 2:
        m['uninstallActionPath'] = r.fstring()
        m['uninstallActionArgs'] = r.fstring()
    r.seek(start + size)
    return m


def parse_chunks(r):
    start = r.tell()
    size = r.u32()
    version = r.u8()
    count = r.u32()
    guids = [r.guid() for _ in range(count)]
    hashes = [r.u64() for _ in range(count)]
    shas = [r.raw(20).hex() for _ in range(count)]
    groups = [r.u8() for _ in range(count)]
    window = [r.u32() for _ in range(count)]
    filesize = [r.i64() for _ in range(count)]
    r.seek(start + size)
    return {
        'dataVersion': version,
        'list': [
            {'guid': guids[i], 'hash': hashes[i], 'sha1': shas[i], 'group': groups[i], 'windowSize': window[i], 'fileSize': filesize[i]}
            for i in range(count)
        ],
    }


def parse_files(r):
    start = r.tell()
    size = r.u32()
    version = r.u8()
    count = r.u32()
    names = [r.fstring() for _ in range(count)]
    symlinks = [r.fstring() for _ in range(count)]
    hashes = [r.raw(20).hex() for _ in range(count)]
    flags = [r.u8() for _ in range(count)]
    tags = [[r.fstring() for _ in range(r.u32())] for _ in range(count)]
    parts = []
    for _ in range(count):
        file_parts = []
        for _ in range(r.u32()):
            pstart = r.tell()
            psize = r.u32()
            file_parts.append({'guid': r.guid(), 'offset': r.u32(), 'size': r.u32()})
            r.seek(pstart + psize)
        parts.append(file_parts)
    md5 = [None] * count
    mime = [''] * count
    sha256 = [None] * count
    if version >= 1:
        for i in range(count):
            if r.u32():
                md5[i] = r.raw(16).hex()
        mime = [r.fstring() for _ in range(count)]
    if version >= 2:
        sha256 = [r.raw(32).hex() for _ in range(count)]
    r.seek(start + size)
    return {
        'dataVersion': version,
        'list': [
            {
                'filename': names[i],
                'symlinkTarget': symlinks[i],
                'sha1': hashes[i],
                'flags': flags[i],
                'installTags': tags[i],
                'chunkParts': parts[i],
                'md5': md5[i],
                'mimeType': mime[i],
                'sha256': sha256[i],
                'size': sum(p['size'] for p in parts[i]),
            }
            for i in range(count)
        ],
    }


def parse_custom(r):
    start = r.tell()
    try:
        size = r.u32()
    except struct.error:
        return {}
    version = r.u8()
    count = r.u32()
    keys = [r.fstring() for _ in range(count)]
    values = [r.fstring() for _ in range(count)]
    r.seek(start + size)
    return dict(zip(keys, values))


def blob_int(s, nbytes):
    raw = bytes(int(s[i:i + 3]) for i in range(0, len(s), 3))
    return int.from_bytes(raw[:nbytes], 'little')


def parse_json(data):
    j = json.loads(data)
    feature = blob_int(j['ManifestFileVersion'], 4)
    chunks = []
    for guid, h in j['ChunkHashList'].items():
        chunks.append({
            'guid': guid.upper(),
            'hash': blob_int(h, 8),
            'sha1': j.get('ChunkShaList', {}).get(guid, '').lower(),
            'group': blob_int(j['DataGroupList'][guid], 1),
            'windowSize': 1048576,
            'fileSize': blob_int(j['ChunkFilesizeList'][guid], 8),
        })
    files = []
    for f in j['FileManifestList']:
        parts = [{'guid': p['Guid'].upper(), 'offset': blob_int(p['Offset'], 4), 'size': blob_int(p['Size'], 4)} for p in f['FileChunkParts']]
        files.append({
            'filename': f['Filename'],
            'symlinkTarget': '',
            'sha1': bytes(int(f['FileHash'][i:i + 3]) for i in range(0, len(f['FileHash']), 3)).hex(),
            'flags': 0,
            'installTags': f.get('InstallTags', []),
            'chunkParts': parts,
            'md5': None,
            'mimeType': '',
            'sha256': None,
            'size': sum(p['size'] for p in parts),
        })
    return {
        'header': {'json': True},
        'meta': {
            'featureLevel': feature,
            'appName': j.get('AppNameString'),
            'buildVersion': j.get('BuildVersionString'),
            'launchExe': j.get('LaunchExeString'),
            'launchCommand': j.get('LaunchCommand'),
            'prereqIds': j.get('PrereqIds', []),
            'prereqName': j.get('PrereqName'),
            'prereqPath': j.get('PrereqPath'),
            'prereqArgs': j.get('PrereqArgs'),
        },
        'chunks': {'list': chunks},
        'files': {'list': files},
        'customFields': j.get('CustomFields', {}),
    }


def chunk_path(manifest, chunk):
    return '%s/%02d/%016X_%s.chunk' % (chunk_dir(manifest['meta']['featureLevel']), chunk['group'], chunk['hash'], chunk['guid'])


def parse_chunk(data):
    r = Reader(data)
    magic = r.u32()
    if magic != CHUNK_MAGIC:
        raise ValueError('not a chunk')
    h = {'magic': magic, 'version': r.u32(), 'headerSize': r.u32(), 'dataSizeCompressed': r.u32(), 'guid': r.guid(), 'rollingHash': r.u64(), 'storedAs': r.u8()}
    if h['version'] >= 2:
        h['sha1'] = r.raw(20).hex()
        h['hashType'] = r.u8()
    if h['version'] >= 3:
        h['dataSizeUncompressed'] = r.u32()
    payload = data[h['headerSize']:h['headerSize'] + h['dataSizeCompressed']]
    if h['storedAs'] & 2:
        raise ValueError('encrypted chunk')
    if h['storedAs'] & 1:
        payload = zlib.decompress(payload)
    return h, payload


ROLLING_POLY = 0xC96C5795D7870F42
WINDOW = 1048576


def _rolling_table():
    table = []
    for i in range(256):
        for _ in range(8):
            i = (i >> 1) ^ ROLLING_POLY if i & 1 else i >> 1
        table.append(i)
    return table


ROLLING_TABLE = _rolling_table()


def rolling_hash(data):
    h = 0
    table = ROLLING_TABLE
    for b in data:
        h = (((h << 1) | (h >> 63)) & 0xFFFFFFFFFFFFFFFF) ^ table[b]
    return h


def _fstring(s):
    if not s:
        return struct.pack('<i', 0)
    raw = s.encode('utf-8') + b'\x00'
    return struct.pack('<i', len(raw)) + raw


def _section(payload):
    return struct.pack('<IB', len(payload) + 5, 0) + payload


def _guid_bytes(guid):
    return struct.pack('<4I', *[int(guid[i:i + 8], 16) for i in range(0, 32, 8)])


def build_chunk(guid, data):
    padded = data + bytes(WINDOW - len(data))
    stored = zlib.compress(padded)
    header = struct.pack('<IIII', CHUNK_MAGIC, 3, 66, len(stored)) + _guid_bytes(guid)
    header += struct.pack('<QB', rolling_hash(padded), 1) + hashlib.sha1(padded).digest() + struct.pack('<BI', 3, WINDOW)
    return header + stored, padded


def build(app_name, build_version, files, custom_fields=None, new_guid=None):
    import uuid
    new_guid = new_guid or (lambda: uuid.uuid4().hex.upper())
    chunks = []
    current = bytearray()
    guid = new_guid()
    entries = []
    for name, data in files:
        parts = []
        pos = 0
        while pos < len(data) or (not data and not parts):
            room = WINDOW - len(current)
            take = min(room, len(data) - pos)
            if take:
                parts.append((guid, len(current), take))
                current += data[pos:pos + take]
                pos += take
            if len(current) == WINDOW:
                chunks.append((guid, bytes(current)))
                current = bytearray()
                guid = new_guid()
            if not data:
                break
        entries.append((name, hashlib.sha1(data).digest(), parts))
    if current:
        chunks.append((guid, bytes(current)))
    chunk_files = {}
    chunk_rows = []
    for g, data in chunks:
        blob, padded = build_chunk(g, data)
        chunk_files[g] = blob
        group = (zlib.crc32(_guid_bytes(g)) & 0xFFFFFFFF) % 100
        chunk_rows.append((g, rolling_hash(padded), hashlib.sha1(padded).digest(), group, len(blob)))
    meta = struct.pack('<IBI', 17, 0, 0) + _fstring(app_name) + _fstring(build_version) + _fstring('') + _fstring('')
    meta += struct.pack('<I', 0) + _fstring('') + _fstring('') + _fstring('')
    chunk_list = struct.pack('<I', len(chunk_rows))
    chunk_list += b''.join(_guid_bytes(r[0]) for r in chunk_rows)
    chunk_list += b''.join(struct.pack('<Q', r[1]) for r in chunk_rows)
    chunk_list += b''.join(r[2] for r in chunk_rows)
    chunk_list += b''.join(struct.pack('<B', r[3]) for r in chunk_rows)
    chunk_list += b''.join(struct.pack('<I', WINDOW) for _ in chunk_rows)
    chunk_list += b''.join(struct.pack('<q', r[4]) for r in chunk_rows)
    file_list = struct.pack('<I', len(entries))
    file_list += b''.join(_fstring(e[0]) for e in entries)
    file_list += b''.join(_fstring('') for _ in entries)
    file_list += b''.join(e[1] for e in entries)
    file_list += bytes(len(entries))
    file_list += b''.join(struct.pack('<I', 0) for _ in entries)
    for e in entries:
        file_list += struct.pack('<I', len(e[2]))
        for g, offset, size in e[2]:
            file_list += struct.pack('<I', 28) + _guid_bytes(g) + struct.pack('<II', offset, size)
    custom = custom_fields or {}
    custom_list = struct.pack('<I', len(custom)) + b''.join(_fstring(k) for k in custom) + b''.join(_fstring(v) for v in custom.values())
    body = _section(meta) + _section(chunk_list) + _section(file_list) + _section(custom_list)
    stored = zlib.compress(body)
    header = struct.pack('<IIII', MANIFEST_MAGIC, 41, len(body), len(stored)) + hashlib.sha1(body).digest() + struct.pack('<BI', 1, 17)
    return header + stored, chunk_files
