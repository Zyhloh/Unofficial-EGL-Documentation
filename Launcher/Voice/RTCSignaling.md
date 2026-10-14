# Voice - RTC Signaling

The control channel between a party voice participant and the media server: a websocket to `client_base_url` from [Get Voice Room Connection](../../EpicGames/PartyService/Conferences/ConnectVoiceRoom.md). Every message below was captured on 2026-10-14, both from EGL's own EOS SDK (`1.19.4230.0-57929184@LauncherV2`, hooked) and from a standalone client that talked to EGL in both directions. A second live pass the same day added populated `join_res.users`, `kick_user` and mute timing. Messages marked "not observed" come only from the SDK binary (`LibRtc::*`).

Media (SDP / ICE / DTLS / RTP) is on [Media](Media.md), audio packet signing on [Audio Signing](AudioSigning.md), the end-to-end order on [Voice Chat](../Flows/VoiceChat.md).

## Stack (EGL)

| Layer | Implementation |
| --- | --- |
| Room API | `FRTCRoom` / `RTCRoomHelper`, source `PartiesInternalApi` (other sources: `RtcApi`, `LobbyApi`, `PartiesApi`) |
| Client library | `LibRtc` (Epic, "RTCP"): `FConferenceService`, `FConnectionService`, `FMediaServiceClient`, `FRtcpConnection` |
| Control channel | websocket (`FLwsWebSocket`, libwebsockets), JSON text messages with a `type` field |
| Media | libwebrtc (`ThirdParty\WebRTC\7204`), one `PeerConnection` per room, Opus, DTLS-SRTP, RTP/RTCP mux |
| Audio I/O | XAudio2 (render) and RtAudio (capture) through `FRTCAudio`, WebRTC APM (AEC3 / NS / AGC1 or AGC2) |

## Connection

- Open `client_base_url` unchanged (`wss://signaling-service-prod.<region>.live.rtcp.on.epicgames.com/ws?ms=...&p=epicparty&t=...`). No extra headers or subprotocols needed.
- Frames are text, one JSON object per frame, no envelope besides `type`.
- Keepalive: a text frame containing a single space `" "`, every 5s, in both directions. The server also sends `" "`; ignore it.
- Do not send WebSocket ping control frames: the server closes the socket with `1002` (protocol error). Disable library auto-ping.
- Close: send `user_left` for yourself, then close the socket.

Captured order (standalone client joining a room where EGL already was):

1. client `join`
2. server `dominant_speaker` (current speaker, can arrive before `join_res`)
3. server `join_res`
4. client `join_update` (DTLS fingerprint), then ICE / DTLS / SRTP start ([Media](Media.md))
5. existing participants: either inside `join_res.users` or as separate `user_joined` messages (both seen, see below)
6. client `subscribe` for each of them
7. server `mute_audio`, `audio_only`, `network_status`, `speaking` as state changes
8. server `user_left` for each participant that leaves; `kick_user` when the party is disbanded

`join_res.users` is a list of JSON-encoded strings, not objects. Each string is a complete `user_joined` message for a participant already in the room; parse it with a JSON decoder before use. It was `[]` in the first captures (existing participants then arrived as separate `user_joined` messages about 100ms after `join_res`) and populated in the second pass, where the server also sent the same participant as a `user_joined` message right after `join_res`. Handle both and de-duplicate by `user_token`: subscribe to every parsed `join_res.users[]` entry and every `user_joined`.

## Client -> server

### join

Sent by EGL:

```json
{
  "type": "join",
  "ticket": "<jwt>",
  "user_token": "94b1569506b04f9f8557af611e8c5e47",
  "options": [
    "subscribe",
    "dtx",
    "rtcp_rsize",
    "new_audio_only_reasons",
    "v2",
    "unified_plan",
    "speaking",
    "speaking_self_only",
    "ras_csrc",
    "reserved_audio_streams",
    "signed_audio"
  ],
  "version": "1.19.4230.0-57929184@LauncherV2",
  "device": {
    "os": "Windows",
    "model": "",
    "manufacturer": "",
    "online_platform_type": "0"
  },
  "status": {
    "is_muted": 1,
    "audio_muted_reason": 1,
    "is_audio_only": 1,
    "reason_enum": 6,
    "is_screencast": 0
  },
  "connection_id": "B5BE40C1389FCEA61DF04E587C8C1833",
  "video": {
    "width": 0,
    "height": 0,
    "codecs": []
  },
  "voice_moderation": {
    "signed_public_key": "<jwt>"
  }
}
```

