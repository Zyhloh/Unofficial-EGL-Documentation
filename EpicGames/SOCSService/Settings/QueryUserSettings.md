## SOCS Service - Settings: Query User Settings

Loads the overlay settings once the account id and `osName` are known (`fetch-initial-socs-settings`). The result becomes the `socs-settings` value that the overlay then pushes to the EOS SDK as `update-voice-settings`.

URL: https://api.epicgames.dev/epic/socs/v1/users/:accountId/settings/query \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

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

_Example Response (shape from client)_

```json
{
  "settings": [
    {
      "id": "v1VoiceChatMode",
      "default": "openMic",
      "userOverrides": [
        {
          "scopes": { "v1Platform": "Windows", "v1DeploymentId": "d0e1f2a3b4c5d6e7f8091a2b3c4d5e6f" },
          "value": "pushToTalk"
        }
      ]
    },
    {
      "id": "v1VoicePushToTalkKeybinding",
      "default": "...",
      "userOverrides": [
        { "scopes": { "v1Platform": "Windows" }, "value": "CONTROL+V" }
      ]
    }
  ]
}
```

Resolution: the first `userOverrides` entry whose `scopes.v1Platform` matches (or is absent) wins, else `default`. Note the client's matcher has an operator-precedence quirk and in practice returns `userOverrides[0]`.
