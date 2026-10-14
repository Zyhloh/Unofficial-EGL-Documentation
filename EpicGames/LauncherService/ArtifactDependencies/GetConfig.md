## Launcher Service - Artifact Dependencies: Get Config

Dependency config for one build (prerequisites / dependent artifacts installed with it). Fetched during install when the build declares one; logged as `Install.DependencyConfigResolved` (`eglv2_lib::api::artifact_dependency`). On failure the previous config is kept (`Download.DependencyConfigKept`).

URL: https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/artifactDependencies/v1/config/:namespace/:catalogItemId/:appName/:buildVersion \
Method: GET \
Auth Required: Yes (Bearer access token)

The URL is the assets base (`/launcher/api/public/assets/v2`) with `/assets/v2` stripped, then `artifactDependencies/v1/config` and the four segments. GET is inferred (URL-only builder, no body type).

## Path Parameters
`namespace`: Catalog namespace <br/>
`catalogItemId`: Catalog item id <br/>
`appName`: App / artifact id <br/>
`buildVersion`: `buildVersion` from [Get Asset (v2)](../Assets/GetAssetV2.md)

---

_Example Response (shape from client)_

```json
{
  "namespace": "fn",
  "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
  "revision": 1,
  "rvn": 1,
  "dependencies": [],
  "aliases": [],
  "entries": []
}
```

Field names from `DependencyConfig` / `DependencyEntry` (`namespace`, `catalogItemId`, `dependencies`, `revision`, `rvn`, `aliases`, `entries`); which fields belong to which of the two structs was not separated, so the nesting is inferred. Values are placeholders.
