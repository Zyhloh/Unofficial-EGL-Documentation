## Library Service - Playtime: Get All

Total playtime per artifact for the account. Backs `get_playtime` (cached in `playtime-cache.json`, refreshed in the background).

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/playtime/account/:accountId/all \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`accountId`: The account id

---

_Example Response_

Shortened to two entries.

```json
[
  {
    "accountId": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
    "artifactId": "Grunt",
    "totalTime": 1378
  },
  {
    "accountId": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
    "artifactId": "Daisy",
    "totalTime": 2786
  }
]
```

Bare array, one entry per artifact ever played. `artifactId` is the app name (`appName` of the library record; some app names are 32-hex ids). `totalTime` is in seconds.
