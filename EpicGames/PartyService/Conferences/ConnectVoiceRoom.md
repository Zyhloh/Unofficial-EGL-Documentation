## Party Service - Conferences: Get Voice Room Connection

Issues the RTC credentials for the party voice room. Called by `connect-party-voice-room` and again by `update-session-info` whenever the EOS SDK asks for a fresh token (`request-session-info`). The overlay hands the `rtcp` block to the SDK as `connect-voice-room` / `update-session-info`; see [Voice Chat](../../../Launcher/Flows/VoiceChat.md).

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId/conferences/connection \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token, from `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: The signed-in account id <br/>

No body.

---

_Example Response (shape from client; only `providers.rtcp.room_name`, `participant_token`, `client_base_url` are read. Values not captured)_

```json
{
  "providers": {
    "rtcp": {
      "room_name": "...",
      "participant_token": "...",
      "client_base_url": "wss://..."
    }
  }
}
```