| Field | Notes |
| --- | --- |
| `ticket` | `participant_token` from the Party Service |
| `user_token` | own account id (= token `clientId`) |
| `options` | conference features (`FMediaServiceClientImpl::GenerateConferenceFeatures`). `signed_audio` only with `voice_moderation` |
| `version` | SDK version string; the standalone client sent the same value |
| `device.online_platform_type` | `"0"` on Windows |
| `status` | initial state. `is_audio_only: 1` + `reason_enum: 6` = no video. EGL joins muted (`is_muted: 1`, `audio_muted_reason: 1`) and unmutes right after `join_update`; joining with `is_muted: 0`, `audio_muted_reason: 0` also works |
| `connection_id` | random 32 hex chars, uppercase, new per join |
| `voice_moderation.signed_public_key` | JWT from [Register Public Key](../../EpicGames/PublicKeyService/PublicKey/Register.md). Omitted together with `signed_audio` for an unmoderated join |

The first participant fixes the room's moderation mode. Always join with `signed_audio` + `signed_public_key`: a room created by an unmoderated join makes every later EGL join fail with `VoiceModerationModeMismatch` ("Unable to connect to voice chat"). See [Moderation](Moderation.md#voice-moderation-key).

Fields in the SDK serializer that were not sent: `data_streams [{ ordered, protocol, type, id }]`, `reserved_audio_streams_max_pool_size`, `test { force_proximity_radius }`, `voice_moderation.mode`.

### join_update

Sent once after `join_res`, carrying the client's DTLS certificate fingerprint:

```json
{
  "type": "join_update",
  "fingerprint": {
    "fingerprint": "sha-256 7E:2D:4C:6B:8A:0F:1E:3D:5C:7B:9A:8F:6E:4D:2C:1B:0A:9F:8E:7D:6C:5B:4A:39:28:17:06:F5:E4:D3:C2:B1"
  }
}
```

