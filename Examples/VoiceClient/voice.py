import asyncio
import json
import os
import secrets
import struct
import time

import websockets
from aiortc import RTCConfiguration, RTCPeerConnection, RTCSessionDescription, rtcdtlstransport
from aiortc.codecs import opus
from aiortc.contrib.media import MediaPlayer, MediaRecorder
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

SDK_VERSION = '1.19.4230.0-57929184@LauncherV2'
KEEPALIVE_SECONDS = 5
JOIN_OPTIONS = [
    'subscribe', 'dtx', 'rtcp_rsize', 'new_audio_only_reasons', 'v2', 'unified_plan',
    'speaking', 'speaking_self_only', 'ras_csrc', 'reserved_audio_streams', 'signed_audio',
]
SDK_CIPHERS = (
    b'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:'
    b'ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:'
    b'ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:AES128-GCM-SHA256:AES256-SHA:AES128-SHA'
)
SIGNED_TRAILER = 4 + 64 + 4
UNSIGNED_TRAILER = 4


class AudioSigner:
    version = struct.pack('>I', 1)

    def __init__(self, private_key, room_name):
        self.private_key = private_key
        self.context = room_name.encode()
        self.counter = 0

    def sign(self, payload):
        counter = struct.pack('>I', self.counter)
        self.counter += 1
        return payload + counter + self.private_key.sign(payload + counter + self.context) + self.version


def strip_signature(payload):
    if len(payload) >= SIGNED_TRAILER and payload[-4:] == b'\x00\x00\x00\x01':
        return payload[:-SIGNED_TRAILER]
    if len(payload) >= UNSIGNED_TRAILER and payload[-4:] == b'\x00\x00\x00\x00':
        return payload[:-UNSIGNED_TRAILER]
    return payload


signer = None
_create_ssl_context = rtcdtlstransport.RTCCertificate._create_ssl_context
_encode = opus.OpusEncoder.encode
_decode = opus.OpusDecoder.decode


def _ssl_context(self, srtp_profiles):
    ctx = _create_ssl_context(self, srtp_profiles)
    ctx.set_cipher_list(SDK_CIPHERS)
    return ctx


def _signed_encode(self, frame, force_keyframe=False):
    payloads, timestamp = _encode(self, frame, force_keyframe)
    if signer is not None:
        payloads = [signer.sign(p) for p in payloads]
    return payloads, timestamp


def _stripped_decode(self, encoded_frame):
    encoded_frame.data = strip_signature(encoded_frame.data)
    return _decode(self, encoded_frame)


rtcdtlstransport.RTCCertificate._create_ssl_context = _ssl_context
opus.OpusEncoder.encode = _signed_encode
opus.OpusDecoder.decode = _stripped_decode


def new_signing_key():
    key = Ed25519PrivateKey.generate()
    raw = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return key, raw


def join_message(ticket, account_id, signed_public_key):
    return {
        'type': 'join',
        'ticket': ticket,
        'user_token': account_id,
        'options': JOIN_OPTIONS,
        'version': SDK_VERSION,
        'device': {'os': 'Windows', 'model': '', 'manufacturer': '', 'online_platform_type': '0'},
        'status': {'is_muted': 0, 'audio_muted_reason': 0, 'is_audio_only': 1, 'reason_enum': 6, 'is_screencast': 0},
        'connection_id': secrets.token_hex(16).upper(),
        'video': {'width': 0, 'height': 0, 'codecs': []},
        'voice_moderation': {'signed_public_key': signed_public_key},
    }


def media_section(join_res, mid, direction, ssrc=None):
    lines = [
        'm=audio 9 UDP/TLS/RTP/SAVPF 100',
        'c=IN IP4 0.0.0.0',
        'a=rtcp:9 IN IP4 0.0.0.0',
        f'a=ice-ufrag:{join_res["ice"]["ufrag"]}',
        f'a=ice-pwd:{join_res["ice"]["pwd"]}',
        f'a=fingerprint:{join_res["fingerprint"]["fingerprint"]}',
        'a=setup:actpass',
        f'a=mid:{mid}',
        'a=extmap:1 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time',
        'a=extmap:5 urn:ietf:params:rtp-hdrext:ssrc-audio-level',
        'a=rtcp-mux',
        'a=rtcp-rsize',
        'a=rtpmap:100 opus/48000/2',
        'a=fmtp:100 minptime=10;useinbandfec=1;usedtx=1',
        f'a=ptime:{join_res.get("ptime") or 60}',
        f'a={direction}',
    ]
    if ssrc is not None:
        lines += [f'a=msid:remote audio-{ssrc}', f'a=ssrc:{ssrc} cname:remote']
    lines += [f'a=candidate:1 1 udp 2130706431 {join_res["ipv4"]} {join_res["udp_port"]} typ host', 'a=end-of-candidates']
    return lines


