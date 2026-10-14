## SOCS Service - Settings: Update User Setting

Writes one overlay setting. Fired from the voice settings panel (device, volume, mode, push-to-talk key), chime toggles and disclosure dialogs. Setting ids are listed in the [README](../README.md).

URL: https://api.epicgames.dev/epic/socs/v1/users/:accountId/settings/:settingId \
Method: PUT \
Auth Required: Yes (Bearer EG1 access token, any client)

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
    "v1DeploymentId": "_"
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

`v1DeploymentId` is the native app deployment id (inferred to be `_` for EGL, the value it sends as party `deployment_id`; a scoped write was not captured). Success is any `2xx`; the body is not read.