No ICE credentials or candidates are sent; the server is ICE-lite and learns the client from its STUN checks ([Media](Media.md#ice)).

### subscribe

Required once per remote participant, or the server forwards no audio from them:

```json
{
  "type": "subscribe",
  "sender_token": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
  "audio": true,
  "data": false,
  "video": false,
  "message_id": 0
}
```

`audio: false` stops receiving that sender (EGL's deafen sends it for every participant, undeafen sends `audio: true` again).

### mute_audio

```json
{
  "type": "mute_audio",
  "is_muted": 1,
  "user_token": "94b1569506b04f9f8557af611e8c5e47",
  "reason_enum": 1
}
```

| `is_muted` / `reason_enum` | When EGL sent it |
| --- | --- |
| `0` / `0` | unmuted (after any of the below) |
| `1` / `1` | mic muted (`update-voice-settings { inputMuted: true }`, SDK `AudioDisabled`); also the first step of deafen |
| `1` / `2` | right after `join_update`, immediately followed by `0` / `0` (initial state sync); peers see this pair every time EGL joins |
| `1` / `3` | deafen (`audioEnabled: false`, SDK `AudioNotListeningDisabled`), sent after `1` / `1`, together with `subscribe audio: false` per participant |

Deafen captured as: `mute_audio 1/1`, `mute_audio 1/3`, `subscribe { audio: false }`. Undeafen: `mute_audio 0/0`, `subscribe { audio: true }`. The SDK maps `reason_enum 3` on a peer to "not listening" (inferred from `AudioNotListeningDisabled`).

### block

```json
{
  "type": "block",
  "sender_token": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
  "block": true
}
```

On every `user_joined` EGL sent `block true`, `subscribe { audio: true }`, `block false` in the same millisecond (re-applying its blocked set, `set-blocked-participants`). A blocked participant keeps `block: true`.

### user_left

```json
{
  "type": "user_left",
  "user_token": "94b1569506b04f9f8557af611e8c5e47"
}
```

Sent with the own account id before closing. EGL also sent it once right before re-joining a room.

### Not observed (from the SDK)

| `type` | Fields |
| --- | --- |
| `audio_only` | `is_audio_only`, `user_token`, `reason_enum` |
| `video_resolution` | `user_token`, `sender_token`, `resolution`, `framerate` |
| `position` | `position` (proximity rooms) |

## Server -> client

### join_res

```json
{
  "type": "join_res",
  "status": 0,
  "user_token": "94b1569506b04f9f8557af611e8c5e47",
  "abort_on_inactivity": true,
  "crypto": { "key_params": "" },
  "fingerprint": {
    "fingerprint": "sha-256 5C:1E:9A:7F:3D:2B:8E:4A:6F:0C:1D:2E:3B:4A:59:68:77:86:95:A4:B3:C2:D1:E0:F1:A2:B3:C4:D5:E6:F7:08"
  },
  "ice": {
    "pwd": "RSGJwJCR1N+2gKgzgHmOvWcREmsCRAXC",
    "servers": [],
    "ufrag": "oHnpOjDxTPw"
  },
  "ipv4": "203.0.113.24",
  "ipv6": "2001:db8:48d:5b0c::24",
  "udp_port": 41872,
  "tcp_port": 0,
  "ssltcp_port": 43120,
  "maxaveragebitrate": 0,
  "options": [ "speaking", "dtx", "reserved_audio_streams", "unified_plan", "ras_csrc", "signed_audio" ],
  "ptime": 60,
  "reserved_audio_streams": [
    { "ssrc": 20 },
    { "ssrc": 30 },
    { "ssrc": 40 },
    { "ssrc": 50 },
    { "ssrc": 60 }
  ],
  "ssrc": {
    "audio": 10,
    "video": 11,
    "video_rtx": 15,
    "video_sim": [ 12, 13, 14 ],
    "video_sim_rtx": [ 16, 17, 18 ]
  },
  "stream": {
    "audio": { "audio_muted_reason": 1, "is_muted": true, "ssrc": 10 },
    "status": 0,
    "stream_id": "default",
    "video": {
      "audio_only_reason": 6,
      "height": 0,
      "is_audio_only": 1,
      "is_screencast": 0,
      "rtx_ssrc": 15,
      "sim_rtx_ssrc": [ 16, 17, 18 ],
      "sim_ssrc": [ 12, 13, 14 ],
      "ssrc": 11,
      "width": 0
    }
  },
  "users": [],
  "video": { "codecs": [] },
  "video_max_bitrate_p2p": 800000,
  "video_max_size": 0
}
```

| Field | Use |
| --- | --- |
| `status` | `0` = joined. Anything else: see reject reasons below |
| `ssrc.audio` | SSRC your outgoing audio RTP must use. Assigned per join: `10` for the first participant, `70` for the second in the captures |
| `reserved_audio_streams[].ssrc` | SSRCs the server sends mixed-in remote audio on; one receive stream per entry |
| `ice.ufrag` / `ice.pwd` | server ICE credentials for the remote SDP. `ice.servers` was empty |
| `fingerprint.fingerprint` | server DTLS certificate fingerprint (`<hash> <hex>`); the certificate looked static across sessions |
| `ipv4` / `udp_port` | the single host candidate. `ipv6` and `ssltcp_port` were present but not needed; `tcp_port` was `0` |
| `ptime` | `60`; Opus frame duration in ms |
| `options` | the subset of requested options the server enabled; `signed_audio` echoed only for moderated joins |
| `stream` | your own initial stream state, mirrors the `join` `status` |
| `users` | participants already in the room, each a JSON string holding a full `user_joined` message ([example](#join_res-with-participants)); can also be `[]` (then the participants come as `user_joined`) |
| `abort_on_inactivity`, `maxaveragebitrate`, `video*`, `crypto` | not needed for audio |

### join_res with participants

Captured joining a room where an EGL user was already talking (only the fields that differ from the example above, plus `users`):

```json
{
  "type": "join_res",
  "status": 0,
  "user_token": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "ssrc": { "audio": 70, "video": 71, "video_rtx": 75, "video_sim": [ 72, 73, 74 ], "video_sim_rtx": [ 76, 77, 78 ] },
  "reserved_audio_streams": [
    { "ssrc": 80 },
    { "ssrc": 90 },
    { "ssrc": 100 },
    { "ssrc": 110 },
    { "ssrc": 120 }
  ],
  "stream": {
    "audio": { "audio_muted_reason": 0, "is_muted": false, "ssrc": 70 },
    "status": 0,
    "stream_id": "default",
    "video": { "audio_only_reason": 6, "height": 0, "is_audio_only": 1, "is_screencast": 0, "rtx_ssrc": 75, "sim_rtx_ssrc": [ 76, 77, 78 ], "sim_ssrc": [ 72, 73, 74 ], "ssrc": 71, "width": 0 }
  },
  "users": [
    "{\"metadata\":{\"online_platform_type\":\"0\",\"platform\":\"windows\"},\"ssrc\":{\"audio\":10,\"rtx\":15,\"video\":11},\"status\":{\"audio_muted_reason\":0,\"is_audio_only\":1,\"is_muted\":0,\"is_screencast\":0,\"reason\":\"unsupported\"},\"streams\":[{\"audio\":{\"audio_muted_reason\":0,\"is_muted\":false,\"ssrc\":10},\"stream_id\":\"default\",\"video\":{\"audio_only_reason\":6,\"height\":0,\"is_audio_only\":1,\"is_screencast\":0,\"rtx_ssrc\":15,\"sim_rtx_ssrc\":[16,17,18],\"sim_ssrc\":[12,13,14],\"ssrc\":11,\"width\":0}}],\"type\":\"user_joined\",\"user_token\":\"94b1569506b04f9f8557af611e8c5e47\",\"voice_moderation\":{\"signed_public_key\":\"<jwt>\"}}"
  ]
}
```

Parsed, the string is the [user_joined](#user_joined) message of `94b1569506b04f9f8557af611e8c5e47` (audio SSRC `10`). The new participant got audio SSRC `70` and reserved streams `80`-`120`; EGL's audio then arrived on SSRC `80` with CSRC `10`.

```python
for raw in join_res["users"]:
    user = json.loads(raw) if isinstance(raw, str) else raw
    on_user_joined(user)
```

### dominant_speaker

```json
{
  "type": "dominant_speaker",
  "user_token": "94b1569506b04f9f8557af611e8c5e47"
}
```

### user_joined

A participant that joined (EGL client, moderated):

```json
{
  "type": "user_joined",
  "user_token": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
  "metadata": { "online_platform_type": "0", "platform": "windows" },
  "ssrc": { "audio": 70, "rtx": 75, "video": 71 },
  "status": {
    "audio_muted_reason": 1,
    "is_audio_only": 1,
    "is_muted": 1,
    "is_screencast": 0,
    "reason": "unsupported"
  },
  "streams": [
    {
      "audio": { "audio_muted_reason": 1, "is_muted": true, "ssrc": 70 },
      "stream_id": "default",
      "video": {
        "audio_only_reason": 6,
        "height": 0,
        "is_audio_only": 1,
        "is_screencast": 0,
        "rtx_ssrc": 75,
        "sim_rtx_ssrc": [ 76, 77, 78 ],
        "sim_ssrc": [ 72, 73, 74 ],
        "ssrc": 71,
        "width": 0
      }
    }
  ],
  "voice_moderation": { "signed_public_key": "<jwt>" }
}
```

`ssrc.audio` is the participant's own audio SSRC; it appears as the CSRC of the forwarded packets on the reserved streams ([Media](Media.md#rtp)). `voice_moderation.signed_public_key` is their key JWT (claims as in [Register Public Key](../../EpicGames/PublicKeyService/PublicKey/Register.md)); verify their audio with the `key` claim. Send `subscribe` for `user_token`.

### user_left

```json
{
  "type": "user_left",
  "user_token": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b"
}
```

### speaking

```json
{
  "type": "speaking",
  "user_token": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
  "is_speaking": 1,
  "stream_id": "default"
}
```

Sent for every participant including yourself, `is_speaking` `1` / `0`.

### mute_audio

```json
{
  "type": "mute_audio",
  "user_token": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
  "is_muted": true,
  "reason_enum": 2,
  "stream_id": "default"
}
```

Relayed client `mute_audio`; `is_muted` is a boolean here. Same `reason_enum` table as above.

While EGL is mic-muted (`is_muted: true`, `reason_enum: 1`) it sends no RTP at all: in a 16s mute the forwarded stream dropped from 16-17 Opus packets/s (60ms frames) to 0 from the `mute_audio` until the unmute (`is_muted: false`, `reason_enum: 0`), then resumed at the same rate. Treat a muted participant's silence as normal, not as a media failure.

### kick_user

```json
{
  "type": "kick_user"
}
```

No other fields (the SDK parser also reads an optional `reason`; none was sent). Captured when the party was disbanded (the other member left a 2-member party): the server sent `user_left` for the departing member, then `kick_user` in the same millisecond, about 1.3s after `party.v2.MEMBER_LEFT` / `MEMBER_EXPIRED_PARTY_DISBANDED` on Epic Connect. The room is closed; leave voice (inferred to surface as the SDK result `KickedFromConference`).

### audio_only

```json
{
  "type": "audio_only",
  "user_token": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
  "is_audio_only": 1,
  "reason": "unsupported",
  "reason_enum": 6,
  "stream_id": "default"
}
```

### network_status

```json
{
  "type": "network_status",
  "user_token": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
  "uplink": 0,
  "downlink": 0
}
```

### Not observed (from the SDK)

| `type` | Fields |
| --- | --- |
| `remote_mute_audio` | `is_muted` (server-side hard mute of the local user) |
| `screencast` | `is_screencast`, `user_token` |
| `transfer` | `url`, `ticket` (media server migration: join `url` with the new `ticket`, then leave the old conference) |
| `control_secondary` | `enabled`, `audio_sending_enabled` |
| `subscribe_res` | `status` (`LibRtc::ESubscribeResStatus`), `message_id` |
| `audio_streams_mapping` | `mapping` |

## Reject reasons

`LibRtc` result strings: `CredentialAccessDenied`, `RoomNotFound`, `RoomFull`, `TokenBanned`, `ServerUnsupportedApiVersion`, `ServerGenericError`, `RoomOptionsMismatch`, `VoiceModerationModeMismatch`, `PublicKeyValidationFailed`, `DuplicateSession` ("same user connected from elsewhere"), `KickedFromConference`, `ServerTermination`, `ServerUnavailable`. Only `VoiceModerationModeMismatch` was reproduced (EGL joining a room first joined without `signed_audio`). The wire encoding of the reasons was not captured.

## EGL (SDK) side

- `PartyFeature::HandleConnectVoiceRoomIntent` receives `connect-voice-room` `{ participantToken, roomName, clientBaseUrl, roomSettings }`. One room per local user (`Connection to multiple rooms is not supported`).
- `FRTCRoom::Join` keeps `clientBaseUrl` as `MsUrlRequested`; `RTCSessionResolver` can swap it after a `transfer` (`MsUrlActual`, `UrlAndTokenReplaced`). For analytics the SDK derives `RegionName` from the `*.rtcp.on.epicgames.com` host and `SignalingServiceType` from the `signaling-service-` segment.
- Local mute / deafen arrive as `update-voice-settings` (`inputMuted`, `audioEnabled`) and become the `mute_audio` / `subscribe` sequences above. Per-participant volume / local mute (`set-participant-audio`) stay local.
- `set-blocked-participants` `{ participants: [{ id }] }` drives `block`.
- Remote events update `FVoiceRoomState`, published to the overlay as `voice-room.participants[]` `{ id, muted, speaking, notListening, voiceChatOff }`.
- Token refresh: the SDK sets `request-session-info` `{ roomName, requestUniqueIndex }` (`PartyFeature::OnSessionInfoRequest`, timeout `SessionInfoRequestTimeoutSeconds`); the overlay calls the Party Service again and answers `update-session-info` `{ participantToken, roomName, clientBaseUrl, requestUniqueIndex }`.
- Leave: `disconnect-voice-room` -> `PartyFeature::DisconnectPartyConference` -> `user_left` + websocket close, then a `party-leave-analytics` row (`AccountId`, `RoomName`, `DisconnectReason`, `AvgRoundTripTimeSec`, `IncomingAvgPacketLossFraction`, `OutgoingAvgPacketLossFraction`, `AvgJitterBufferDelaySec`, `VoiceModerationEnabled`, `VoiceModerationEnabledDurationSec`, `VoiceChatOutgoingActivitySec`, `VoiceChatIncomingActivitySec`) for `EOS_PartyFeature_AddNotifyLeaveAnalytics`.
- SDK logs redact message bodies (`[MediaService] Sending message. Type[...] Json[<Redacted>]`); the bodies above come from hooking the websocket send / receive.
