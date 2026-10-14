# Voice - RTC Signaling And Media

What the EOS SDK does on the wire once the overlay hands it `participantToken` / `roomName` / `clientBaseUrl`. Everything here comes from `EOSSDK-Win64-Shipping.dll` `1.19.4230.0-57929184@LauncherV2` (IDA, `LibRtc::*` and `Epic::OnlineServices::FRTC*`). No traffic was captured; field names are exact, values and ordering of a live session are not.

## Stack

| Layer | Implementation |
| --- | --- |
| Room API | `FRTCRoom` / `RTCRoomHelper`, source `PartiesInternalApi` (other sources: `RtcApi`, `LobbyApi`, `PartiesApi`) |
| Client library | `LibRtc` (Epic, "RTCP"): `FConferenceService`, `FConnectionService`, `FMediaServiceClient`, `FRtcpConnection` |
| Control channel | websocket (`FLwsWebSocket`, libwebsockets) to the media server, JSON messages with a `type` field |
| Media | libwebrtc (`ThirdParty\WebRTC\7204`), one `PeerConnection` per room, Opus `opus/48000/2`, DTLS-SRTP, RTP/RTCP mux, SCTP data channel |
| Audio I/O | XAudio2 (render) and RtAudio (capture) through `FRTCAudio`, WebRTC APM (AEC3 / NS / AGC1 or AGC2) |

## Connect

1. `PartyFeature::HandleConnectVoiceRoomIntent` receives `connect-voice-room` `{ participantToken, roomName, clientBaseUrl, roomSettings }`. One room per local user; a second room is refused (`Connection to multiple rooms is not supported`).
2. `FRTCRoom::Join` stores `clientBaseUrl` as the requested media server URL (`MsUrlRequested`). `RTCSessionResolver` can map it to a different URL after a `transfer` (`MsUrlActual`, `UrlAndTokenReplaced`).
3. The SDK parses the URL for analytics: a host containing `rtcp.on.epicgames.com` yields `RegionName`, a path segment starting `signaling-service-` yields `SignalingServiceType`. This is the only hint of the URL shape in the binary (`client_base_url` itself is opaque, needs a capture).
4. LibRtc opens the control websocket (`[MediaService] Control channel connected`) and sends `join`.
5. The server answers `join_res`. The client builds the remote SDP itself from it (inferred from the SDP template strings next to the `join_res` parser; no SDP field exists in any control message): `a=ice-lite`, `a=ice-ufrag` / `a=ice-pwd` from `ice`, `a=fingerprint` from `fingerprint`, one `a=candidate` per address from `ipv4` / `ipv6` with `udp_port`, `tcp_port`, `ssltcp_port`, Opus fmtp with `maxaveragebitrate`, `ptime`, `useinbandfec=1`. TURN entries (`turn:` / `turns:`) and the default STUN `stun:stun.l.google.com:19302` come from `ice.servers` / config.
6. ICE + DTLS complete; `OnConferenceSignalingConnectionEstablished`, room status becomes connected and the SDK publishes the `voice-room` state to the overlay.
7. Keep-alive on the control channel: `[MediaService] Start ping with interval %f`, `Ping Sent` / `Pong received`; a missed pong ends the session with `BrokenPingPong` and triggers reconnect (`ReconnectionAttemptsStarted`, bounded by attempt count and timeout).

## Control messages

Client to server (type table at `0x18222FCF0`):

| `type` | Fields |
| --- | --- |
| `join` | `ticket`, `user_token`, `options` (array: `dtx`, `ras_csrc`, `speaking_self_only`, `reserved_audio_streams`, ...), `version`, `device { os, model, manufacturer, online_platform_type }`, `status { is_muted, audio_muted_reason, is_audio_only, reason_enum, is_screencast }`, `connection_id`, `data_streams [{ ordered, protocol, type, id }]`, `video { width, height, codecs }`, `reserved_audio_streams_max_pool_size`, `test { force_proximity_radius }`, `voice_moderation { signed_public_key, ... mode }` |
| `join_update` | `fingerprint` |
| `mute_audio` | `is_muted`, `user_token`, `reason_enum` |
| `audio_only` | `is_audio_only`, `user_token`, `reason_enum` |
| `subscribe` | `sender_token`, `audio`, `data`, `video`, `message_id` |
| `video_resolution` | `user_token`, `sender_token`, `resolution`, `framerate` |
| `position` | `position` (proximity rooms) |
| `user_left` | `user_token` |

Server to client:

