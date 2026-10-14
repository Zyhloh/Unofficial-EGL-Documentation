## Presence Service - Presence: Last Online

Last-online time of friends, used for friend list sorting.

URL: https://api.epicgames.dev/epic/presence/internal/v1/:namespace/:accountId/last-online \
Method: GET \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>
`accountId`: Your account id <br/>

## Query Parameters
`circle`: `friends` <br/>

---

_Example Response (shape from client)_

```json
{
  "b9cd1f0b1b1a4fd7a2f1d1e4c3b2a190": [ { "last_online": "2026-10-14T00:00:00.000Z" } ]
}
```
