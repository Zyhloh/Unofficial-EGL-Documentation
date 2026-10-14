## Library Service - Playtime: Get All

Total playtime per artifact for the account. Backs `get_playtime` (cached in `playtime-cache.json`, refreshed in the background).

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/playtime/account/:accountId/all \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`accountId`: The account id

---

_Example Response (shape from client)_

```json
[
  {
    "accountId": "94b1569506b04f9f8557af611e8c5e47",
    "artifactId": "Fortnite",
    "totalTime": 123456
  }
]
```

`artifactId` is the app name (`AppId.appName`). `totalTime` unit is not visible in the client (seconds in the legacy launcher).
