## SOCS Service - Settings: Query User Settings

Loads the overlay settings once the account id and `osName` are known (`fetch-initial-socs-settings`). The result becomes the `socs-settings` value that the overlay then pushes to the EOS SDK as `update-voice-settings`.

URL: https://api.epicgames.dev/epic/socs/v1/users/:accountId/settings/query \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: The signed-in account id <br/>

## Body
```json
{
  "scopeMatchFilters": {
    "v1Platform": ["Windows"]
  }
}
```

`scopeMatchFilters` is `{}` when no platform is passed.

---

_Example Response_

```json
{
  "settings": [
    { "id": "v1AccessibilityAllowVoiceDictation", "userOverrides": [], "default": "false" },
    { "id": "v1AccessibilityReadMessagesAloud", "userOverrides": [], "default": "false" },
    { "id": "v1AgeVerificationChatRestrictionNotificationSeen", "userOverrides": [], "default": "false" },
    { "id": "v1EpicPartiesProfileMoveHasSeenDisclosure", "userOverrides": [], "default": "true" },
    { "id": "v1GlobalNicknamesHasSeenDisclosure", "userOverrides": [ { "scopes": {}, "value": "true" } ], "default": "false" },
    { "id": "v1VoiceChatMode", "userOverrides": [], "default": "openMic" },
    { "id": "v1VoiceChatReportingDisclosureAcceptanceStatus", "userOverrides": [ { "scopes": {}, "value": "seen-accepted" } ], "default": "never-shown" },
    { "id": "v1VoiceInputDevice", "userOverrides": [], "default": "" },
    { "id": "v1VoiceInputVolume", "userOverrides": [], "default": "50" },
    { "id": "v1VoiceOutputDevice", "userOverrides": [], "default": "" },
    { "id": "v1VoiceOutputVolume", "userOverrides": [], "default": "50" },
    { "id": "v1VoicePushToTalkKeybinding", "userOverrides": [], "default": "" }
  ]
}
```

A scoped override looks like (shape from client):

```json
{
  "id": "v1VoiceChatMode",
  "userOverrides": [
    { "scopes": { "v1Platform": "Windows", "v1DeploymentId": "_" }, "value": "pushToTalk" }
  ],
  "default": "openMic"
}
```

Resolution: the first `userOverrides` entry whose `scopes.v1Platform` matches (or is absent) wins, else `default`. Note the client's matcher has an operator-precedence quirk and in practice returns `userOverrides[0]`. Chime settings are absent from the response until written (missing = enabled).
