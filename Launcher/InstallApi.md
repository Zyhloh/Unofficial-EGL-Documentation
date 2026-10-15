# Install API

A loopback-only HTTP server inside the launcher (`src\install_api`, axum) that lets games and the EOS install helper manage their own installation: list installs, query sizes, and start install / update / tag change / repair / uninstall operations. Not exercised live; routes and types are from the binary.

## Discovery

On start the launcher picks a free loopback port (IPv4 / IPv6 candidates) and writes `%LOCALAPPDATA%\com.epicgames.eglv2\api.json`:

```json
{
  "version": "0.95.2+gfa9ad49",
  "machineSecret": "<64 hex characters>",
  "port": 36783
}
```

Games learn where it is through the launch arguments `-eglv2` and `-eglv2apipath="<path>"` (not added for Unreal Engine namespaces; see [Game Launch](Flows/GameLaunch.md)). Non-loopback connections are dropped. Every request must carry the secret:

`x-epic-machine-secret`: `machineSecret` from `api.json` <br/>

The expected caller user agent is `epiconlineservicesinstallhelper.exe`.

## Routes

| Route | What |
| ----- | ---- |
| `/api/v1/installation...` | List installations: `InstallationsResponse { installations, installationsRevision }` |
| `queryManifestInfo` | `ManifestInfoRequest` -> `ManifestInfoResponse { appsInfo, TagSetInfo { deltaBuildSize, totalBuildSize, deltaDownloadSize, totalDownloadSize }, dependencyConfig, manifestData }` |
| operation request | `OperationRequestBody { actions: [{ type, sandboxId, artifactId, dir, tags }] }`, `type` = `install`, `update`, `tagchange`, `repair` or `uninstall`. Returns `InstallAccepted { operationId }` |
| `/operations/<id>` | `GET` progress (`OperationProgress`, `OngoingStats`); move to running; `PATCH { "downloadRateLimitBps": <n> }` sets a per-operation speed ceiling; cancel |

The dependency config ([Artifact Dependency Config](../EpicGames/LauncherService/ArtifactDependencies/GetConfig.md)) is handed to games through `queryManifestInfo`, which is how Fortnite resolves aliases such as `FortniteJunoContent` to its add-on content.
