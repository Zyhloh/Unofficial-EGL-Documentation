import asyncio
import json
import math
import os
import struct
import tempfile
import wave

from auth import Auth
from connect import Connect
from epic import Epic
from voice import VoiceRoom, new_signing_key

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config():
    with open(os.path.join(HERE, 'config.json'), encoding='utf-8') as f:
        return json.load(f)


def tone(path):
    rate = 48000
    frames = bytearray()
    for i in range(rate * 4):
        t = i / rate
        value = int(12000 * math.sin(2 * math.pi * (440 if int(t) % 2 == 0 else 660) * t)) if t % 1.0 < 0.5 else 0
        frames += struct.pack('<h', value)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(frames))
    return path


async def run():
    config = load_config()
    send_audio = config['sendAudio'] or tone(os.path.join(tempfile.gettempdir(), 'egl-voice-tone.wav'))
    token = Auth(config).token()
    me = token['account_id']
    epic = Epic(token)
    connect = Connect(token['access_token'], me)

    connection_id = await connect.start()
    await epic.leave_current_party()
    party = await epic.create_party(connection_id, config['connectionMeta'])
    party_id = party['id']
    revision = party['members'][0]['revision']
    await epic.set_presence(connection_id, {
        'id': party_id,
        'type': 'INVITE_ONLY',
        'timestamp': party['created_at'],
        'memberCount': 1,
        'clientJoinable': True,
    })
    print('party', party_id)

    invitee = config['inviteAccountId']
    if invitee:
        await epic.invite(invitee)
        print('invited', invitee)
        try:
            await connect.wait_for(
                lambda e: e.get('type') == 'party.v2.MEMBER_JOINED' and (e.get('payload') or {}).get('account_id') == invitee,
                config['inviteWaitSeconds'],
            )
        except asyncio.TimeoutError:
            print('invite not accepted in time')

    credentials = await epic.voice_credentials(party_id)
    claim = dict(config['memberMeta'], active_voice_connection=connection_id)
    revision = (await epic.update_member_meta(party_id, revision, connection_id, claim, True))['revision']

    signing_key, public_key = new_signing_key()
    signed_public_key = await epic.register_public_key(public_key)

    room = VoiceRoom(credentials, me, send_audio, os.path.expanduser(config['recordDir']))
    try:
        await room.connect(signing_key, signed_public_key)
        print('in voice room', credentials['room_name'])
        await asyncio.sleep(config['durationSeconds'])
    finally:
        await room.close()
        try:
            await epic.update_member_meta(party_id, revision, connection_id, claim, False)
        except RuntimeError:
            pass
        await epic.leave_party(party_id)
        await connect.close()
        await epic.close()
        print('left party')


if __name__ == '__main__':
    asyncio.run(run())
