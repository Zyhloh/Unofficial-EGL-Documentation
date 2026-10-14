import asyncio
import json
import uuid

import websockets

URL = 'wss://connect.ol.epicgames.com/?auth-token={token}&accept-language=en'
HEARTBEAT_MS = 45000


def frame(command, headers, body=''):
    lines = [command] + [f'{k}:{v}' for k, v in headers.items()]
    return '\n'.join(lines) + '\n\n' + body + '\x00'


def parse(raw):
    if isinstance(raw, bytes):
        raw = raw.decode('utf-8', 'replace')
    raw = raw.rstrip('\x00')
    if not raw.strip():
        return None, {}, ''
    head, _, body = raw.partition('\n\n')
    lines = head.split('\n')
    headers = dict(line.split(':', 1) for line in lines[1:] if ':' in line)
    return lines[0], headers, body


class Connect:
    def __init__(self, token, account_id):
        self.token = token
        self.account_id = account_id
        self.connection_id = None
        self.events = asyncio.Queue()
        self.ws = None
        self.tasks = []

    async def start(self):
        self.ws = await websockets.connect(URL.format(token=self.token), max_size=None)
        await self.ws.send(frame('CONNECT', {'accept-version': '1.2,1.1,1.0', 'heart-beat': f'{HEARTBEAT_MS},0'}))
        command, headers, _ = parse(await self.ws.recv())
        if command != 'CONNECTED':
            raise RuntimeError(f'connect failed: {command} {headers}')
        self.connection_id = headers['session']
        await self.ws.send(frame('SUBSCRIBE', {'id': 'sub-0', 'destination': f'{uuid.uuid4()}/account/{self.account_id}'}))
        self.tasks = [asyncio.create_task(self.reader()), asyncio.create_task(self.heartbeat())]
        return self.connection_id

    async def reader(self):
        async for raw in self.ws:
            command, _, body = parse(raw)
            if command != 'MESSAGE':
                continue
            try:
                await self.events.put(json.loads(body))
            except json.JSONDecodeError:
                continue

    async def heartbeat(self):
        while True:
            await asyncio.sleep(HEARTBEAT_MS / 1000 - 5)
            await self.ws.send('\n')

    async def wait_for(self, predicate, timeout):
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        while True:
            event = await asyncio.wait_for(self.events.get(), max(0.1, deadline - loop.time()))
            if predicate(event):
                return event

    async def close(self):
        for task in self.tasks:
            task.cancel()
        if self.ws:
            await self.ws.close()
