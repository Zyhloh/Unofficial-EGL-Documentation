# Install and Update

How a library item becomes files on disk, and how the launcher keeps it updated, verified and repaired. Every step was reproduced with a standalone client ([Download Client](../../Examples/DownloadClient)), which installs, updates, verifies, repairs and uninstalls games, apps, add-ons and engines without the launcher.

## Overview

| Step | Request |
| ---- | ------- |
| Owned items | [Library Items](../../EpicGames/LibraryService/Library/Items.md) |
| Titles, categories, add-ons, custom attributes, art | [Catalog Bulk Items](../../EpicGames/CatalogService/Catalog/BulkItems.md) |
| Build of an item | [Get Asset (v2)](../../EpicGames/LauncherService/Assets/GetAssetV2.md) |
| Dependencies (Fortnite) | [Artifact Dependency Config](../../EpicGames/LauncherService/ArtifactDependencies/GetConfig.md) |
| Optional components | [Selective Download Metadata](../../EpicGames/ArtifactDeliveryService/Builds/SdMeta.md) |
| File and chunk list | [Manifest](../../EpicGames/ArtifactDeliveryService/Builds/Manifest.md) |
| File data | [Chunk](../../EpicGames/ArtifactDeliveryService/Builds/Chunk.md) |
| Update check | [Batch App Info](../../EpicGames/LauncherService/Assets/AppInfo.md) |
| Smaller updates | [Delta Manifest](../../EpicGames/ArtifactDeliveryService/Builds/Delta.md) |
| Deployment id for launch | [Bulk Sidecars](../../EpicGames/LauncherService/Assets/BulkSidecars.md) |

Manifests, chunks and `.sdmeta` files need no Epic token; their URLs carry a short-lived signed query token instead (chunks also download without it).

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

1. **Catalog**: `releaseInfo[]` gives the app name per platform; `mainGameItem` marks an add-on, which installs into its base game's folder (see [Add-ons](../Library/Addons.md)); `customAttributes.FolderName` is the default folder name; `ThirdPartyManagedApp` / `ThirdPartyManagedProvider` route the title to a partner client instead (see [Third-party Titles](../Library/ThirdPartyTitles.md)); `eulaIds` trigger the EULA prompt first.
2. **Build info**: Get Asset (v2) for `platform / namespace / catalogItem / app / label` (10 s timeout, up to 3 retries from 250 ms). It returns `buildVersion`, the manifest `hash` (SHA-1), the manifest mirrors, and optionally `selectiveDownload` + `sdMetaHash`, `metadata.hasDependencyConfig`, `sidecar`. An add-on the account does not own returns `403 not_entitled`; a title with no Epic build returns `404 download_info_not_found`.
3. **Dependencies**: only when `metadata.hasDependencyConfig` is true. Stored on the install record (`dependencyConfig`).
4. **Manifest**: the mirrors are tried in the order given; a copy is accepted when its SHA-1 equals `hash`. Signed tokens expire about 5 minutes after step 2.
5. **Components**: the selected components' install tags filter the file list. A file with no tags is always installed; a tagged file when any of its tags is selected. Without a `.sdmeta`, the tags themselves are the options (Unreal Engine: `templates`, `engine_source`, `platform_*`, ...).
6. **Chunks**: every chunk referenced by a selected file is downloaded once, from the healthiest CDN, decompressed and SHA-1 checked (24 to 64 in parallel, retries, failover and stall timeout in [Chunk](../../EpicGames/ArtifactDeliveryService/Builds/Chunk.md)). Chunks are held in RAM and spill to `<install>\.egstore\chunk_cache` when the budget is full, on pause or on exit.
7. **Assembly**: each file is its chunk parts concatenated in order, written in place (very large files go through `.egl-part` temps) and SHA-1 hashed while streaming. A mismatch flags the file for repair instead of failing the install.
8. **Verify**: with `verifyFilesOnInstall` (on by default) the files are read back after a drive cache flush and hashed again; corruption is repaired.
9. **Prerequisites**: the manifest's `prereqPath` / `prereqArgs` run elevated (UAC). See [Third-party Titles](../Library/ThirdPartyTitles.md#prerequisites-seen).
10. **Record**: the manifest is saved as `<install>\.egstore\<installationId>.manifest`, and the install is appended to `installations.jsonl` (`version` = `buildVersion`, `tags`, `componentSelection`, `dependencyConfig`, `sidecar`, `launchCommand`, `launchExecutable`, `parentInstallationId` for add-ons). An uninstall entry is written under `HKCU\...\Uninstall`.

Live example, Crosshair V2: 626 files, 203 chunks, 101.5 MB download, 201.5 MB on disk, about 1.5 s on a fast connection.

## Sizes without installing

- `get_manifest_info`: steps 2 and 4, then sums file sizes (install) and chunk file sizes (download) for the selected tags.
- `prefetch_manifest { hold: true }`: runs steps 2 and 4 ahead of the click and holds the parsed manifest for a while.
- `get_dlc_manifest_sizes`: a cached `ManifestSummary` (`cache/manifest-summaries/<installationId>.json`: `formatVersion` 3, `buildVersion`, `manifestBytes`, `manifestSha1`, `fileCount`, `installSize`, `downloadSize`, `tags`, `ownershipToken`), the local manifest in `.egstore`, else steps 2 and 4.
- `get_selective_download_info`: served from `sd-cache.json`, revalidated in the background against `buildVersion` + `sdMetaHash`.

## Background update check

