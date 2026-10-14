## Launcher Service - Assets: Bulk Sidecars

Refreshes the stored "artifact sidecars" (per-artifact config blob + revision) for installed games (`src\api\sidecars.rs`, `Download.SidecarsRefreshed`). The sidecar's revision and deployment id are later passed to the game at launch. A sidecar is also delivered inline in [Get Asset (v2)](GetAssetV2.md) (`sidecar`).

URL: https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/bulk/sidecars \
Method: PUT \
Auth Required: Yes (Bearer access token)

The URL is the assets base with its trailing `/v2` removed, plus `/bulk/sidecars`. The update-check call site sends it through the launcher's PUT helper. The body type is `SidecarQuery`; its fields were not recovered.

## Headers
`Content-Type`: application/json <br/>

---

_Example Response (shape from client)_

```json
{
  "data": [
    {
      "namespace": "fn",
      "appName": "Fortnite",
      "config": "{}",
      "rvn": 3
    }
  ]
}
```

Field names from `SidecarsResponse` (`data`) and `SidecarEntry` (`config`, `rvn`, `appName`, `namespace`). Values are placeholders.
