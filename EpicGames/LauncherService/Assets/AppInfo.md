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

Field names from `AppInfoRequest` (`appKeys`) and its element (`artifactId`, `catalogId`, `sandboxId`). Values are placeholders.

---

_Example Response (shape from client)_

```json
{
  "elements": [
    {
      "appName": "Fortnite",
      "buildVersion": "++Fortnite+Release-32.00-CL-12345678-Windows",
      "sdMetaHash": "94b1569506b04f9f8557af611e8c5e4794b15695",
      "sidecarRvn": 3
    }
  ]
}
```

Field names from `AppInfoElement` (4 fields: `appName`, `buildVersion`, `sdMetaHash`, `sidecarRvn`). The `elements` wrapper is inferred: `AppInfoElement` is deserialized next to `AssetsResponse` (`elements`), the wrapper used by [Get Asset (v2)](GetAssetV2.md). Values are placeholders.

Errors are logged as `Batch app info fetch failed: HTTP ..` / `Failed to parse batch app info` (`Download.BatchAppInfoFetch`). For availability, 401 / 403 / 429 / unreachable / unreadable responses become separate `NotEstablished` reasons; a 429 stops the sweep (`Availability probe rate-limited; stopping sweep`).
