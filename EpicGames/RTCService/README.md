# Hosts

This are some (not all) Hosts that you can access the RTC Service from

- api.epicgames.dev (`/rtc`, inferred: the SDK only names the service `RTC` and resolves its base URL at runtime)

<br/>

Recommended Hosts:

- api.epicgames.dev

EOS SDK `1.19.4230.0-57929184@LauncherV2` (shipped as `EOSSDK-Win64-Shipping.dll`) holds three routes under service name `RTC`. They back `EOS_RTCAdmin_*` (trusted server / client-credentials API). The launcher does not call them: party voice credentials come from the Party Service ([Get Voice Room Connection](../PartyService/Conferences/ConnectVoiceRoom.md)).

| Operation | Method | Path | Page |
| --- | --- | --- | --- |
| `JoinRoom` | POST | `/v1/:deploymentId/room/:roomId` | [Query Join Room Token](Room/QueryJoinRoomToken.md) |
| `ModifyParticipant` | POST | `/v1/:deploymentId/room/:roomId/participants/:puid` | [Set Hard Mute](Room/SetParticipantHardMute.md) |
| `RemoveParticipant` | DELETE | `/v1/:deploymentId/room/:roomId/participants/:puid` | [Kick Participant](Room/KickParticipant.md) |

The voice media itself does not go over REST. The SDK opens a websocket control channel to the room's `client_base_url` and runs WebRTC; see [RTC Signaling](../../Launcher/Voice/RTCSignaling.md).
