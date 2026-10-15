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
    "requestId": "7a1c3e5b-2d4f-4b6a-8c9e-1f3a5b7d9e2c",
    "timestamp": "2026-10-14T17:37:33.294Z"
  }
}
```

### Text reporting

`chat` / `enhanced-text-reporting` sets whether group chats you create are reportable ([Create Conversation](../../ChatService/Conversations/CreateConversation.md#isreportable)): `prefer-not-recording` -> new groups `isReportable: false` (EGL shows "Text reporting is off"), `recording` -> `true`.

```json
{
  "game": "fn",
  "settings": [
    { "namespace": "chat", "settingName": "enhanced-text-reporting", "preferredValue": "recording" }
  ]
}
```

_Example Response_

```json
{
  "response": {
    "settings": [
      {
        "namespace": "chat",
        "settingName": "enhanced-text-reporting",
        "effectiveValue": "recording",
        "effectiveSource": "preference",
        "pendingConsent": false
      }
    ]
  },
  "meta": {
    "requestId": "4f2b8d6a-9c1e-4a3b-8e7d-0c5f1a2b3d4e",
    "timestamp": "2026-10-14T22:53:54.696Z"
  }
}
```

Realtime: `k3s.v1.EFFECTIVE_VALUES_CHANGED` over [Epic Connect](../../../Launcher/Social/Connect.md) (from the client code; not seen in the captures).
