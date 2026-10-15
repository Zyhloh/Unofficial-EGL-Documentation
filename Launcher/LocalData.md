# Local Data

Tauri app identifier `com.epicgames.eglv2`. Data dir `%LOCALAPPDATA%\com.epicgames.eglv2` (older files are moved from `%APPDATA%\com.epicgames.eglv2` by the `run:roaming_migration` startup step). Layout below is from a live install of 0.95.1 plus file names in the exe; account ids shown as `<accountId>`, environment as `<env>`.

```
%LOCALAPPDATA%\com.epicgames.eglv2\
  EBWebView\                         WebView2 user data folder (shared by all webviews, guarded by a lockfile)
  auth\
    auth.json                        per-environment session info
    access-token-<env>.dpapi         DPAPI encrypted access token cache
  cache\
    disk-size-cache.json
    manifest-summaries\<hash>.json
    social-overlay-bindings.json
    <env>\
      account\                       per-account caches (library, collections, playtime, ...)
      catalog-cache.json
      engines-cache.json
      tools-cache.json
      product-art-cache.json
      product-mapping-cache.json
      sd-cache.json                  selective download metadata
      store-tags-cache.json
      launchdarkly\flags.json         last known flag values
  device.json                        { device_id, login_id }
  download\
    queue.json
    activity.json
  feedback\history-<env>.json
  heroes\_index.json, <sha1>.jpg     detail page heroes
  images\_index.json, <md5>.jpg      cover cache (served as http://img.localhost/<md5>)
  images\heroes\_index.json, _meta.json
  installations.jsonl                append-only installation records
  installations.jsonl.prev           previous copy
  last-version.txt                   last launched version, e.g. 0.95.1+ge288862
  logs\EpicGamesLauncher_<YYYY-MM-DD_HH-MM-SS>.log
  settings\
    app-settings.json                global settings (get_settings / patch_settings)
    chat-settings.json
    game-settings.json               per-game settings (launch args, cloud saves toggle)
    ui-preferences.json
    window-geometry.json
    account\<accountId>\library-settings.json
  telemetry\
    session-ever-ran.marker
    spool\seg-<ms>-<pid>-<n>.jsonl, spool.lock
  ue\custom-engines.json
  update-splash\EpicGamesLauncherUpdate-<version>.exe, close
```