| `type` | Fields |
| --- | --- |
| `join_res` | `user_token`, `ssrc`, `video`, `data_streams`, `udp_port`, `ssltcp_port`, `tcp_port`, `status` (`LibRtc::FJoinResMessage::STATUS_TYPE`), `maxaveragebitrate`, `ptime`, `video_max_bitrate_p2p`, `options`, `ice { servers, ufrag, pwd }`, `fingerprint`, `users`, `ipv4`, `ipv6`, `power_mode`, `abort_on_inactivity`, `reserved_audio_streams { ssrc }`, `proximity { radius }` |
| `user_joined` | `ssrc`, `status`, `metadata`, `user_token`, `voice_moderation` |
| `user_left` | `user_token` |
| `mute_audio` | `is_muted`, `user_token`, `reason_enum` |
| `remote_mute_audio` | `is_muted` (server-side hard mute of the local user) |
| `speaking` | `user_token`, `is_speaking` |
| `audio_only` | `is_audio_only`, `user_token`, `reason_enum` |
| `screencast` | `is_screencast`, `user_token` |
| `kick_user` | `reason` |
| `transfer` | `url`, `ticket` (media server migration: the client joins `url` with the new `ticket`, then leaves the old conference) |
| `network_status` | |
| `control_secondary` | `enabled`, `audio_sending_enabled` |
| `subscribe_res` | `status` (`LibRtc::ESubscribeResStatus`), `message_id` |
| `audio_streams_mapping` | `mapping` |

`ticket` and `user_token`: `transfer` replaces the room URL together with a new `ticket`, which matches the `clientBaseUrl` + `participantToken` pair, so `ticket` is the participant token and `user_token` the participant id (inferred from that pairing, not from a capture).

Server-side reject reasons (`LibRtc` result strings): `CredentialAccessDenied`, `RoomNotFound`, `RoomFull`, `TokenBanned`, `ServerUnsupportedApiVersion`, `ServerGenericError`, `RoomOptionsMismatch`, `VoiceModerationModeMismatch`, `PublicKeyValidationFailed`, `DuplicateSession` ("same user connected from elsewhere"), `KickedFromConference`, `ServerTermination`, `ServerUnavailable`.

## Mute, deafen, participant state

- Local mute / deafen arrive as `update-voice-settings` (`inputMuted`, `audioEnabled`). The SDK maps them to `EOS_RTCAS_Enabled` / `EOS_RTCAS_Disabled` / `EOS_RTCAS_NotListeningDisabled` for sending (`PartyFeature::HandleUpdateSending`) and toggles receiving (`UpdateAudioReceiving`). "Mic-on + deafen is not representable on the wire; peers see NotListeningDisabled." On the wire this is `mute_audio` with `is_muted` + `reason_enum`.
- Per-participant volume / local mute: `set-participant-audio` `{ id, volume }` or `{ id, muted }` -> `UpdateParticipantVolume` / `UpdateReceiving` (local only).
- Blocking: `set-blocked-participants` `{ participants: [{ id }] }` replaces the blocked set; blocked users are unsubscribed (`FRTCRoom::BlockParticipant`).
- Remote changes (`user_joined`, `user_left`, `mute_audio`, `speaking`) update `FVoiceRoomState`, published to the overlay as `voice-room.participants[]` `{ id, muted, speaking, notListening, voiceChatOff }`.
- Audio priority list goes over the SCTP data channel (`Audio priority list has been sent`).

## Leave

`disconnect-voice-room` -> `PartyFeature::DisconnectPartyConference` -> `LeaveConference`, websocket closed (`[MediaService] Closing websocket ...`). On teardown the SDK emits audio output `Idle` and a `party-leave-analytics` row (`AccountId`, `RoomName`, `DisconnectReason`, `AvgRoundTripTimeSec`, `IncomingAvgPacketLossFraction`, `OutgoingAvgPacketLossFraction`, `AvgJitterBufferDelaySec`, `VoiceModerationEnabled`, `VoiceModerationEnabledDurationSec`, `VoiceChatOutgoingActivitySec`, `VoiceChatIncomingActivitySec`) built from WebRTC stats (`inbound-rtp`, `outbound-rtp`, `remote-inbound-rtp`, `candidate-pair`). The launcher subscribes with `EOS_PartyFeature_AddNotifyLeaveAnalytics`.

## Token refresh

When the SDK needs new credentials (reconnect after expiry) it sets state `request-session-info` `{ roomName, requestUniqueIndex }` (`PartyFeature::OnSessionInfoRequest`, timeout `SessionInfoRequestTimeoutSeconds`). The overlay calls the Party Service again and answers with intent `update-session-info` `{ participantToken, roomName, clientBaseUrl, requestUniqueIndex }`.

## Voice moderation (signed audio)

With voice reporting enabled the room joins with `voice_moderation` (`signed_public_key`), audio frames are signed (`RegisterAudioOutgoingSigningAlgorithm`, `UpdateModerationSendingSignature`) and a rolling local recording (`FRTCAudioLogicRecord`) is kept for reports. Upload path: [Reporting](Moderation.md).
