## KWS - Settings: Update Setting Values

Set preferred values. The communication settings panel sends the six chat settings; party privacy sends `party.party-joinability` (`Public` / `Private`).

URL: https://api.kws.ol.epicgames.com/v1/epic-settings/public/users/:accountId/values \
Method: PATCH \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: Your account id <br/>

## Body
```json
{
  "game": "fn",
  "settings": [
    { "namespace": "chat", "settingName": "text", "preferredValue": "friends" },
    { "namespace": "party", "settingName": "party-joinability", "preferredValue": "Public" }
  ]
}
```

General (non game) updates send `productId` instead of `game`.

---

_Example Response (shape from client)_

```json
{
  "response": { "settings": [ { "namespace": "party", "settingName": "party-joinability", "effectiveValue": "Public" } ] },
  "meta": { "timestamp": "2026-10-14T00:00:00.000Z" }
}
```
