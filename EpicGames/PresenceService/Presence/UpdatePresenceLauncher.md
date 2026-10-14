## Presence Service - Presence: Update Presence (Launcher)

The Rust launcher (`eglv2_lib::social::presence::publish`, `src\social\presence\publish.rs`) publishes its own presence on its Epic Connect connection and keeps it alive (`Social.Presence.KeepaliveScheduled` / `KeepaliveSent`). Path segments `presence`, `api`, `v1`, `_` and the trailing `presence` are hardcoded in the URL builder; the host is inferred from the environment table. Body field names `status` (`online` / `away`), `conn`, `props` appear next to the builder; nothing is sent while offline (`PatchSkippedOffline`). Method is PATCH per the log strings (`presence PATCH failed`). Needs a live capture to confirm.

URL: https://presence-public-service-prod.ol.epicgames.com/presence/api/v1/_/:accountId/presence/:connectionId \
Method: PATCH \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {EG1 access token} <br/>

## Path Parameters
`accountId`: Your account id <br/>
`connectionId`: Launcher Epic Connect connection id <br/>

## Body
```json
{
  "status": "online",
  "conn": { "props": {} }
}
```
