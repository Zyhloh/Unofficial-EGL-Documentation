## Presence Service - Presence: Update Presence

Overlay presence publish. Sent on Epic Connect connect, on status / party changes, and as a heartbeat every 15-30 min (random). Identical payloads on the same connection are throttled for 60s. Skipped while Epic Connect is down. The manual status picker sends `statusSettings` and no `party`.

Required for party voice: a client that never publishes presence shows as Offline to friends and EGL hides its party invites. Publish right after the Epic Connect connection exists and again after creating the party.

URL: https://api.epicgames.dev/epic/presence/internal/v1/:namespace/:accountId/presence/:connectionId \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>
`X-HTTP-Method-Override`: PATCH <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>
`accountId`: Your account id <br/>
`connectionId`: Epic Connect `connectionId` (STOMP `CONNECTED` `session` header) <br/>

## Body
Body a standalone client sent after creating its party (accepted; friends saw it online and EGL showed the invite):
```json
{
  "status": "online",
  "party": {
    "id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "type": "INVITE_ONLY",
    "timestamp": "2026-10-14T16:53:45.111Z",
    "memberCount": 1,
    "clientJoinable": true
  },
  "conn": { "props": {} }
}
```

Overlay body with the manual status picker (from the client code):
```json
{
  "status": "away",
  "statusSettings": { "mode": "manual_set" },
  "conn": { "props": {} }
}
```

`status`: `online` / `away` (manual picker may also send other values). `statusSettings.mode`: `manual_set`, or `manual_unset` when going back to `online`. `party` omitted when parties are disabled; without an active party it carries only the default joinability (`type`, `timestamp`, `clientJoinable`). `party.type` is the party `joinability`, `timestamp` the party `created_at`.

---

_Example Response_ (to the party body above; only `own` is read)

```json
{
  "own": {
    "accountId": "94b1569506b04f9f8557af611e8c5e47",
    "status": "online",
    "perNs": [
      {
        "status": "online",
        "party": {
          "joinable": false,
          "invitable": true
        },
        "ns": "_",
        "conns": [
          {
            "id": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
            "props": {}
          }
        ]
      }
    ]
  }
}
```

The server reduces `party` to `joinable` / `invitable`; the party `id` and `memberCount` are not echoed. The same response came back for a body without a party (`party { type, timestamp, clientJoinable }` only).

Friends receive the result as `presence.v1.UPDATE` over Epic Connect ([Connect](../../../Launcher/Social/Connect.md#presencev1update-payload)).