Other names in the exe that live under the data dir (exact folder not confirmed): `pending-uninstalls.json`, `recently-played.json`, `last-played.json`, `playtime-cache.json`, `project-state.json`, `in-place-update.json`, `self-update-applied.json`, `stable-target.json`, `fab-settings.json`, `ld-overrides.json` / `ld-overrides.jsonc`, `api.json` (see [Install API](InstallApi.md)), `cloud-saves\` (confirmed directly under the data dir, see [Cloud Saves](Flows/CloudSaves.md#local-state)), `listings_v1.db` (Fab vault index), `fab.jsonl`, `ue-gates-cache.json`, `platform-availability-cache.json`, `voice-settings.json`, per-account `app-settings.json`.

Refresh tokens are not on disk; see [Token Storage](Auth/TokenStorage.md) (Credential Manager service `com.epicgames.eglv2.<env>`).

## app-settings.json

Keys of a live file:

| Key | Notes |
| --- | --- |
| `defaultInstallDir` | Default `C:\Users\<user>\Epic Games` |
| `minimizeToTray`, `startOnBoot` | |
| `enableNotifications`, `suppressNotificationsWhileGaming` | |
| `maxConcurrentDownloads`, `downloadSpeedLimit`, `downloadSpeedLimitGameplay`, `downloadSpeedUnit` | |
| `downloadScheduleEnabled`, `downloadScheduleStartMinute`, `downloadScheduleEndMinute`, `automaticDownloadsEnabled`, `autoLaunchOnDownloadComplete`, `retryCanceledUpdates`, `verifyFilesOnInstall`, `verifyAllFilesOnUpdate` | |
| `locale`, `defaultMainTab`, `lastVisitedTab` | |
| `updaterEndpoint` | Self-update endpoint override (null) |
| `environment` | Persisted environment, see [Environments](Environments.md) |
| `releaseChannel` | `stable` / `stage` / `canary` / `manual` |
| `showBuildBadges`, `showPerformanceOverlay`, `developerModeEnabled`, `enableDeveloperShortcuts`, `devBuildPollingTier`, `verboseLogs` | Staff / developer |
| `hideSocialPanel`, `socialOverlayUrl` | Social panel; the URL only applies with `-debugtools` |
| `egsZeroTrust` | Staff: load the EGS v2 store behind Cloudflare Access |
| `performanceProfile` | `{ preset, customOverrides }` |
| `showWhatsNewOnStartup`, `lastWhatsNewVersionShown`, `ftueSeen`, `v1Migrated` | |
| `externalSourcesEnabled`, `externalRescanIntervalMinutes` | Steam / Xbox import |
| `idleTimeoutMinutes` | Presence idle |
| `topBar`, `topBarHintSeen`, `topBarHintRippleCount` | Top bar layout |
| `cloudSavesEnabled` | |

## installations.jsonl

First line is a header, then one JSON object per write. The newest line for an `installationId` wins; an install in progress is written with `complete: false` and `pendingVersion` / `pendingTags`, then again with `complete: true` and `version` / `tags`. Deleted installs are tombstones `{installationId, writtenAt, deleted}`. The file is compacted from time to time (`installations.jsonl.prev` is the previous copy).

```json
{"version":1,"writtenAt":"2026-10-14T22:52:11Z","entries":7}
{"installationId":"7C7D6290F7A428E71E3826B60AEEE13D","complete":true,"dir":"D:\\Fortnite","platform":"Windows","namespace":"fn","itemId":"d75daf91c89b49ecb110b69a7bd68996","artifactId":"afdb5a85efcc45d8ae8e406e2121d81c","version":"1.1","tags":[""],"parentInstallationId":"1061D9CB32B3BAC1ACADBB5DD155FFB3","launchCommand":"","launchExecutable":"","writtenAt":"2026-10-14T15:22:55Z"}
```

Base game entries also carry `componentSelection` (`sdMetaHash`, `selected` and `known` component ids, `governedTags`), `dependencyConfig`, `sidecar` (`revision`), and `launchCommand` / `launchExecutable` from the manifest. Other fields of the record: `mainArtifactId`, `isFab`, `prereqSha1Hash`, `lastPrereqSucceededSha1Hash`. The manifest of each installation is `<dir>\.egstore\<installationId>.manifest`. New installs get a random 128-bit id (32 upper-case hex characters, not a UUID: `8CE0EF97CDEE4101095806EB75F3D336` for a fresh Crosshair V2 install); the same item installed again gets a new one. Installs imported from the old launcher keep its installation GUID.

## Download state

`download\queue.json`: `{ "version": 1, "operations": [] }`, see [Install and Update](Flows/InstallAndUpdate.md#queue-and-resume). `download\activity.json`: per account a list of `{ key: "<namespace>:<itemId>:<appName>", kind: "installed", at: <ms> }`. `cache\disk-size-cache.json`: `{ entries: [{ app_id: { namespaceId, itemId, appName }, bytes, measured_at_ms }] }`.

## game-settings.json

```json
{
  "games": {},
  "addons": {
    "fn:4fe75bbc5a674f4f9b356b5c90567da5:Fortnite": {
      "fn:1e8bda5cfbb641b9a9aea8bd62285f73:Fortnite_Studio": false,
      "fn:d75daf91c89b49ecb110b69a7bd68996:afdb5a85efcc45d8ae8e406e2121d81c": true
    }
  },
  "cloudSaves": {}
}
```

`games` holds per-game settings (`autoUpdate`, `priorityDownload`, `additionalCommandsEnabled`, launch args, `cloudSaves`, `showNotifications`); `addons` is the [Manage add-ons](Library/Addons.md#add-on-toggles) opt-in map.

## Other locations

| Path | What |
| --- | --- |
| `%PROGRAMDATA%\Epic\UnrealEngineLauncher\LauncherInstalled.dat` | v1 install list, read by the install scan and Fab UE targets |
| `%PROGRAMDATA%\Epic\EpicGamesLauncher\Data\Manifests\*.item` | v1 item manifests, read by the install scan (`.item`, `.pending.item`, `.returned.item`) |
| `%LOCALAPPDATA%\EpicGamesLauncher\Saved\...` | v1 data, read by the v1 migration (settings, cloud save baseline) |
| `SOFTWARE\Classes\com.epicgames.launcher` (hive not resolved) | URL protocol registration, see [Deep Links](DeepLinks.md) |
| `SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{D0769F44-D459-450F-B084-CAE38062C75B}` | Uninstall entry the launcher checks for "installed copy" |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\EpicGames-<appName>` | Written for every installed game: `DisplayName`, `InstallLocation`, `Publisher` (catalog developer), `DisplayIcon` (`<launchExe>,0`), `EpicAppId` (`<namespace>:<itemId>:<appName>`), `EstimatedSize` (KB), `NoModify` and `NoRepair` `1`, `UninstallString` = `"<launcher exe>" "com.epicgames.launcher://apps/<namespace>:<itemId>:<appName>?action=uninstall"` |
| Mutex `Global\EpicLauncherV2InstallerMutex` | Held by the NSIS installer during a self update |
| Mutex `Local\com.epicgames.eglv2-v1-removal` | v1 removal in flight |

The v1 paths are reconstructed from string pieces (`ProgramData`, `UnrealEngineLauncher`, `LauncherInstalled.dat`, `EpicGamesLauncher`, `Data`, `Manifests`); exact joining is inferred.
