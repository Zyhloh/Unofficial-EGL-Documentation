## KWS - Settings: Get Setting Values

Parental controls / age-bracket settings (internally `K3S`). Two calls on start: general (`namespace=profile,chat,communications`, `settingName=require-pin-to-add-friend,curtain-tower,voice,enhanced-voice-reporting`, `productId` only for two allow-listed product ids) and Fortnite (`game=fn`, `namespace=chat,party`, `settingName=text,enhanced-text-reporting,filter-out-mature-language,filter-out-pii,party-joinability,voice,enhanced-voice-reporting`). Retried up to 8 times.

URL: https://api.kws.ol.epicgames.com/v1/epic-settings/public/users/:accountId/values \
Method: GET \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: Your account id <br/>

## Query Parameters
`namespace`: Comma separated namespaces <br/>
`settingName`: Comma separated setting names <br/>
`game`: `fn` for Fortnite scoped values <br/>
`productId`: Optional, only `e6bcca5b37d0457ca881aec508205542` or `d42d7101bb7a41c09a810ee418b7d3d0` <br/>

Chat audience values ordered: `nobody`, `friends`, `friends-and-teammates`, `friends-team-connections`, `everybody`. Reporting values: `recording`, `prefer-not-recording`. `denyReason` values: `limitEnforced`, `verificationRequired`. `party-joinability`: `Public` maps to party `OPEN`, anything else `INVITE_ONLY`.

---

_Example Response (shape from client)_

```json
{
  "response": {
    "settings": [
      {
        "namespace": "chat",
        "settingName": "text",
        "effectiveValue": "friends",
        "parentLimit": "friends",
        "allowed": false,
        "denyReason": "verificationRequired",
        "remediation": [ { "remediationMethod": "AGE_VERIFICATION", "remediationUrl": "https://..." } ],
        "definition": { "ageBracket": { "enforcedLimit": "friends" } }
      },
      {
        "namespace": "communications",
        "settingName": "curtain-tower",
        "effectiveValueSchedule": {},
        "scheduleCalculatedFromTimeZone": "Europe/London"
      }
    ]
  },
  "meta": { "timestamp": "2026-10-14T00:00:00.000Z" }
}
```
