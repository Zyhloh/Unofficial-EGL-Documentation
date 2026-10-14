## KWS - Settings: Update Setting Values

Set preferred values. The communication settings panel sends the chat settings (`text`, `voice`, `enhanced-text-reporting`, `enhanced-voice-reporting`, `filter-out-mature-language`, `filter-out-pii`); party privacy sends `party.party-joinability` (`Public` / `Private`). The voice "Reporting on / off" toggle is `chat.enhanced-voice-reporting` ([Moderation](../../../Launcher/Voice/Moderation.md#reporting-preference)).

URL: https://api.kws.ol.epicgames.com/v1/epic-settings/public/users/:accountId/values \
Method: PATCH \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: Your account id <br/>

## Body
Voice reporting off:
```json
{
  "game": "fn",
  "settings": [
    { "namespace": "chat", "settingName": "enhanced-voice-reporting", "preferredValue": "prefer-not-recording" }
  ]
}
```

Other settings use the same shape, several entries per call allowed:
```json
{
  "game": "fn",
  "settings": [
    { "namespace": "chat", "settingName": "text", "preferredValue": "friends" },
    { "namespace": "party", "settingName": "party-joinability", "preferredValue": "Public" }
  ]
}
```

`enhanced-voice-reporting` values: `recording` (label "Always On"), `prefer-not-recording` ("Off When Possible"). General (non game) updates send `productId` instead of `game`. A parent limit can make `effectiveValue` differ from the preference.

---

_Example Response_

```json
{
  "response": {
    "settings": [
      {
        "namespace": "chat",
        "settingName": "enhanced-voice-reporting",
        "effectiveValue": "prefer-not-recording",
        "effectiveSource": "preference",
        "pendingConsent": false
      }
    ]
  },
  "meta": {
    "requestId": "d33bd07d-d135-498b-9d84-5e4ea7f6df5d",
    "timestamp": "2026-10-14T17:37:33.294Z"
  }
}
```

Realtime: `k3s.v1.EFFECTIVE_VALUES_CHANGED` over [Epic Connect](../../../Launcher/Social/Connect.md) (from the client code; not seen in the captures).
