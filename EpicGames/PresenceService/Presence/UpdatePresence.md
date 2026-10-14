## Presence Service - Presence: Update Presence

Overlay presence publish. Sent on Epic Connect connect, on status / party changes, and as a heartbeat every 15-30 min (random). Identical payloads on the same connection are throttled for 60s. Skipped while Epic Connect is down. The manual status picker sends `statusSettings` and no `party`.

URL: https://api.epicgames.dev/epic/presence/internal/v1/:namespace/:accountId/presence/:connectionId \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>
`X-HTTP-Method-Override`: PATCH <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>
`accountId`: Your account id <br/>
`connectionId`: Epic Connect `connectionId` from `core.connect.v1.connected` <br/>

## Body
```json
{
  "status": "online",
  "statusSettings": { "mode": "manual_set" },
  "party": {
    "id": "...",
    "type": "OPEN",
    "timestamp": "2026-10-14T00:00:00.000Z",
    "memberCount": 2,
    "clientJoinable": true
  },
  "conn": { "props": {} }
}
```

`status`: `online` / `away` (manual picker may also send other values). `statusSettings.mode`: `manual_set`, or `manual_unset` when going back to `online`. `party` omitted when parties are disabled; without an active multi-member party it carries only the default joinability (`type`, `timestamp`, `clientJoinable`). The response field `own` is a presence object (same shape as `presence.v1.UPDATE`).

---

_Example Response (shape from client; only `own` is read)_

```json
{
  "own": {
    "accountId": "94b1569506b04f9f8557af611e8c5e47",
    "status": "online",
    "perNs": [
      { "ns": "_", "status": "online", "party": { "id": "...", "joinable": true, "invitable": true, "memberCount": 2 }, "conns": [] }
    ]
  }
}
```
