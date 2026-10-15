## Library Service - Playtime: Get Artifact

Total playtime of one game for an account.

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/playtime/account/:accountId/artifact/:artifactId \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`accountId`: The account id <br/>
`artifactId`: App name of the game, e.g. `Daisy`

---

_Example Response_

```json
{
  "accountId": "94b1569506b04f9f8557af611e8c5e47",
  "artifactId": "Daisy",
  "totalTime": 2906
}
```

`totalTime` is in seconds. Intervals sent with [Publish Bulk](PublishBulk.md) are added to it right away.
