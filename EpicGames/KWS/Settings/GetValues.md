## KWS - Settings: Get Setting Values

Parental controls / age-bracket settings (internally `K3S`). Two calls on start: general (`namespace=profile,chat,communications`, `settingName=require-pin-to-add-friend,curtain-tower,voice,enhanced-voice-reporting`, `productId` only for two allow-listed product ids) and Fortnite (`game=fn`, `namespace=chat,party`, `settingName=text,enhanced-text-reporting,filter-out-mature-language,filter-out-pii,party-joinability,voice,enhanced-voice-reporting`). Retried up to 8 times. The effective `enhanced-voice-reporting` value feeds the voice reporting label ([Moderation](../../../Launcher/Voice/Moderation.md#reporting-preference)).

URL: https://api.kws.ol.epicgames.com/v1/epic-settings/public/users/:accountId/values \
Method: GET \
Auth Required: Yes (Bearer EG1 access token, any client)

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

_Example Response (`chat` / `enhanced-voice-reporting`)_

```json
{
  "response": {
    "settings": [
      {
        "namespace": "chat",
        "settingName": "enhanced-voice-reporting",
        "preferredValue": "recording",
        "preferredValueUpdatedAt": 1791999453588,
        "preferredValueFromOrgLevel": false,
        "effectiveValue": "recording",
        "effectiveSource": "preference",
        "effectiveValueUpdatedAt": 1791999453588,
        "isOrgLevel": false,
        "definition": {
          "orgId": "00000000-1111-4222-8333-444444444444",
          "productId": "55555555-6666-4777-8888-999999999999",
          "namespace": "chat",
          "settingName": "enhanced-voice-reporting",
          "valueType": "option",
          "allowProductOverrides": "ageBrackets",
          "inheritFromOrg": true,
          "translations": {
            "en": {
              "label": "Enhanced voice chat recording",
              "parentNotice": "Determines enhanced voice chat recording setting"
            }
          },
          "options": [
            { "value": "recording", "translations": { "en": { "label": "Always On" } } },
            { "value": "prefer-not-recording", "translations": { "en": { "label": "Off When Possible" } } }
          ],
          "restrictiveOrder": "firstRestrictive",
          "userHidden": false,
          "required": false,
          "dataStorage": "raw",
          "maximumScheduleWindowsPerDay": 0,
          "ageBracket": {
            "consentTypeRequired": "none",
            "consentType": "none",
            "applyConsentToEnforcedUsersOnly": false,
            "defaultValue": "prefer-not-recording",
            "defaultPreference": "prefer-not-recording"
          }
        }
      }
    ]
  },
  "meta": {
    "requestId": "1e08232a-ceb3-43b3-9500-60b0b986d73d",
    "timestamp": "2026-10-14T17:37:33.704Z"
  }
}
```

Fields the overlay reads on other settings (shape from client):

```json
{
  "namespace": "chat",
  "settingName": "text",
  "effectiveValue": "friends",
  "parentLimit": "friends",
  "allowed": false,
  "denyReason": "verificationRequired",
  "remediation": [ { "remediationMethod": "AGE_VERIFICATION", "remediationUrl": "https://..." } ],
  "definition": { "ageBracket": { "enforcedLimit": "friends" } }
}
```

`communications` / `curtain-tower` carries `effectiveValueSchedule` and `scheduleCalculatedFromTimeZone` instead of a plain value (shape from client).
