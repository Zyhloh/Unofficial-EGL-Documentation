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

_Example Response (shortened)_

```json
{
  "b9cd1f0b1b1a4fd7a2f1d1e4c3b2a190": [ { "last_online": "2026-11-12T15:29:54.030Z" } ],
  "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60": [ { "last_online": "2026-11-13T20:50:29.210Z" } ]
}
```

One key per friend (18 for 18 friends on the test account), each holding a one-element array.
