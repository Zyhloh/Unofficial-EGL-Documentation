import argparse
import asyncio
import json
import os
import sys
import time

from auth import Auth
from client import Client, kind
from cloudsaves import CloudSaves

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config():
    with open(os.path.join(HERE, 'config.json'), encoding='utf-8') as f:
        return json.load(f)


def size(n):
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n < 1024 or unit == 'TB':
            return f'{n:.1f} {unit}' if unit != 'B' else f'{n} B'
        n /= 1024


class Progress:
    def __init__(self):
        self.bytes = 0
        self.files = 0
        self.start = time.time()
        self.last = 0

    def __call__(self, event):
        if event['type'] == 'chunk':
            self.bytes += event['bytes']
        else:
            self.files += 1
        now = time.time()
        if now - self.last > 0.5:
            self.last = now
            rate = self.bytes / max(now - self.start, 0.001)
            sys.stdout.write(f'\r  {size(self.bytes)} downloaded, {self.files} files, {size(rate)}/s   ')
            sys.stdout.flush()


def print_json(data):
    print(json.dumps(data, indent=2, default=str))


def cmd_library(client, args):
    for r in sorted(client.library(), key=lambda r: r['item'].get('title', '')):
        installed = client.state.get(r['appName'])
        mark = f"  [{installed['version']}]" if installed else ''
        print(f"{r['item'].get('title', '?')[:48]:48} {kind(r['item']):24} {r['appName']}{mark}")


def cmd_info(client, args):
    record = client.find(args.app)
    info = client.describe(record)
    meta = info['manifest']['meta']
    print_json({
        'title': info['title'],
        'kind': info['kind'],
        'appName': record['appName'],
        'namespace': record['namespace'],
        'catalogItemId': record['catalogItemId'],
        'buildVersion': info['element']['buildVersion'],
        'installSize': size(info['installSize']),
        'downloadSize': size(info['downloadSize']),
        'launchExe': meta.get('launchExe'),
        'launchCommand': meta.get('launchCommand'),
        'prereq': {'ids': meta.get('prereqIds'), 'path': meta.get('prereqPath'), 'args': meta.get('prereqArgs')},
        'installTags': info['tags'],
        'components': info['components'],
        'attributes': {k: v for k, v in info['attributes'].items() if 'Requirements' not in k},
    })


def cmd_addons(client, args):
    record = client.find(args.app)
    for a in client.addons(record):
        mark = ' installed' if a['installed'] else ''
        print(f"{a['title'][:44]:44} {a['appName']:34} {a['status']}{mark}")


async def cmd_install(client, args):
    tags = args.tags.split(',') if args.tags is not None else None
    components = args.components.split(',') if args.components is not None else None
    job = client.prepare(args.app, args.dir, tags, components)
    summary = job['summary']
    print(f"{summary['title']} {summary['from'] or '-'} -> {summary['to']}  ({summary['kind']})")
    print(f"  {summary['dir']}")
    print(f"  {summary['files']} files, {summary['unchanged']} unchanged, {summary['write']} to write, {summary['remove']} to remove")
    print(f"  download {size(summary['downloadSize'])} in {summary['chunks']} chunks, reuse {size(summary['reuseSize'])}, installed {size(summary['installSize'])}{', delta manifest' if summary['delta'] else ''}")
    if args.dry_run or (summary['write'] == 0 and summary['remove'] == 0):
        if summary['write'] == 0 and summary['remove'] == 0:
            print('  up to date')
        return
    client.engine.progress = Progress()
    await client.commit(job, run_prereqs=args.prereqs or client.config['runPrereqs'])
    print('\n  done')


def cmd_check(client, args):
    for u in client.check_updates():
        state = 'update available' if u['update'] else ('never updates' if u['neverUpdate'] else 'up to date')
        print(f"{u['title'][:40]:40} {u['installed']} -> {u['live']}  {state}")


def cmd_verify(client, args):
    bad = client.verify(args.app)
    for reason, name in bad:
        print(f'{reason:8} {name}')
    print(f'{len(bad)} bad files')


async def cmd_repair(client, args):
    client.engine.progress = Progress()
    print(f'\nrepaired {await client.repair(args.app)} files')


def cmd_uninstall(client, args):
    client.uninstall(args.app, args.run_uninstall_action)
    print('removed')


def cmd_launch(client, args):
    result = client.launch(args.app, args.args, args.dry_run)
    if not args.dry_run:
        print('launched')
        return
    if 'args' in result:
        result['args'] = ['-AUTH_PASSWORD=<exchange code>' if a.startswith('-AUTH_PASSWORD=') else a for a in result['args']]
    if 'uri' in result:
        result['uri'] = result['uri'].split('?')[0] + '?<query with exchange code>'
    print_json(result)


def cmd_saves(client, args):
    st = CloudSaves(client).status(client.find(args.app))
    if st is None:
        print('this title has no cloud saves')
        return
    print_json({k: v for k, v in st.items() if k not in ('cfg', 'remote', 'local')})


def cmd_sync_saves(client, args):
    print_json(CloudSaves(client).sync(client.find(args.app), args.prefer, args.force))


def cmd_import(client, args):
    for name in client.import_egl(args.path):
        print('imported', name)


def cmd_export(client, args):
    print_json(client.export_egl(args.app))
    print('restart the Epic Games Launcher to see it')


def cmd_art(client, args):
    print_json(client.art(client.find(args.app), client.config['locale']))


def main():
    parser = argparse.ArgumentParser(prog='DownloadClient')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('library')
    for name in ('info', 'addons', 'verify', 'repair', 'art'):
        sub.add_parser(name).add_argument('app')
    p = sub.add_parser('install')
    p.add_argument('app')
    p.add_argument('--dir')
    p.add_argument('--tags')
    p.add_argument('--components')
    p.add_argument('--prereqs', action='store_true')
    p.add_argument('--dry-run', action='store_true')
    sub.add_parser('check')
    sub.add_parser('saves').add_argument('app')
    p = sub.add_parser('sync-saves')
    p.add_argument('app')
    p.add_argument('--prefer', choices=('cloud', 'local'))
    p.add_argument('--force', choices=('push', 'pull'))
    p = sub.add_parser('launch')
    p.add_argument('app')
    p.add_argument('args', nargs='*')
    p.add_argument('--dry-run', action='store_true')
    sub.add_parser('import').add_argument('path', nargs='?')
    sub.add_parser('export').add_argument('app')
    p = sub.add_parser('uninstall')
    p.add_argument('app')
    p.add_argument('--run-uninstall-action', action='store_true')
    args = parser.parse_args()

    config = load_config()
    client = Client(config, Auth(config).token())
    handler = globals()['cmd_' + args.command.replace('-', '_')]
    result = handler(client, args)
    if asyncio.iscoroutine(result):
        asyncio.run(result)


if __name__ == '__main__':
    main()
