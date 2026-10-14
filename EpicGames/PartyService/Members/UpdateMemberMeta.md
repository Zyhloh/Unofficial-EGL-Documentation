## Party Service - Members: Update Member Meta (Active Voice Connection)

Claims or releases the party voice room for one device (`set-active-voice-connection`). Sent right after `connect-party-voice-room`, with `disconnect-party-voice-room`, and 1s-debounced on deafen / undeafen. On `409` / `errors.com.epicgames.social.party.stale_revision` the client re-reads the party and retries once with the member's current `revision`.

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId/meta \
Method: PATCH \
Auth Required: Yes (Bearer elevated EG1 access token, from `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: The signed-in account id <br/>

## Body
```json
{
  "revision": 2,
  "update": {
    "active_voice_connection": "b1e2c3d4a5f60718293a4b5c6d7e8f90",
    "platform_name": "Windows",
    "product_name": "Epic Games Launcher"
  },
  "connection": {
    "id": "b1e2c3d4a5f60718293a4b5c6d7e8f90",
    "deployment_id": "d0e1f2a3b4c5d6e7f8091a2b3c4d5e6f",
    "active_in_party_voice_room": true
  }
}
```

Release (`intent: "unset"`) sends only `revision` and `connection` with `active_in_party_voice_room: false`. When claiming, `active_in_party_voice_room` is `!deafened`; `platform_name` is the client's `osName`.

Other devices of the same account read `active_voice_connection` to decide who owns voice (`should-claim-active-voice-device`, `current-active-device`). See [Voice Chat](../../../Launcher/Flows/VoiceChat.md).
