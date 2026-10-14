## Social Ban Service - Bans: Get User Summary

Fetched once the account is known (intent `get-user-ban-status`). If the newest ban is not acked the client immediately acks it.

URL: https://social-ban-public-service-prod.social.live.on.epicgames.com/socialban/api/public/v1/:accountId \
Method: GET \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: Your account id <br/>

---

_Example Response (shape from client)_

```json
{
  "bans": [
    {
      "starts_at": "2026-10-14T00:00:00.000Z",
      "ends_at": "2026-10-15T00:00:00.000Z",
      "duration_s": 86400,
      "name": { "features": ["..."] },
      "acked": false
    }
  ],
  "warnings": []
}
```