1. The first check runs 5 s plus up to 3 s after start, once signed in. After that the interval comes from the LaunchDarkly flags `game-update-check-interval` (default `20`) and `game-update-check-jitter` (default `1.5`), most likely minutes. A deep link or `trigger_update_check` runs a check early.
2. Installed apps are sent to Batch App Info in groups of 50: `{"appKeys":[{"artifactId","catalogId","sandboxId"}]}`. The response is a bare array of `{appName, labelName, buildVersion, catalogItemId, namespace, assetId}`.
3. An update exists when `buildVersion` differs from the install record's `version`. The same pass refreshes sidecars and notices `sdMetaHash` changes.
4. Automatic download: only with `automaticDownloadsEnabled`, the game's `autoUpdate` setting, and inside the download window (`downloadScheduleEnabled`, `downloadScheduleStartMinute`, `downloadScheduleEndMinute`). Add-ons wait for their parent's update. Otherwise the update is offered manually. The new manifest and delta can be fetched ahead of the click.

## Update

1. The old manifest is read from `.egstore` ("No old manifest found in .egstore, treating all files as new").
2. A [delta manifest](../../EpicGames/ArtifactDeliveryService/Builds/Delta.md) is merged into the new manifest when available; otherwise old and new manifests are diffed.
3. Files whose SHA-1 is unchanged are kept. Changed files are built as `<file>.new` temps and swapped in at the end, so an interrupted update resumes from them. Chunk data that already exists in installed files is read from disk ("Chunk-level dedup: reusing existing chunks from installation"); only the rest is downloaded. An in-place mode with a journal also exists (`EGL_DESTRUCTIVE_UPDATES`).
4. Files the new build no longer has are deleted after the swap, except files that another installation in the same folder still lists (add-ons and their parent share a folder). If a sibling's manifest cannot be read, nothing is deleted.
5. With `verifyAllFilesOnUpdate` the untouched files are verified while the download runs.

Live example, Fortnite 42.30 -> 42.40 (launcher log and our client agree on every number):

| Step | Result |
| ---- | ------ |
| Batch App Info | `buildVersion` `++Fortnite+Release-42.40-CL-59086525-Windows` differs from the record |
| Delta | `Deltas/Ui2VxPBjUkymuiCJyoZ-FA/vtuT6fElREubMbN1CCx_7g.delta`, 11 MB, merged (449 files, 149,599 chunks) |
| Diff | 694 selected files: 324 unchanged, 370 changed, 44 removed |
| Chunks | 63,642 needed, 60,234 read from installed files, 3,408 downloaded (3.01 GB, shown as "2.8 GB"); "Written 3.3 GB" in the UI is the uncompressed chunk data |
| Assembly | 370 files rebuilt into temps (29 files over 256 MiB streamed), 59.9 GB read from the old files, then renamed over the originals; 44 obsolete files deleted |
| Time | 33 s on a fast NVMe drive and connection |

Without the delta the same update would download 13,286 chunks (12.3 GB).

Smaller example, Quixel Bridge 5.7 build updated in place to the 5.8 build (no delta, different apps): 231 files, 198 kept, 33 rewritten, 2 deleted, 32 MB downloaded instead of 80 MB.

`modify_install` (changing components) goes through the same path with the installed build: newly selected tags are downloaded, deselected files are deleted.

## Verify and repair

1. The latest manifest is fetched (steps 2 and 4). If it cannot be downloaded the verify fails (`FNO-P-11`).
2. Every selected file is hashed (SHA-1) against the manifest; `verify-repair-started-event` reports how many are corrupt or missing.
3. Repair rebuilds what it can from local data, downloads the chunks of the remaining bad files and retries a bounded number of times ("Repair: exhausted retries, leaving the installation incomplete").

Live example: one corrupted and one deleted file in Crosshair V2 were found and repaired by downloading 2 chunks.

## Uninstall

Seen live on Crosshair V2 (`uninstall_game`, `trigger=user`):

1. Any live download of the app is cancelled (bytes kept for a later resume).
2. The record is rewritten with `complete: false`.
3. The install folder is renamed to `<dir>.egl-uninstalling-<timestamp>` and deleted in the background, so the whole folder goes, including files the manifest does not list (saves or configs a game wrote there).
4. The `EpicGames-<appName>` Add/Remove Programs entry and `cache\manifest-summaries\<installationId>.json` are removed.
5. A tombstone `{"installationId":"8CE0EF97CDEE4101095806EB75F3D336","deleted":true,"writtenAt":"..."}` is appended to `installations.jsonl`, and the title goes back to `CanInstall`.

Add-ons share their parent's folder, so they are removed file by file instead: the files listed by the add-on's manifest are deleted, except files another installation in the same folder still lists. Uninstalling a base game uninstalls its add-ons first. Ownership token files are removed. Manifest uninstall actions (`uninstallActionPath`) are not run.

## Queue and resume

One operation runs at a time; others wait in `download\queue.json` (`{version, operations[]}`, each with `op_id`, `app_id`, `kind`, `priority`, `volume`, `state` `Queued` / `Active` / `Paused`, install parameters). On resume the launcher re-reads the cached manifest (`.resume_manifest.bin`), counts chunks already in `chunk_cache` and reuses `.new` / `.egl-part` temps. Speed limits: `downloadSpeedLimit`, `downloadSpeedLimitGameplay` (while a game runs).

## Install API for games

Games can ask the launcher to install, update, change tags, repair or uninstall through a loopback HTTP API; see [Install API](../InstallApi.md).
