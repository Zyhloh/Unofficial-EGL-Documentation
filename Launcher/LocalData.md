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
  heroes\_index.json, <md5>.jpg      detail page heroes
  images\_index.json, <md5>.jpg      cover cache (served as http://img.localhost/<md5>)
  images\heroes\_index.json, _meta.json
  installations.jsonl                append-only installation records
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

Other names in the exe that live under the data dir (exact folder not confirmed): `pending-uninstalls.json`, `recently-played.json`, `last-played.json`, `playtime-cache.json`, `project-state.json`, `in-place-update.json`, `self-update-applied.json`, `stable-target.json`, `fab-settings.json`, `ld-overrides.json` / `ld-overrides.jsonc`, `api.json` (install API record), `cloud-saves\state\...`, `listings_v1.db` (Fab vault index), `fab.jsonl`, `ue-gates-cache.json`, `platform-availability-cache.json`, `voice-settings.json`, per-account `app-settings.json`.

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

## Other locations

| Path | What |
| --- | --- |
| `%PROGRAMDATA%\Epic\UnrealEngineLauncher\LauncherInstalled.dat` | v1 install list, read by the install scan and Fab UE targets |
| `%PROGRAMDATA%\Epic\EpicGamesLauncher\Data\Manifests\*.item` | v1 item manifests, read by the install scan (`.item`, `.pending.item`, `.returned.item`) |
| `%LOCALAPPDATA%\EpicGamesLauncher\Saved\...` | v1 data, read by the v1 migration (settings, cloud save baseline) |
| `SOFTWARE\Classes\com.epicgames.launcher` (hive not resolved) | URL protocol registration, see [Deep Links](DeepLinks.md) |
| `SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{D0769F44-D459-450F-B084-CAE38062C75B}` | Uninstall entry the launcher checks for "installed copy" |
| Mutex `Global\EpicLauncherV2InstallerMutex` | Held by the NSIS installer during a self update |
| Mutex `Local\com.epicgames.eglv2-v1-removal` | v1 removal in flight |

The v1 paths are reconstructed from string pieces (`ProgramData`, `UnrealEngineLauncher`, `LauncherInstalled.dat`, `EpicGamesLauncher`, `Data`, `Manifests`); exact joining is inferred.
