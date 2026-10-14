## RTC Service - Room: Kick Participant

SDK operation `RemoveParticipant`, behind `EOS_RTCAdmin_Kick`. Not used by the launcher or by party voice: party voice credentials come from the Party Service ([Get Voice Room Connection](../../PartyService/Conferences/ConnectVoiceRoom.md)). The kicked client receives a `kick_user` control message ([RTC Signaling](../../../Launcher/Voice/RTCSignaling.md)).

URL: https://api.epicgames.dev/rtc/v1/:deploymentId/room/:roomId/participants/:puid \
Method: DELETE \
Auth Required: Yes (Bearer EOS client access token, inferred)

## Path Parameters
`deploymentId`: EOS deployment id <br/>
`roomId`: Room name <br/>
`puid`: Product user id of the participant <br/>