def server_offer(join_res):
    streams = [s['ssrc'] for s in join_res.get('reserved_audio_streams', [])]
    mids = [str(i) for i in range(len(streams) + 1)]
    lines = ['v=0', 'o=- 0 2 IN IP4 127.0.0.1', 's=-', 't=0 0', 'a=ice-lite', 'a=msid-semantic:WMS *', 'a=group:BUNDLE ' + ' '.join(mids)]
    lines += media_section(join_res, '0', 'recvonly')
    for mid, ssrc in zip(mids[1:], streams):
        lines += media_section(join_res, mid, 'sendonly', ssrc)
    return '\r\n'.join(lines) + '\r\n'


def sdp_fingerprint(sdp):
    for line in sdp.splitlines():
        if line.startswith('a=fingerprint:sha-256'):
            return line[len('a=fingerprint:'):].strip()
    raise RuntimeError('no sha-256 fingerprint in local answer')


class VoiceRoom:
    def __init__(self, credentials, account_id, send_audio, record_dir):
        self.credentials = credentials
        self.account_id = account_id
        self.send_audio = send_audio
        self.record_dir = record_dir
        self.ws = None
        self.pc = None
        self.recorders = []
        self.tasks = []
        self.join_res = asyncio.get_running_loop().create_future()

    async def send(self, message):
        await self.ws.send(json.dumps(message, separators=(',', ':')))

    async def connect(self, signing_key, signed_public_key):
        global signer
        signer = AudioSigner(signing_key, self.credentials['room_name'])
        self.ws = await websockets.connect(self.credentials['client_base_url'], max_size=None, ping_interval=None)
        self.tasks = [asyncio.create_task(self.reader()), asyncio.create_task(self.keepalive())]
        await self.send(join_message(self.credentials['participant_token'], self.account_id, signed_public_key))
        join_res = await asyncio.wait_for(self.join_res, 15)
        if join_res.get('status') != 0:
            raise RuntimeError(f'join rejected: {join_res}')
        await self.start_media(join_res)
        return join_res

    async def reader(self):
        async for raw in self.ws:
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                continue
            kind = message.get('type')
            if kind == 'join_res' and not self.join_res.done():
                self.join_res.set_result(message)
                for user in message.get('users', []):
                    await self.subscribe(user['user_token'])
            elif kind == 'user_joined':
                print('joined:', message['user_token'])
                await self.subscribe(message['user_token'])
            elif kind == 'user_left':
                print('left:', message['user_token'])
            elif kind == 'speaking':
                print('speaking:', message['user_token'], bool(message['is_speaking']))
            elif kind == 'mute_audio':
                print('muted:', message['user_token'], message['is_muted'])

    async def keepalive(self):
        while True:
            await asyncio.sleep(KEEPALIVE_SECONDS)
            await self.ws.send(' ')

    async def start_media(self, join_res):
        self.pc = RTCPeerConnection(RTCConfiguration(iceServers=[]))

        @self.pc.on('track')
        def on_track(track):
            os.makedirs(self.record_dir, exist_ok=True)
            path = os.path.join(self.record_dir, f'{int(time.time())}-{len(self.recorders)}.wav')
            recorder = MediaRecorder(path)
            recorder.addTrack(track)
            self.recorders.append(recorder)
            asyncio.ensure_future(recorder.start())

        @self.pc.on('connectionstatechange')
        async def on_state():
            print('media:', self.pc.connectionState)

        await self.pc.setRemoteDescription(RTCSessionDescription(sdp=server_offer(join_res), type='offer'))
        self.pc.addTrack(MediaPlayer(self.send_audio, loop=True).audio)
        self.pc.getTransceivers()[0].sender._ssrc = join_res['ssrc']['audio']
        answer = await self.pc.createAnswer()
        await self.send({'type': 'join_update', 'fingerprint': {'fingerprint': sdp_fingerprint(answer.sdp)}})
        await self.pc.setLocalDescription(answer)

    async def deafen(self, deafened, participants):
        await self.send({'type': 'mute_audio', 'is_muted': int(deafened), 'user_token': self.account_id, 'reason_enum': 3 if deafened else 0})
        for sender_token in participants:
            await self.subscribe(sender_token, audio=not deafened)

    async def subscribe(self, sender_token, audio=True):
        await self.send({'type': 'subscribe', 'sender_token': sender_token, 'audio': audio, 'data': False, 'video': False, 'message_id': 0})

    async def mute(self, muted):
        await self.send({'type': 'mute_audio', 'is_muted': int(muted), 'user_token': self.account_id, 'reason_enum': 1 if muted else 0})

    async def close(self):
        global signer
        try:
            await self.send({'type': 'user_left', 'user_token': self.account_id})
        except Exception:
            pass
        for task in self.tasks:
            task.cancel()
        for recorder in self.recorders:
            await recorder.stop()
        if self.pc:
            await self.pc.close()
        if self.ws:
            await self.ws.close()
        signer = None
