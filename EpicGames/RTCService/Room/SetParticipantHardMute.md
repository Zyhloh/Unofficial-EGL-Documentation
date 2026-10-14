## RTC Service - Room: Set Participant Hard Mute

SDK operation `ModifyParticipant`, behind `EOS_RTCAdmin_SetParticipantHardMute`. Not used by the launcher or by party voice: party voice credentials come from the Party Service ([Get Voice Room Connection](../../PartyService/Conferences/ConnectVoiceRoom.md)).

URL: https://api.epicgames.dev/rtc/v1/:deploymentId/room/:roomId/participants/:puid \
Method: POST \
Auth Required: Yes (Bearer EOS client access token, inferred)

## Headers
`Content-Type`: application/json <br/>

## Path Parameters
`deploymentId`: EOS deployment id <br/>
`roomId`: Room name <br/>
`puid`: Product user id of the participant <br/>

## Body
```json
{
  "hardMuted": true
}
```
