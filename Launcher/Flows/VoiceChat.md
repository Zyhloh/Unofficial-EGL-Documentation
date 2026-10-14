# Voice Chat (Party Voice)

Party voice in EGL v2 has no browser WebRTC. The hosted social overlay manages the party over REST + Epic Connect, fetches RTC credentials from the Party Service, and hands them to the EOS SDK, which joins the room with its own websocket + libwebrtc stack. EGL party voice is the same system as Fortnite party voice: a Fortnite client on Switch joined an EGL party, claimed voice and talked in the same room.

Everything in [Building a client](#building-a-client) was confirmed on 2026-10-14 by a standalone client that created a party, invited an EGL user, and talked with EGL in both directions. Working code: [Examples/VoiceClient](../../Examples/VoiceClient/) ([how to run it](../Voice/ReferenceClient.md)).

## Components

| Component | Role |
| --- | --- |
| Epic Connect `wss://connect.ol.epicgames.com` | connection id (= party connection id), `party.v2.*` events ([Connect](../Social/Connect.md)) |
| Presence `api.epicgames.dev/epic/presence` | online status; without it invites are hidden ([Update Presence](../../EpicGames/PresenceService/Presence/UpdatePresence.md)) |
| Party Service `api.epicgames.dev/epic/party` | parties, invites, member meta, voice credentials ([README](../../EpicGames/PartyService/README.md)) |
| Public Key Service | voice moderation key ([Register Public Key](../../EpicGames/PublicKeyService/PublicKey/Register.md)) |
| Signaling `wss://signaling-service-prod.<region>.live.rtcp.on.epicgames.com/ws` | JSON control channel ([RTC Signaling](../Voice/RTCSignaling.md)) |
| Media server (`join_res.ipv4:udp_port`) | ICE-lite, DTLS-SRTP, Opus ([Media](../Voice/Media.md), [Audio Signing](../Voice/AudioSigning.md)) |
| KWS / SOCS | reporting preference, voice settings ([Moderation](../Voice/Moderation.md), [Settings](../Voice/Settings.md)); not needed to talk |
| EGL only: social overlay, EOS SDK `1.19.4230.0-57929184@LauncherV2`, launcher (`eglv2_lib::social`, `eglv2_lib::eos`) | UI, claim logic, SDK room, tray / taskbar / chimes ([Native Bridge](../Voice/NativeBridge.md)) |

## Building a client

### 1. Token

Any EG1 access token works for every call below (verified with `launcherAppClient2` `34a02cf8f4414e29b15921876da36f9a`, `grant_type=authorization_code`, `token_type=eg1`). Social endpoints (party, presence, SOCS, KWS) take `X-Epic-Agent: epic-social` and a random `X-EPIC-CORRELATION-ID`.

### 2. Epic Connect

Open `wss://connect.ol.epicgames.com/?auth-token=<eg1>&accept-language=en` and speak STOMP ([Connect](../Social/Connect.md)):

```
CONNECT
accept-version:1.2,1.1,1.0
heart-beat:45000,0

^@
```

```
CONNECTED
version:1.2
heart-beat:0,45000
session:3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d

^@
```

```
SUBSCRIBE
id:sub-0
destination:20d0a958-8dd0-490a-bb7f-fe8939e7be44/account/94b1569506b04f9f8557af611e8c5e47

^@
```

`session` is the connection id used in every later step. Heartbeat (`\n`) at least every 45s. Server frames may be binary.

### 3. Leave the old party

One party per account. [Get Parties Summary](../../EpicGames/PartyService/Users/GetUserSummary.md) `GET /epic/party/internal/v2/users/:me`; if `current` exists, [Leave Party](../../EpicGames/PartyService/Members/LeaveParty.md) `DELETE /parties/:current/members/:me`. Not in a party:

```json
{ "invites": [], "join_requests": [] }
```

### 4. Create the party

[Create Party](../../EpicGames/PartyService/Parties/CreateParty.md) `POST /epic/party/internal/v2/parties`:

```json
{
  "config": { "joinability": "INVITE_ONLY", "max_size": 16 },
  "meta": { "created_by": "94b1569506b04f9f8557af611e8c5e47" },
  "join_info": {
    "connection": {
      "id": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
      "deployment_id": "_",
      "meta": { "osName": "Windows", "platformName": "egs", "productName": "Epic Games Launcher" }
    }
  }
}
```

Response: party `id` `2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f`, `chat_conversation_id` `ep-<id>`, `is_reportable: false`, own member with `revision: 0` (full body on the endpoint page). To join an existing party instead: [Join Party](../../EpicGames/PartyService/Members/JoinParty.md).

### 5. Publish presence

[Update Presence](../../EpicGames/PresenceService/Presence/UpdatePresence.md) `POST /epic/presence/internal/v1/_/:me/presence/:connectionId` with `X-HTTP-Method-Override: PATCH`:

```json
{
  "status": "online",
  "party": {
    "id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "type": "INVITE_ONLY",
    "timestamp": "2026-10-14T16:53:45.111Z",
    "memberCount": 1,
    "clientJoinable": true
  },
  "conn": { "props": {} }
}
```

Skip it and friends see you Offline and EGL does not show your invite.

### 6. Invite

[Send Party Invite](../../EpicGames/PartyService/Invites/SendInvite.md) `POST /epic/party/internal/v2/users/:invitee/invites/:me?auto=false`, no body:

```json
{
  "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
  "sent_by": "94b1569506b04f9f8557af611e8c5e47",
  "auto": false,
  "meta": {},
  "sent_to": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
  "sent_at": "2026-10-14T16:53:45.315Z",
  "updated_at": "2026-10-14T16:53:45.315Z",
  "expires_at": "2026-10-14T17:53:45.315Z"
}
```

Wait on Epic Connect for `party.v2.INVITE_EXPIRED` (invite consumed) and `party.v2.MEMBER_JOINED` with the invitee's `account_id` ([event examples](../../EpicGames/PartyService/README.md#realtime-events)). Voice can be joined before anyone else is in the party.

### 7. Voice credentials

[Get Voice Room Connection](../../EpicGames/PartyService/Conferences/ConnectVoiceRoom.md) `POST /epic/party/internal/v2/parties/:partyId/members/:me/conferences/connection`, no body:

```json
{
  "providers": {
    "rtcp": {
      "participant_token": "<jwt>",
      "client_base_url": "wss://signaling-service-prod.use2.live.rtcp.on.epicgames.com/ws?ms=wss://10.0.12.34:8443/6c1e2f3a-4b5d-4e6f-8a9b-0c1d2e3f4a5b&p=epicparty&t=MTAuMC4xMi4zNHwxMjM0NTY3OA.3KnMtEhf9pnxsRtWn1QSq3d0j0wPmuJ7oN_ruEZsWW4",
      "room_name": "pv2-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f"
    }
  }
}
```

`participant_token`: EdDSA JWT, `iss: rtcp-manager`, `sub: CONNECT`, `clientId` = account id, `conferenceId` = room name, `namespace: epicparty`, 2h lifetime (decoded claims on the endpoint page). Fetch again when it expires.

### 8. Claim voice

[Update Member Meta](../../EpicGames/PartyService/Members/UpdateMemberMeta.md) `PATCH /epic/party/internal/v2/parties/:partyId/members/:me/meta`:

```json
{
  "revision": 0,
  "update": {
    "active_voice_connection": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
    "platform_name": "Windows",
    "product_name": "Epic Games Launcher"
  },
  "connection": {
    "id": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
    "deployment_id": "_",
    "active_in_party_voice_room": true
  }
}
```

The response carries the new member `revision` (`1`); keep it for the release PATCH. Other members get `party.v2.MEMBER_STATE_UPDATED`. One device per account holds voice.

### 9. Voice moderation key

Generate an Ed25519 key pair and register the public key: [Register Public Key](../../EpicGames/PublicKeyService/PublicKey/Register.md) `POST https://publickey-service-prod.ecbc.live.use1a.on.epicgames.com/publickey/v2/publickey/` (plain EG1, no social headers):

```json
{ "algorithm": "ed25519", "key": "KjiNzdIo9qri4fFyUm0u7zYV00jgNYjFxWgYkrdVH/w=" }
```

Response `{ "jwt": "<jwt>" }` = `signed_public_key` (claims `account_id`, `generated`, `key_guid`, `kid` `20230621`, `key`, `expiration`, `type: legacy`).

### 10. Signaling

Open `client_base_url` (plain text JSON, `" "` keepalive every 5s, no WebSocket pings) and send `join` ([RTC Signaling](../Voice/RTCSignaling.md#join)):

```json
{
  "type": "join",
  "ticket": "<participant_token>",
  "user_token": "94b1569506b04f9f8557af611e8c5e47",
  "options": ["subscribe", "dtx", "rtcp_rsize", "new_audio_only_reasons", "v2", "unified_plan", "speaking", "speaking_self_only", "ras_csrc", "reserved_audio_streams", "signed_audio"],
  "version": "1.19.4230.0-57929184@LauncherV2",
  "device": { "os": "Windows", "model": "", "manufacturer": "", "online_platform_type": "0" },
  "status": { "is_muted": 0, "audio_muted_reason": 0, "is_audio_only": 1, "reason_enum": 6, "is_screencast": 0 },
  "connection_id": "B5BE40C1389FCEA61DF04E587C8C1833",
  "video": { "width": 0, "height": 0, "codecs": [] },
  "voice_moderation": { "signed_public_key": "<jwt>" }
}
```

The server answers `join_res` with `status: 0`, `ssrc.audio`, `reserved_audio_streams`, `ice { ufrag, pwd }`, `fingerprint`, `ipv4`, `udp_port`, `ptime: 60` (full example on the signaling page). `dominant_speaker` can arrive first.

### 11. Media

Build a remote SDP offer from `join_res` (ice-lite, `a=setup:actpass`, BUNDLE, one `recvonly` section + one `sendonly` section per reserved SSRC, Opus PT 100, one host candidate), create your answer with outgoing SSRC = `join_res.ssrc.audio`, send `join_update { fingerprint: { fingerprint: "sha-256 <your cert fingerprint>" } }`, then run ICE (controlling) and DTLS (client, ECDHE-RSA suites). Details: [Media](../Voice/Media.md).

### 12. Participants

For every `join_res.users[]` entry and every `user_joined`, send:

```json
{ "type": "subscribe", "sender_token": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b", "audio": true, "data": false, "video": false, "message_id": 0 }
```

Without it no audio from that participant is forwarded. Incoming audio arrives on the reserved SSRCs with the speaker's SSRC as CSRC. `speaking`, `mute_audio`, `audio_only`, `network_status`, `user_left` update state.

### 13. Send audio

Encode Opus 48kHz stereo, 60ms frames, sign each payload ([Audio Signing](../Voice/AudioSigning.md)):

```
payload = opus || u32be(counter) || Ed25519(opus || u32be(counter) || "pv2-<partyId>") || 00 00 00 01
```

Strip the 72-byte trailer from incoming payloads before decoding. Mute / deafen: [Settings](../Voice/Settings.md#on-the-wire).

### 14. Leave

1. Signaling `{ "type": "user_left", "user_token": "<me>" }`, close the websocket and peer connection.
2. [Update Member Meta](../../EpicGames/PartyService/Members/UpdateMemberMeta.md) with the current `revision` and `active_in_party_voice_room: false`.
3. [Leave Party](../../EpicGames/PartyService/Members/LeaveParty.md) `DELETE /parties/:partyId/members/:me`.
4. Close Epic Connect.

## Minimal client checklist

- Publish presence after connecting / creating the party, or the invite never shows in EGL.
- Leave `current` before creating a party (one party per account).
- Always join moderated: `signed_audio` option + `voice_moderation.signed_public_key`. The first joiner fixes the room mode; an unmoderated first joiner breaks EGL with `VoiceModerationModeMismatch`.
- Register the key with `algorithm: "ed25519"` on `/publickey/v2/publickey/` (not `/publickey/v2/so/`).
- Signaling keepalive is a `" "` text frame every 5s; disable WebSocket ping frames (server closes with `1002`).
- `subscribe` every participant (`join_res.users[]` and each `user_joined`); `join_res.users` was always empty in captures.
- Remote SDP: ice-lite, server `actpass`, client answers `active`; client is ICE controlling and nominates.
- DTLS: offer ECDHE-RSA cipher suites (server cert is RSA). aiortc's default ECDSA-only list is silently ignored.
- Outgoing RTP SSRC = `join_res.ssrc.audio`, PT `100`, Opus 48kHz stereo, 60ms frames.
- Sign every outgoing payload; counter from `0`, `+1` per packet, never backwards; context = room name.
- Strip the 72-byte trailer (or 4 bytes for version `0`) from incoming payloads before Opus decoding.
- Release voice (`active_in_party_voice_room: false`) and leave the party on exit.

## How EGL does it

1. Launcher signs the SDK in: exchange code -> `EOS_Auth_Login`, EG1 token pushed with `EOS_Auth_SetAccessTokenOverride`. The SDK announces the overlay URL and its bridge scripts; the launcher loads the overlay in the `social` WebView2 and exposes host object `eosBridge`. See [Native Bridge](../Voice/NativeBridge.md).
2. Overlay connects to Epic Connect and receives `core.connect.v1.connected` `{ connectionId }` (`epicConnectId`).
3. Overlay loads party state ([Get Parties Summary](../../EpicGames/PartyService/Users/GetUserSummary.md)) and voice settings ([Query User Settings](../../EpicGames/SOCSService/Settings/QueryUserSettings.md) -> `update-voice-settings` to the SDK).
4. Party created or joined ([Create Party](../../EpicGames/PartyService/Parties/CreateParty.md), [Join Party](../../EpicGames/PartyService/Members/JoinParty.md), [Join Group Party](../../EpicGames/PartyService/Groups/JoinGroupParty.md), [Send Party Invite](../../EpicGames/PartyService/Invites/SendInvite.md), [Send Join Request](../../EpicGames/PartyService/JoinRequests/SendJoinRequest.md)).
5. Voice claim (`CheckActiveVoiceClaims`), recorded in member meta `active_voice_connection` / `platform_name` / `product_name`:
   - meta points to a live first-party connection -> that device holds voice (`current-active-device`), nothing to do;
   - `product_name` is another product -> do not claim;
   - meta points to a dead connection of the same os / platform / product, or a previous connection id of this client, or a forced reclaim -> claim;
   - otherwise claim only if this device's connection is the oldest live first-party connection.
   A second member joining a party with no voice holder triggers `refresh-active-party-voice-check` (Get Party + claim check).
6. Eligibility gate must be `yes` (age verification, cabined mode, parental limit, social ban, reporting disclosure, voice setting; see [Settings](../Voice/Settings.md#voice-eligibility-gate)).
7. Overlay intent `connect-party-voice-room` `{ partyId, currentMemberRevision, epicConnectId, osName, productName, voiceBlockedIds }`:
   1. [Get Voice Room Connection](../../EpicGames/PartyService/Conferences/ConnectVoiceRoom.md).
   2. To the SDK (feature `party`): `set-blocked-participants` `{ participants: [{ id }] }`, then `connect-voice-room` `{ participantToken, roomName, clientBaseUrl, roomSettings: { AudioInputDeviceMode: "AlwaysOn" } }`.
   3. [Update Member Meta](../../EpicGames/PartyService/Members/UpdateMemberMeta.md) claims voice.
8. SDK registers its moderation key, joins the room (`join` -> `join_res` -> `join_update`), runs ICE / DTLS, signs audio. Status flows back as `voice-room.status` (`connecting` -> `connected`). On `connected` the overlay re-sends per-member volume / mute (`set-participant-audio`) and `update-voice-settings { inputMuted, audioEnabled }`.
9. In call: SDK publishes `voice-room.participants[] { id, muted, speaking, notListening, voiceChatOff }` and `pttActive`; overlay draws speaking rings and sends `voice-party-state-changed` to the launcher (tray / taskbar). Mute, deafen, PTT, device and volume changes are `update-voice-settings` intents. Deafen also updates `active_in_party_voice_room` (1s debounce).
10. Token refresh: SDK state `request-session-info { roomName, requestUniqueIndex }` -> overlay calls Get Voice Room Connection again -> intent `update-session-info { participantToken, roomName, clientBaseUrl, requestUniqueIndex }`.
11. Membership upkeep: `party.v2.*` events update the roster. If the local member becomes `suspended`, the overlay calls [Keep Alive](../../EpicGames/PartyService/Members/KeepAlive.md). Network loss disconnects voice locally.
12. Leave voice / party: `disconnect-party-voice-room` -> SDK `disconnect-voice-room` (`user_left`) + Update Member Meta (`active_in_party_voice_room: false`); leaving the party is [Leave Party](../../EpicGames/PartyService/Members/LeaveParty.md). Voice also drops when eligibility turns `no:*`, when another device claims voice, or when the party is left / disbanded.
13. Analytics: the SDK emits a party-leave row via `EOS_PartyFeature_AddNotifyLeaveAnalytics`; the launcher correlates it with the Epic Connect member-exit event (`telemetry::party_leave`).
14. Reporting (optional): [Moderation](../Voice/Moderation.md).

## States and events (EGL)

| Where | Name | Meaning |
| --- | --- | --- |
| overlay -> launcher | `voice-party-state-changed` `not-in-party` / `in-party` / `muted` / `deafened` | tray + taskbar artwork (`in-party-speaking` accepted, not sent by this build) |
| SDK -> overlay | `voice-room.status` `none` / `connecting` / `connected` / `error` | connection spinner, `error` releases the local claim |
| SDK -> overlay | `voice-room.participants[]` | `muted`, `speaking`, `notListening`, `voiceChatOff` per member |
| SDK -> overlay | `request-session-info` | token refresh needed |
| SDK -> overlay | `current-active-device` | which device holds voice |
| SDK -> launcher | `EOS_UI` audio chime `PartyUserJoined`, `PartyUserLeft`, `PushToTalkActivated`, `PushToTalkDeactivated`, `VoiceMuted`, `VoiceUnmuted`, `PartyJoinabilityChanged`, `PartyMessageReceived` | launcher plays the chime |
| overlay chimes intent | `party-local-user-joined`, `party-local-user-left`, `party-local-user-switched`, `party-users-joined`, `party-users-left`, `party-joinability-changed`, `message-received`, `party-voice-mute-changed` | gated by SOCS chime settings |
| Epic Connect | `party.v2.MEMBER_JOINED` ... `party.v2.PARTY_UPDATED` | see [Party Service README](../../EpicGames/PartyService/README.md#realtime-events) |

## Not confirmed

- `join_res.users` populated (always `[]`; existing participants came as `user_joined`).
- Server messages `transfer`, `kick_user`, `remote_mute_audio`, `subscribe_res`, `audio_streams_mapping` (SDK only).
- Wire format of join rejections other than the client-side `VoiceModerationModeMismatch` message.
- The report upload ([Moderation](../Voice/Moderation.md#report-flow)).
