## Avatar Service - Avatars: Settings

The signed-in account's own avatar.

URL: https://api.epicgames.dev/epic/avatar/v1/:deploymentId/accounts/:accountId/settings \
Method: GET \
Auth Required: Yes (Bearer EG1 access token)

## Headers
`X-Epic-Agent`: `epic-social` <br/>

## Path Parameters
`deploymentId`: Avatars deployment, `9c9906b240c74a92a6b9100d6e4ccbd0` <br/>
`accountId`: Your account id. Another account's id returns 403

---

_Example Response_

```json
{
  "avatar": {
    "avatarId": "AthenaCharacter:cid_defaultoutfit[2,6]",
    "url": "https://cosmo.fdeb.live.use1a.on.epicgames.com/cdn-cgi/image/height={},format=png/v1/item/HNbvcohOxY4TnWtpDLdeUInh7V_DipmSPvrhzLo6A6I/png"
  },
  "sync": true
}
```

`avatarId` is a Fortnite cosmetic id. Replace `{}` in `url` with a height in pixels.

_Example Response (another account)_

```json
{
  "errorCode": "403",
  "errorMessage": "Authorization failed",
  "intent": "prod",
  "messageVars": [],
  "numericErrorCode": -1,
  "originatingService": "avatar-service-v2-api"
}
```
