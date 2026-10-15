# Install API

A loopback-only HTTP server inside the launcher (`src\install_api`, axum) that lets games manage their own installation: list installs, query sizes of tag sets, and start install / update / repair / uninstall operations. Fortnite uses it: right after starting, it queued a `Repair` of its Battle Royale add-on through this API.

## Discovery

On start the launcher binds a loopback port (IPv4 and IPv6) and writes `%LOCALAPPDATA%\com.epicgames.eglv2\api.json`:

```json
{
  "version": "0.95.2+gfa9ad49",
  "machineSecret": "<64 hex characters>",
  "port": 36783
}
```

Games are also told about it with the launch arguments `-eglv2` and `-eglv2apipath="<path>"` (not for Unreal Engine namespaces; see [Game Launch](Flows/GameLaunch.md)). Fortnite found it without them. Non-loopback connections are dropped.

## Headers
`x-epic-machine-secret`: `machineSecret` from `api.json`. Missing or wrong: `401` (`InstallApi.MachineSecretRejected`) <br/>
`Content-Type`: application/json (POST / PATCH)

Base URL: `http://127.0.0.1:<port>/api/v1/installation`

## Routes

| Method | Path | What |
| ------ | ---- | ---- |
| POST | `/login` | `204`; acknowledges a game session (`InstallApi.LoginAcknowledged`) |
| GET | `/installations` | Installations known to the launcher |
| POST | `/queryManifestInfo` | Sizes of tag sets for an app, against the latest build |
| GET | `/operations` | Running, queued, suspended and completed operations |
| POST | `/operations` or `/operations/install` | Start an operation; returns `{ "operationId" }` |
| GET | `/operations/{id}` | One operation |
| PATCH | `/operations/{id}` | `{ "downloadRateLimitBps": <n> }`: speed ceiling for that operation |
| DELETE | `/operations/{id}` | Cancel (progress preserved) |
| POST | `/operations/{id}/move-to-running` | Run a queued operation now (`moved-to-running` / `already-running`) |

## GET /installations

```json
{
  "installations": [
    {
      "installationId": "7C7D6290F7A428E71E3826B60AEEE13D",
      "state": "Installed",
      "dir": "D:\\Fortnite",
      "manifestPath": "D:\\Fortnite\\.egstore\\7C7D6290F7A428E71E3826B60AEEE13D.manifest",
      "sandboxId": "fn",
      "itemId": "d75daf91c89b49ecb110b69a7bd68996",
      "artifactId": "afdb5a85efcc45d8ae8e406e2121d81c",
      "tags": [""],
      "pendingTags": [],
      "manifestData": { "version": "1.1" }
    }
  ]
}
```

`state` is `Installed` or `Incomplete`. The base game entry also carries its `dependencyConfig` ([Artifact Dependency Config](../EpicGames/LauncherService/ArtifactDependencies/GetConfig.md)), which is how Fortnite resolves aliases such as `FortniteJunoContent` to add-on content.

## POST /queryManifestInfo

```json
{
  "apps": [
    {
      "sandboxId": "fn",
      "itemId": "4fe75bbc5a674f4f9b356b5c90567da5",
      "artifactId": "Fortnite",
      "installationId": "1061D9CB32B3BAC1ACADBB5DD155FFB3",
      "tagSets": [["GFP_JunoRoot"], ["GFP_SaveTheWorldRoot"]]
    }
  ]
}
```

`sandboxId`, `itemId` and `artifactId` are required (`400`, logged as "app is missing sandboxId"). One result per tag set:

```json
{
  "appsInfo": [
    {
      "tagSetsInfo": [
        { "deltaBuildSize": 9467316793, "totalBuildSize": 9467316793, "deltaDownloadSize": 8743222074, "totalDownloadSize": 8842758260 },
        { "deltaBuildSize": 5011270330, "totalBuildSize": 5011270330, "deltaDownloadSize": 4496711971, "totalDownloadSize": 4541123632 }
      ]
    }
  ]
}
```

`delta*` is what installing that tag set would add to the current install, `total*` the size of the whole tag set. An empty `apps` list returns `{"appsInfo":[]}`.

## GET /operations

```json
{
  "running": [],
  "queued": [],
  "suspended": [],
  "completed": [
    {
      "id": "91EA76FFDECEA959",
      "status": "Success",
      "installationsRevision": "000001A13F4ECD100000000000000003",
      "request": {
        "body": {
          "actions": [
            { "type": "Repair", "sandboxId": "fn", "artifactId": "afdb5a85efcc45d8ae8e406e2121d81c", "dir": "D:\\Fortnite", "tags": [""] }
          ]
        }
      },
      "progress": {
        "bpsOngoingStats": { "state": "Completed", "updateProgress": -1.0, "downloadSize": 0, "downloadedBytes": 0 }
      }
    }
  ]
}
```

Operations started by the launcher itself are listed too (the Fortnite update showed up as `InstallOrUpdate`). Action `type` values: `InstallOrUpdate`, `Repair`, `TagChange`, `Uninstall`. Operation `status` values: `Running`, `Queued`, `Suspended`, `Success`, `Error`, `Cancelled`. The request body to start one is the same `{ "actions": [ ... ] }` object.
