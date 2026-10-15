## Launcher Service - Artifact Dependencies: Get Config

Dependency config for one build (prerequisites / dependent artifacts installed with it). Fetched during install when the build declares one ([Get Asset (v2)](../Assets/GetAssetV2.md) `metadata.hasDependencyConfig: true`); logged as `Install.DependencyConfigResolved` (`eglv2_lib::api::artifact_dependency`). On failure the previous config is kept (`Download.DependencyConfigKept`).

URL: https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/artifactDependencies/v1/config/:namespace/:catalogItemId/:appName/:buildVersion \
Method: GET \
Auth Required: Yes (Bearer access token)

The URL is the assets base (`/launcher/api/public/assets/v2`) with `/assets/v2` stripped, then `artifactDependencies/v1/config` and the four segments.

## Path Parameters
`namespace`: Catalog namespace <br/>
`catalogItemId`: Catalog item id <br/>
`appName`: App / artifact id <br/>
`buildVersion`: `buildVersion` from [Get Asset (v2)](../Assets/GetAssetV2.md)

---

_Example Response_

Fortnite (`fn` / `4fe75bbc5a674f4f9b356b5c90567da5` / `Fortnite` / `++Fortnite+Release-42.30-CL-58813929-Windows`):

```json
{
  "namespace": "fn",
  "baseCatalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
  "baseArtifactId": "Fortnite",
  "buildVersion": "++Fortnite+Release-42.30-CL-58813929-Windows",
  "created": "2026-10-06T12:04:14.736Z",
  "rvn": 1,
  "aliases": {
    "Fortnite": "Fortnite",
    "FortniteStWContent": "aa31f9e94e844b299ca757d1d0b97a09",
    "FortniteJunoContent": "94bc5ec13f8f438c97fdbef3e9019e27"
  },
  "entries": {
    "Fortnite": {
      "namespace": "fn",
      "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
      "dependencies": []
    },
    "aa31f9e94e844b299ca757d1d0b97a09": {
      "namespace": "fn",
      "catalogItemId": "0b41f0192f7f4f2691684581aedc0778",
      "dependencies": ["Fortnite"]
    },
    "94bc5ec13f8f438c97fdbef3e9019e27": {
      "namespace": "fn",
      "catalogItemId": "b619cf61a4144d67bd753dc990637e7c",
      "dependencies": ["Fortnite"]
    }
  }
}
```

`aliases` maps a readable name to an artifact id; `entries` is keyed by artifact id and lists the artifact ids each one depends on. Here the two content artifacts depend on the base `Fortnite` artifact.

_Example Response (404, build without a dependency config)_

```json
{
  "errorCode": "errors.com.epicgames.launcher.artifact_dependency_config_not_found",
  "errorMessage": "No artifact dependency configuration found for namespace=5b325322a4c04b9e9e780b9a1e9b2d70, baseArtifactId=Grunt, buildVersion=1.2-aeeb6200374fc01a6a51c3006846a350febeb243.21-Win",
  "messageVars": [
    "5b325322a4c04b9e9e780b9a1e9b2d70",
    "Grunt",
    "1.2-aeeb6200374fc01a6a51c3006846a350febeb243.21-Win"
  ],
  "numericErrorCode": 30033,
  "originatingService": "launcher-service",
  "intent": "prod"
}
```
