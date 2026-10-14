# Cloud Saves

EGL v2 syncs save folders of games that declare `CloudSaveFolder` (also `CloudSaveFolder_MAC`, `CloudSaveFolder_Linux`, `CloudIncludeList`, `CloudExcludeList`, `CloudSaveCustomPathSuffix` catalog custom attributes) to the Data Storage service. Rust: `eglv2_lib::cloud_saves::{service, sync, upload, restore, packer, probe, gate, pending, backup, paths, state, v1_import}`, commands in `commands::cloud_saves`.

Switches: global `cloudSavesEnabled` (app settings), per game `set_cloud_save_enabled` (`game-settings.json` `cloudSaves`), flag `cloud-saves-enabled`.

## Storage format

Saves are not uploaded file by file. The packer (`cloud_saves::packer`) splits the save folder into chunks and writes a manifest (UE BuildPatch style, `CloudSaves.BuildPacked file_count chunk_count`). Remote layout under the account (inferred from `manifests` / `Chunks` path pieces and the cleanup events):

```
egstore/savesync/<accountId>/<appName>/manifests/<name>.manifest
egstore/savesync/<accountId>/<appName>/Chunks/...
```

Local state: `cloud-saves/state`, the save root `Saved/Saves/<account>/<slug>`, and a `CloudCache`.

## Services

| Step | Endpoint |
| --- | --- |
| List remote manifests / chunks with read links | [List Files](../../EpicGames/DataStorageService/SaveSync/ListFiles.md) |
| Signed write links for new files | [Request Links](../../EpicGames/DataStorageService/SaveSync/RequestLinks.md) |
| Upload | `PUT` to each `writeLink` |
| Download | `GET` each `readLink` |
| Delete superseded manifest / unused chunks | [Delete File](../../EpicGames/DataStorageService/SaveSync/DeleteFile.md) |

## Flow

1. Before launch (`cloud_saves::gate`, `CloudSaves.PullBeforeLaunch`): list manifests, compare with the last synced manifest. Newer cloud data is pulled (`CloudSaves.Pulled`). Local saves are backed up first (`CloudSaves.LocalSavesBackedUp`).
2. Conflict (both sides changed): the launch waits on `cloud-save-decision-required-event`; the UI answers with `cloud_save_resolve` (`{ appId, questionId, choice }`). Error kind `cloud_save_decision_required` exists for launches blocked on this (inferred).
3. After the game exits (`CloudSaves.UploadWaitingForExit`) the folder is packed, links requested, chunks + manifest uploaded (`CloudSaves.Uploaded`, `CloudSaves.UploadFinished`), then old manifests and unused chunks deleted (`CloudSaves.CleanedUp`).
4. Failed uploads are remembered in a pending list and retried (`CloudSaves.OwedRetryStarted`, `CloudSaves.InterruptedUploadResumed`).
5. After an install the cloud copy is pulled once (`CloudSaves.PullAfterInstall`).

Progress events: `cloud-save-sync-state-event`, `cloud-save-upload-state-event`. Manual: `cloud_save_sync_now`, `cloud_save_state`, `cloud_save_open_folder`. Debug: `cloud_save_probe`, `cloud_save_debug_upload`.

v1 import: `cloud_saves::v1_import` takes the UE launcher's per-game `[<account>_Portal.SaveSync]` switches and its baseline so the first v2 sync does not see every file as new.
