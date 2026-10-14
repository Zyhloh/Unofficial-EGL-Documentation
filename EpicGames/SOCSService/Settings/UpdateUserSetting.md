## SOCS Service - Settings: Update User Setting

Writes one overlay setting. Fired from the voice settings panel (device, volume, mode, push-to-talk key), chime toggles and disclosure dialogs. Setting ids are listed in the [README](../README.md).

URL: https://api.epicgames.dev/epic/socs/v1/users/:accountId/settings/:settingId \
Method: PUT \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: The signed-in account id <br/>
`settingId`: Setting id, e.g. `v1VoiceInputDevice` <br/>

## Body
Scoped setting:
```json
{
  "scopes": {
    "v1Platform": "Windows",
    "v1DeploymentId": "d0e1f2a3b4c5d6e7f8091a2b3c4d5e6f"
  },
  "value": "pushToTalk"
}
```

Unscoped setting:
```json
{
  "scopes": {},
  "value": "seen-accepted"
}
```

Success is any `2xx`; the body is not read.
