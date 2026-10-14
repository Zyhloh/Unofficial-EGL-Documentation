## RTC Service - Room: Query Join Room Token

Creates (or reuses) a voice room and issues participant tokens. SDK operation `JoinRoom`, behind `EOS_RTCAdmin_QueryJoinRoomToken`. Not used by the launcher or by party voice: party voice credentials come from the Party Service ([Get Voice Room Connection](../../PartyService/Conferences/ConnectVoiceRoom.md)).

URL: https://api.epicgames.dev/rtc/v1/:deploymentId/room/:roomId \
Method: POST \
Auth Required: Yes (Bearer EOS client access token, inferred)

## Headers
`Content-Type`: application/json <br/>

## Path Parameters
`deploymentId`: EOS deployment id <br/>
`roomId`: Room name (`{conferenceId}` in the SDK route template) <br/>

## Body
```json
{
  "participants": [
    {
      "puid": "0002a1b2c3d4e5f60718293a4b5c6d7e",
      "clientIp": "203.0.113.10",
      "hardMuted": false
    }
  ]
}
```

---

_Example Response (shape from client; fields from the SDK deserializer)_

```json
{
  "roomId": "...",
  "deploymentId": "d0e1f2a3b4c5d6e7f8091a2b3c4d5e6f",
  "clientBaseUrl": "wss://...",
  "participants": [
    {
      "puid": "0002a1b2c3d4e5f60718293a4b5c6d7e",
      "token": "...",
      "clientIp": "203.0.113.10",
      "hardMuted": false
    }
  ]
}
```

The SDK logs `Unexpected room id received from the backend. Requested %s, received %s` when `roomId` differs from the path. `clientBaseUrl` + `token` are what `EOS_RTC_JoinRoom` takes as `ClientBaseUrl` / `ParticipantToken`.
