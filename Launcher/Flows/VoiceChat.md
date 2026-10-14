# Voice Chat (Party Voice)

Party voice in EGL v2 has no browser WebRTC. The hosted social overlay manages the party over REST + Epic Connect, fetches RTC credentials from the Party Service, and hands them to the EOS SDK, which joins the room with its own websocket + libwebrtc stack. The launcher (Rust) only hosts the webview, signs the SDK in, and renders tray / taskbar / chime feedback.

## Components

| Component | Role |
| --- | --- |
| Social overlay (`social-overlay@2.9.2`, `client-HGNfKPY5.js`, `app-Z6xvdTog.js`) | party UI, party REST calls, voice claim logic, settings, report dialog |
| Party Service `api.epicgames.dev/epic/party` | parties, members, invites, member meta, voice room credentials ([README](../../EpicGames/PartyService/README.md)) |
| Epic Connect (`wss://connect.ol.epicgames.com`) | connection id used as party connection, `party.v2.*` events ([Connect](../Social/Connect.md)) |
| EOS SDK `1.19.4230.0-57929184@LauncherV2` | internal party feature: RTC room, devices, mute, moderation recording, Emerald upload |
| Media server (`client_base_url`, `*.rtcp.on.epicgames.com`) | websocket control channel + WebRTC media ([RTC Signaling](../Voice/RTCSignaling.md)) |
| Launcher (`eglv2_lib::social`, `eglv2_lib::eos`) | WebView2 host via `EOS_ExternalOverlay`, SDK login, `voice-settings.json`, tray icon, taskbar badge, chimes, party-leave analytics |
| SOCS `api.epicgames.dev/epic/socs` | persisted voice settings ([README](../../EpicGames/SOCSService/README.md)) |
| Compass / Emerald | voice reports ([Moderation](../Voice/Moderation.md)) |

## Flow

1. Launcher signs the SDK in: exchange code -> `EOS_Auth_Login`, EG1 token pushed with `EOS_Auth_SetAccessTokenOverride`. The SDK announces the overlay URL and its bridge scripts; the launcher loads the overlay in the `social` WebView2 and exposes host object `eosBridge`. See [Native Bridge](../Voice/NativeBridge.md).
2. Overlay connects to Epic Connect and receives `core.connect.v1.connected` `{ connectionId }`. This id (`epicConnectId`) is the party connection id and the voice device id.
3. Overlay loads party state: [Get Parties Summary](../../EpicGames/PartyService/Users/GetUserSummary.md). Voice settings: [Query User Settings](../../EpicGames/SOCSService/Settings/QueryUserSettings.md) -> `update-voice-settings` to the SDK.
4. Party created or joined:
   - create: [Create Party](../../EpicGames/PartyService/Parties/CreateParty.md) `{ config: { joinability, max_size: 16 }, meta: { created_by }, join_info: { connection: { id: epicConnectId, deployment_id, meta: { osName, platformName, productName } } } }`
   - join: [Join Party](../../EpicGames/PartyService/Members/JoinParty.md) / [Join Group Party](../../EpicGames/PartyService/Groups/JoinGroupParty.md) then [Get Party](../../EpicGames/PartyService/Parties/GetParty.md)
   - invites / requests: [Send Party Invite](../../EpicGames/PartyService/Invites/SendInvite.md), [Send Join Request](../../EpicGames/PartyService/JoinRequests/SendJoinRequest.md)
5. Voice claim (`CheckActiveVoiceClaims`). One device per account holds voice, recorded in member meta `active_voice_connection` / `platform_name` / `product_name`:
   - meta points to a live first-party connection -> that device holds voice (`current-active-device`), nothing to do;
   - `product_name` is another product -> do not claim;
   - meta points to a dead connection of the same os / platform / product, or a previous connection id of this client, or a forced reclaim -> claim;
   - otherwise claim only if this device's connection is the oldest live first-party connection.
   A second member joining a party with no voice holder triggers `refresh-active-party-voice-check` (Get Party + claim check).
6. Eligibility gate must be `yes` (age verification, cabined mode, parental limit, social ban, reporting disclosure, voice setting; see [Settings](../Voice/Settings.md#voice-eligibility-gate)).
7. Overlay intent `connect-party-voice-room` `{ partyId, currentMemberRevision, epicConnectId, osName, productName, voiceBlockedIds }`:
   1. [Get Voice Room Connection](../../EpicGames/PartyService/Conferences/ConnectVoiceRoom.md) -> `providers.rtcp { participant_token, room_name, client_base_url }`.
   2. To the SDK (feature `party`): `set-blocked-participants` `{ participants: [{ id }] }`, then `connect-voice-room` `{ participantToken, roomName, clientBaseUrl, roomSettings: { AudioInputDeviceMode: "AlwaysOn" } }`.
   3. [Update Member Meta](../../EpicGames/PartyService/Members/UpdateMemberMeta.md) claims voice: `update { active_voice_connection, platform_name, product_name }`, `connection { id, deployment_id, active_in_party_voice_room: true }`.
8. SDK joins the room: websocket to `client_base_url`, `join` -> `join_res`, ICE / DTLS, Opus over SRTP ([RTC Signaling](../Voice/RTCSignaling.md)). Status flows back as `voice-room.status` (`connecting` -> `connected`). On `connected` the overlay re-sends per-member volume / mute (`set-participant-audio`) and `update-voice-settings { inputMuted, audioEnabled }`.
9. In call: SDK publishes `voice-room.participants[] { id, muted, speaking, notListening, voiceChatOff }` and `pttActive`; overlay draws speaking rings and sends `voice-party-state-changed` to the launcher (tray / taskbar). Mute, deafen, PTT, device and volume changes are `update-voice-settings` intents ([Settings](../Voice/Settings.md)). Deafen also updates `active_in_party_voice_room` (1s debounce).
10. Token refresh: SDK state `request-session-info { roomName, requestUniqueIndex }` -> overlay calls Get Voice Room Connection again -> intent `update-session-info { participantToken, roomName, clientBaseUrl, requestUniqueIndex }`.
11. Membership upkeep: `party.v2.*` events over Epic Connect update the roster. If the local member becomes `suspended`, the overlay calls [Keep Alive](../../EpicGames/PartyService/Members/KeepAlive.md). Network loss disconnects voice locally.
12. Leave voice / party: `disconnect-party-voice-room` -> SDK `disconnect-voice-room` + Update Member Meta (`unset`, `active_in_party_voice_room: false`); leaving the party is [Leave Party](../../EpicGames/PartyService/Members/LeaveParty.md). Voice also drops when eligibility turns `no:*`, when another device claims voice, or when the party is left / disbanded.
13. Analytics: the SDK emits a party-leave row (`RoomName`, `DisconnectReason`, RTT / loss / jitter, `VoiceChatOutgoingActivitySec`, `VoiceChatIncomingActivitySec`, `VoiceModerationEnabled*`) via `EOS_PartyFeature_AddNotifyLeaveAnalytics`; the launcher correlates it with the Epic Connect member-exit event (`telemetry::party_leave`, held / flushed rows).
14. Reporting (optional): `query-recorded-participants` -> `submit-voice-report` (SDK uploads to Emerald) -> Compass report. See [Moderation](../Voice/Moderation.md).

## States and events

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
