## Party Service - Conferences: Get Voice Room Connection

Issues the RTC credentials for the party voice room. Called by `connect-party-voice-room` and again by `update-session-info` whenever the EOS SDK asks for a fresh token (`request-session-info`). The overlay hands the `rtcp` block to the SDK as `connect-voice-room` / `update-session-info`; see [Voice Chat](../../../Launcher/Flows/VoiceChat.md). The launcher never uses the [RTC Service](../../RTCService/README.md) routes for party voice.

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId/conferences/connection \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: The signed-in account id (must be a member) <br/>

No body (`Content-Length: 0`).

---

_Example Response_

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

| Field | Notes |
| --- | --- |
| `room_name` | `pv2-<partyId>`. Also the context string of [audio signing](../../../Launcher/Voice/AudioSigning.md) |
| `client_base_url` | signaling websocket. `<region>` seen: `use2`. Query: `ms` = media server (private IP, port `8443`, path = token `guid`), `p` = namespace `epicparty`, `t` = `base64url("<media ip>|<n>")` + `.` + signature. Use the URL as-is |
| `participant_token` | EdDSA JWT, 2h lifetime. Sent as `ticket` in the signaling `join` ([RTC Signaling](../../../Launcher/Voice/RTCSignaling.md#join)) |

`participant_token` decoded:

```json
{
  "typ": "JWT",
  "alg": "EdDSA"
}
```

```json
{
  "sub": "CONNECT",
  "targetHost": "10.0.12.34",
  "clientId": "94b1569506b04f9f8557af611e8c5e47",
  "conferenceId": "pv2-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
  "iss": "rtcp-manager",
  "namespace": "epicparty",
  "guid": "6c1e2f3a-4b5d-4e6f-8a9b-0c1d2e3f4a5b",
  "exp": 1792004025,
  "iat": 1791996825,
  "eosProperties": {
    "organizationId": "o-1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c",
    "productId": "epicparty",
    "deploymentId": "ae5c43ac915244a39923a08f103c5a02",
    "sandboxId": "epicparty"
  }
}
```

`targetHost` and `guid` match the `ms` part of `client_base_url`; `clientId` is the account id and becomes the participant's `user_token`.
