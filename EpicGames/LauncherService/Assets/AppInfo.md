## Launcher Service - Assets: Batch App Info

Current build version for many apps in one call (`AppInfoRequest`, `Fetching batch app info`). Used by two features:

- Game update checks (`check_for_updates`, timer driven by `game-update-check-interval` / `game-update-check-jitter`): installed games are sent in chunks; when `buildVersion` differs from the installed one an update is flagged (`Update available`, else `Update check: remote build version matches installed (no update)`). A changed `sdMetaHash` triggers a selective-download re-check, a changed `sidecarRvn` a [Bulk Sidecars](BulkSidecars.md) refresh (inferred from the log strings in the same function).
- Platform availability (`probe_platform_availability` `{ appIds }`, `src\platform_availability.rs`): library titles are probed in paced batches to decide whether each one has a build for the host platform. Results are emitted as `PlatformAvailabilityDelta` and cached (`get_platform_availability`).

URL: https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/platform/:platform/label/:label/appInfo \
Method: POST \
Auth Required: Yes (Bearer access token)

The URL is the assets base (`.../launcher/api/public/assets/v2`) with its trailing `/v2` removed, then `/platform/{}/label/{}/appInfo`.

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer <access token> <br/>

## Path Parameters
`platform`: Host platform name, e.g. `Windows` <br/>
`label`: Build label, e.g. `Live` <br/>

## Body
```json
{
  "appKeys": [
    {
      "artifactId": "Fortnite",
      "catalogId": "4fe75bbc5a674f4f9b356b5c90567da5",
      "sandboxId": "fn"
    }
  ]
}
```

`artifactId` = app name, `catalogId` = catalog item id, `sandboxId` = namespace. The `appKeys` wrapper is required; a bare array or any other wrapper key is rejected (see below).

---

_Example Response_

Bare array, one entry per resolved app key.

```json
[
  {
    "appName": "Grunt",
    "labelName": "Live-Windows",
    "buildVersion": "1.2-aeeb6200374fc01a6a51c3006846a350febeb243.21-Win",
    "catalogItemId": "9d60f0d4300a407e817ce5548f12f12d",
    "namespace": "5b325322a4c04b9e9e780b9a1e9b2d70",
    "assetId": "Grunt"
  }
]
```

The client's `AppInfoElement` reads `appName`, `buildVersion`, `sdMetaHash`, `sidecarRvn`; `sdMetaHash` / `sidecarRvn` were absent for the app captured (no selective download, no sidecar).

_Example Response (400, object without `appKeys`, e.g. `{"elements":[...]}`)_

```json
{
  "errorCode": "errors.com.epicgames.launcher.bad_argument",
  "errorMessage": "Please check the request. Required request.appKeys are missed.",
  "messageVars": [],
  "numericErrorCode": 30016,
  "originatingService": "launcher-service",
  "intent": "prod"
}
```

_Example Response (400, bare array body)_

```json
{
  "errorCode": "errors.com.epicgames.common.json_mapping_error",
  "errorMessage": "Json mapping failed.",
  "numericErrorCode": 1019,
  "originatingService": "launcher-service",
  "intent": "prod"
}
```

Errors are logged as `Batch app info fetch failed: HTTP ..` / `Failed to parse batch app info` (`Download.BatchAppInfoFetch`). For availability, 401 / 403 / 429 / unreachable / unreadable responses become separate `NotEstablished` reasons; a 429 stops the sweep (`Availability probe rate-limited; stopping sweep`).
