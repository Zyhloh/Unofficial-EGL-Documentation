## Party Service - Members: Update Member Meta (Active Voice Connection)

Claims or releases the party voice room for one device (`set-active-voice-connection`). Sent right after `connect-party-voice-room`, with `disconnect-party-voice-room`, and 1s-debounced on deafen / undeafen. One device per account holds voice. On `409` / `errors.com.epicgames.social.party.stale_revision` the client re-reads the party and retries once with the member's current `revision`.

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId/meta \
Method: PATCH \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: The signed-in account id <br/>

## Body
Claim:
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

Second captured PATCH (same session, 12s later, sent by EGL with the same `update`):
```json
{
  "revision": 1,
  "update": {
    "active_voice_connection": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
    "platform_name": "Windows",
    "product_name": "Epic Games Launcher"
  },
  "connection": {
    "id": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
    "deployment_id": "_",
    "active_in_party_voice_room": false
  }
}
```

`revision` is the member's current revision (`0` right after [Create Party](../Parties/CreateParty.md), then the value from the previous response). `active_voice_connection` and `connection.id` are the Epic Connect connection id; `platform_name` is the client's `osName`. When claiming, `active_in_party_voice_room` is `!deafened`. Release (`intent: "unset"` in the overlay) sends `active_in_party_voice_room: false`; the overlay build sends only `revision` and `connection` there (from the client code), a standalone client that resends `update` with `false` also works. Set `false` when leaving voice.

Observed from EGL in a 2-member party (2026-10-14): mic mute and unmute each produced a PATCH too (member `revision` +1, `active_in_party_voice_room` stays `true`, `party.v2.MEMBER_STATE_UPDATED` with the same `update` keys); deafen sent `active_in_party_voice_room: false`, undeafen `true`. The connection flag drives the party's [`is_reportable`](../../../Launcher/Voice/Moderation.md#is_reportable): deafen flipped it to `false`, undeafen back to `true` (`party.v2.PARTY_UPDATED` within ~25ms of the member event).

Other devices of the same account read `active_voice_connection` to decide who owns voice (`should-claim-active-voice-device`, `current-active-device`). See [Voice Chat](../../../Launcher/Flows/VoiceChat.md). Other members receive `party.v2.MEMBER_STATE_UPDATED` with `member_state_updated` = the changed keys.

---

_Example Response_

```json
{
  "account_id": "94b1569506b04f9f8557af611e8c5e47",
  "meta": {
    "platform_name": "Windows",
    "product_name": "Epic Games Launcher",
    "active_voice_connection": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d"
  },
  "revision": 1,
  "updated_at": "2026-10-14T16:53:45.378Z",
  "joined_at": "2026-10-14T16:53:45.116Z",
  "suspended": false,
  "connection": {
    "id": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
    "deployment_id": "_",
    "connected_at": "2026-10-14T16:53:45.116Z",
    "updated_at": "2026-10-14T16:53:45.378Z",
    "is_first_party": true,
    "meta": {
      "osName": "Windows",
      "platformName": "egs",
      "productName": "Epic Games Launcher"
    },
    "active_in_party_voice_room": true
  }
}
```
