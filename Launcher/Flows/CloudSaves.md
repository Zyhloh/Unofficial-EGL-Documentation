# Cloud Saves

How the launcher syncs save folders with the Data Storage service. Verified live with TerraTech on a real account: the launcher pulled a 2024 save after install, uploaded a new one on exit, and accepted saves written by a third-party client (pull before launch, chunk download included). The [Download Client](../Library/DownloadClient.md) implements the same format and rules (`saves`, `sync-saves`).

## Which games

A game has cloud saves when its catalog item has the custom attribute `CloudSaveFolder` (macOS: `CloudSaveFolder_MAC`; `CloudSaveFolder_Linux` is never read for the path). If `CloudSaveVersion` is set it must be `<= 1.0`. `CloudSaveCustomPathSuffix` is appended to the folder as is. Optional filters: `CloudIncludeList`, `CloudExcludeList`.

Switches: global `cloudSavesEnabled` (app settings), per game `cloudSaves` in `game-settings.json` (`set_cloud_save_enabled`), LaunchDarkly flag `cloud-saves-enabled`.

## Folder variables

The template is expanded with these variables, matched case-insensitively (`{appdata}` works):

| Variable | Windows value |
| -------- | ------------- |
| `{EpicID}` | Account id |
| `{InstallDir}` | Game install folder |
| `{UserDir}` | Documents (`FOLDERID_Documents`) |
| `{AppData}` | **Local** app data (`FOLDERID_LocalAppData`), so `{AppData}/../Roaming/...` and `{AppData}/../LocalLow/...` reach the other two |
| `{UserProfile}` | User profile folder |
| `{UserSavedGames}` | Saved Games (`FOLDERID_SavedGames`) |
| `{UserLibrary}` | Empty (macOS only) |

An unknown `{...}` or an empty variable makes the folder unusable. The expanded path must be absolute and lie inside one of the user folders above. With Proton the same names map into the game's prefix (`drive_c/users/steamuser/...`).

Example: TerraTech's `{UserDir}/My Games/TerraTech/{EpicID}/` -> `C:\Users\<user>\Documents\My Games\TerraTech\<accountId>`.

## Include / exclude lists

Comma-separated, trimmed, matched against the lower-cased relative path (`/` separators). With a non-empty include list a file must match one include; it must then match no exclude. A pattern ending in `/` is a folder rule (path contains it); otherwise it matches as a suffix of the path (`.sav`, `stats.vdf`); a pattern with `*` / `?` is a wildcard over the whole path (`*` crosses folders). Example: The Stanley Parable `save/,cfg/,stats.vdf,stats_sv.vdf,language.txt`.

## Storage format

Per game the cloud folder `savesync/<accountId>/<appName>/` holds:

```
manifests/2026.10.15-12.17.43.manifest
ChunksV4/00/9EF6137997193143_EB4C91A544215B392DFB44A3DE672520.chunk
ChunksV4/63/13F2B424DDC3F52A_5B4E896CCE2B4BC5A6382AA5D4801E18.chunk
```

Each save version is a binary [Manifest](../../EpicGames/ArtifactDeliveryService/Builds/Manifest.md) plus [Chunks](../../EpicGames/ArtifactDeliveryService/Builds/Chunk.md), the same format as game builds:

| Field | Value |
| ----- | ----- |
| Header version / feature level | 17 |
| Meta `appName` | `<appName><accountId>` |
| Meta `buildVersion` | The manifest name without `.manifest` |
| Every section's data version | 0 |
| File names | Relative to the save folder |
| Custom fields | The unexpanded catalog templates: `CloudSaveFolder`, `CloudSaveFolder_Mac`, `CloudSaveFolder_Linux` (when set) |
| Chunks | Header v3, zlib, 1 MiB window padded with zeros, `hashType` 3; rolling hash over the full window; data group `crc32(guid bytes) % 100` |

The manifest name is the upload time in **UTC**, `%Y.%m.%d-%H.%M.%S`, and is always made newer than the previous one; names sort chronologically, and the newest name is the current save. Files are packed back to back into chunks; the launcher reuses chunk data of unchanged files from the previous version (TerraTech: 11 files, 9 reused from the old chunk, 2 changed files packed into 1 new chunk).

