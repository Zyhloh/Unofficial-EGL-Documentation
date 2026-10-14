# Install and Update

How the launcher turns a library item into files on disk: which metadata it requests, how manifest and chunk URLs are built, and how updates, selective downloads, DLC sizes and verification reuse the same pieces. The manifest parser itself (`eglv2-manifest` crate) is not described; see [Manifest](../../EpicGames/ArtifactDeliveryService/Builds/Manifest.md) for the format notes.

## IPC

| Command | Args | Purpose |
| ------- | ---- | ------- |
| `get_manifest_info` | `appId`, `selectedTags` | `{ downloadSize, installSize }` for the install dialog |
| `get_selective_download_info` | `appId` | Optional components (`SelectiveDownloadInfo`) |
| `get_dlc_manifest_sizes` | `parentAppId`, `items` | Sizes of add-ons for one game |
| `prefetch_manifest` | `appId`, `hold` | Fetch and hold the manifest before the user confirms |
| `install_game` | `appId`, `installPath`, `selectedTags`, `operationId` | Start an install |
| `modify_install` | `appId`, `newTags` | Add / remove components |
| `update_game` | `appId` | Start an update |
| `verify_game_files` / `cancel_verify` | `appId` | Verify and repair |
| `resume_download`, `resume_incomplete_install` | `appId` | Resume |
| `get_installed_games`, `get_all_product_states` | | Install records and per-game state (`canLaunch`, `canInstall`, `updating`, `installing`, `paused`, `verifying`, `repairing`, ...) |

Progress is pushed with `download-progress-event`, `download-queue-state-event` and `product-state-changed-event`.

## Install

1. **Catalog** — the item must be in the catalog cache, otherwise it is fetched with [Catalog Bulk Items](../../EpicGames/CatalogService/Catalog/BulkItems.md) ("Fetched the uncached catalog entry of ..."). `releaseInfo` decides platform availability; `mainGameItem` decides whether an add-on installs into its parent's directory; `eulaIds` drive the library EULA gate (`eula-prompt-event`) before the install proceeds.
2. **Build info** — [Get Asset (v2)](../../EpicGames/LauncherService/Assets/GetAssetV2.md) for `platform / namespace / catalogItem / app / label`. Transient errors and timeouts are retried with backoff ("Retrying manifest metadata fetch after backoff"). The element gives `buildVersion`, manifest mirrors, manifest SHA-1 (`hash`), `selectiveDownload`, `sdMetaHash`, `cdnBaseUrls` and `sidecar`.
3. **Dependencies** — [Artifact Dependency Config](../../EpicGames/LauncherService/ArtifactDependencies/GetConfig.md) for `namespace / item / app / buildVersion`, stored on the install record (`dependencyConfig`).
4. **Manifest** — [Manifest](../../EpicGames/ArtifactDeliveryService/Builds/Manifest.md) from the first mirror whose bytes parse and match `hash` (SHA-1).
5. **Components** — the selected install tags (`selectedTags`) filter the manifest's file list. Component definitions come from [`.sdmeta`](../../EpicGames/ArtifactDeliveryService/Builds/SdMeta.md) or, without one, from the manifest install tags.
6. **Chunks** — for each needed chunk, [Chunk](../../EpicGames/ArtifactDeliveryService/Builds/Chunk.md) `{cdnBaseUrl}/{ChunksDir}/{group:02}/{hash:016X}_{guid}.chunk`, trying every `cdnBaseUrls` entry on failure; decompressed, SHA-1 checked, cached in `.egstore/chunk_cache`.
7. **Assembly** — files are written from chunk parts and hashed while streaming; a mismatch leaves the file for a later verify instead of failing the install.
8. **Prerequisites** — the manifest's prerequisite (`PrereqPath`, `PrereqArgs`, `PrereqIds`) is run; a failure raises `prereq-failed-event`. `prereqSha1Hash` / `lastPrereqSucceededSha1Hash` on the record avoid re-running it.
9. **Record** — the manifest is saved as `.egstore/<id>.manifest` and the install is appended to `installations.jsonl` (`version` = `buildVersion`, `tags`, `componentSelection`, `sidecar`, `launchCommand`, `launchExecutable`, ...).

## Sizes without installing

- `get_manifest_info`: steps 2 and 4, then sums file / chunk sizes for the selected tags.
- `prefetch_manifest { hold: true }`: runs steps 2 and 4 ahead of the click and holds the parsed manifest for a while (`ManifestHold`, expires; `ManifestHoldFailedInstall` when the held copy cannot be used).
- `get_dlc_manifest_sizes`: for each add-on, either a cached `ManifestSummary` (`formatVersion`, `buildVersion`, `manifestBytes`, `manifestSha1`, `fileCount`, `installSize`, `downloadSize`, `tags`, `ownershipToken`) or the local manifest in `.egstore`, else steps 2 and 4 (`DlcSizeFromManifestSummary`, `DlcSizeFromLocalManifest`, `DlcSizeLookupFailed`).
- `get_selective_download_info`: served from `sd-cache.json`, revalidated in the background against `buildVersion` + `sdMetaHash` (`selective-download-info-updated-event`).

## Update

1. A background check (interval from the `game-update-check-interval` / `game-update-check-jitter` flags) runs [Get Asset (v2)](../../EpicGames/LauncherService/Assets/GetAssetV2.md) for installed games and compares `buildVersion` with the record's `version` (inferred: the check's request path was not traced, but `AssetElement.buildVersion` is the only build version source in the client).
2. The new manifest (and a delta, if any) can be downloaded ahead of the click ("update manifest and delta stored ahead of the click").
3. The old manifest is read from `.egstore` ("No old manifest found in .egstore, treating all files as new"). If no installed file changed since install, the delta fetch is skipped.
4. [Delta Manifest](../../EpicGames/ArtifactDeliveryService/Builds/Delta.md) `{cdnBaseUrl}/Deltas/{a}/{b}.delta` is merged into the new manifest when it fits; otherwise the client diffs old vs new manifest.
5. Only changed chunks are downloaded; chunks that can be rebuilt from local data are reused ("Download.ChunkReuseChecked"). New files are written as `.new` temps and swapped in at the end, so an interrupted update resumes from them.

`modify_install` uses the same path with the installed build: if the installed manifest is the latest (SHA-1 match) it is not downloaded again.

## Verify and repair

1. The latest manifest is fetched (steps 2 and 4). If it cannot be downloaded the verify fails (`FNO-P-11`).
2. Every file is hashed against the manifest; `verify-repair-started-event` reports how many files are corrupt or missing.
3. Repair rebuilds what it can from local data, downloads the remaining chunks and retries a bounded number of times ("Repair: files still damaged, retrying", "Repair: exhausted retries, leaving the installation incomplete").

Settings `verifyFilesOnInstall` and `verifyAllFilesOnUpdate` add a verify pass after installs / updates.

## Uninstall of an add-on

DLC files are located from the add-on's manifest in `.egstore`; if it is missing the manifest is fetched again (needs a signed-in session: "Cannot uninstall DLC: no local manifest and not authenticated").