The pulled manifest's `CloudSaveFolder` field is expanded first; if it can't be used, the catalog's folder is used ("Save version names a folder we can't use; using the catalog's").

## Requests

| Step | Request |
| ---- | ------- |
| List versions and chunks | [List Files](../../EpicGames/DataStorageService/SaveSync/ListFiles.md) `GET .../access/egstore/savesync/<accountId>/<appName>/` |
| Get upload links | [Request Links](../../EpicGames/DataStorageService/SaveSync/RequestLinks.md) `POST` same path, `{"files":[...]}` |
| Upload | `PUT <writeLink>` with the file bytes: all new chunks first, then the manifest on its own |
| Download | `GET <readLink>` |
| Clean up | [Delete File](../../EpicGames/DataStorageService/SaveSync/DeleteFile.md) `DELETE .../data/egstore/savesync/<accountId>/<appName>/<path>` |

Retention: the newest 3 manifests are kept, older ones deleted. A chunk is deleted when no kept manifest uses it and it is more than 1 hour old.

## Local state

`%LOCALAPPDATA%\com.epicgames.eglv2\cloud-saves\`:

```
state\<accountId>\<appName>\sync.json        {"baseline":"2026.10.15-12.17.43.manifest","lastSyncedAt":"2026-10-15T12:17:43.484532800Z"}
state\<accountId>\<appName>\manifests\       copies of synced manifests
state\<accountId>\<appName>\upload-staging\, staging\
backups\<accountId>\<appName>\<UTC time>\    local saves before a pull overwrote them (about 5 kept)
pending.json                                 {"accounts":{}} owed syncs, retried at startup
```

Change detection: local = SHA-1 of every selected file compared with the baseline manifest's file list; cloud = newest cloud manifest name differs from `baseline`.

## When it syncs

Seen live, in order:

| Moment | What happened |
| ------ | ------------- |
| After install | Pulled `2024.12.30-11.01.13.manifest`: 9 files from 1 chunk (`CloudSaves.PullAfterInstall`) |
| Before launch | Nothing newer: `up_to_date` |
| After exit | Packed 11 files (9 reused), uploaded 1 chunk + `2026.10.15-12.17.43.manifest` (`CloudSaves.Uploaded`) |
| Before launch, after a third-party client uploaded `2026.10.15-12.19.04.manifest` | Backed up local saves, pulled it (`unchanged=11`), dropped the cached copy of a manifest the cloud no longer had |
| After exit | Files equal the baseline: `unchanged`, nothing uploaded |
| Before launch, cloud version with an extra file | Fetched the third-party chunk, wrote the file (`written=1 unchanged=11 fetched_chunks=1`) |

Rules:

- Before launch: cloud newer, local unchanged -> pull (local saves backed up first). Both changed -> `cloud-save-decision-required-event` kind `conflict`: `useLocal`, `useCloud` or `cancelLaunch`. A failed pull asks `retry` / `playAnyway`.
- After exit: local unchanged -> nothing. Cloud moved during play -> kind `exitConflict` (`useLocal`, `useCloud`, `later`). Too big -> `over_size_cap`. Otherwise upload.
- "Sync saves now" (`cloud_save_sync_now`): kind `syncConflict` when both sides changed.
- Answers come back through `cloud_save_resolve { appId, questionId, choice }`; each side is shown as `{hasFiles, modifiedAt, sizeBytes}`.
- Outcomes: `not_supported`, `disabled`, `skipped_offline`, `account_changed`, `nothing_to_upload`, `unchanged`, `uploaded`, `over_size_cap`, `cloud_moved`, `failed`, `up_to_date`, `pulled`, `conflict`.

Progress events: `cloud-save-sync-state-event`, `cloud-save-upload-state-event`. Other commands: `cloud_save_state`, `cloud_save_open_folder`.

The old launcher's per-game switches (`[<account>_Portal.SaveSync]`) and its `CloudCache` baseline are imported once, so the first sync does not treat every file as new.
