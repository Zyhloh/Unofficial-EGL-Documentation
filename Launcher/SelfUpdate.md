# Self Update

EGL v2 updates itself with the Tauri updater (signed NSIS setup, minisign public key `C39BFB6A058EE12B`, `installMode: quiet`). Whether and to what version it updates is decided by LaunchDarkly flags, with a CDN file as fallback / emergency switch. Code: `eglv2_lib::commands::updater`, `src\stable_target.rs`, `src\self_update_boot_gate.rs`, `commands::update_swap_splash`; frontend `features/updates`.

## Inputs

| Input | Source |
| --- | --- |
| `self-update-mode` | Flag: `encouraged` (bottom bar "update and restart"), `forced` (required), `disabled` (default) |
| `self-update-target-version` | Flag: exact version incl. `+g` hash, e.g. `0.95.2+gfa9ad49`. Must differ from the running version; older means roll back |
| `self-update-cdn-base-urls` | Flag: list of CDN bases tried in order |
| `self-update-forced-hold-minutes` / `self-update-lazy-hold-minutes` | Flags: random start delay 0..N minutes (defaults 15 / 60) |
| Stable target | [Stable Target](#stable-target) file on the CDN |
| Release channel | `stable` (default), `stage`, `canary`, `manual` (opt out). Sent as `releaseChannel` on the LaunchDarkly `machine` context so flag rules target cohorts. `get_release_channel` / `set_release_channel`, event `release-channel-changed-event` |

## Stable target

URL: https://content-download-egs.distro.on.epicgames.com/Builds/EGLv2/stable-target.json \
Method: GET \
Auth Required: No

```json
{
  "version": "0.95.2+gfa9ad49",
  "mode": "encouraged",
  "emergencyOverride": false
}
```

`StableTargetFile`: `version`, `mode` (`encouraged` / `forced` / `disabled`), `emergencyOverride`. With `emergencyOverride` on it can bring its own CDN base (frontend reads `cdnBaseUrl`) and wins over empty flags. Read at boot (`stable target read emergency_override=false ... mode=Encouraged`), again by `check_for_launcher_update` (the manual "Check now"), exposed by `get_stable_target` and `stable-target-changed-event`. CDN failure keeps the last answer.

## Build info

For each CDN base the frontend builds:

```
{cdnBase}/{urlencode(targetVersion)}/{platformDir}/buildinfo.json
```

`platformDir`: `Windows` (`windows-x86_64`), `macOS` (`macos-aarch64`), `Linux/deb` or `Linux/appimage` (from `get_linux_install_flavor`).

URL: https://content-download-egs.distro.on.epicgames.com/Builds/EGLv2/0.95.2%2Bgfa9ad49/Windows/buildinfo.json \
Method: GET \
Auth Required: No

_Example Response_

```json
{
  "platforms": {
    "windows-x86_64": {
      "url": "https://content-download-egs.distro.on.epicgames.com/Builds/EGLv2/0.95.2%2Bgfa9ad49/Windows/EpicGamesLauncherSetup.exe",
      "signature": "dW50cnVzdGVkIGNvbW1lbnQ6..."
    }
  },
  "pub_date": "2026-10-14T14:43:55Z",
  "version": "0.95.2+gfa9ad49",
  "notes": "EGL v0.95.2+gfa9ad49"
}
```

Standard Tauri updater static JSON. `signature` is a base64 minisign signature over `EpicGamesLauncherSetup-<version>-windows-x86_64.exe`. The Rust side probes each manifest URL in order (`No matching update at this endpoint; trying next`, `Matching update found`).

## Flow

1. Boot: `self_update_boot_gate` waits for a running installer (`Global\EpicLauncherV2InstallerMutex`, marker `self-update-applied.json`, up to a timeout) before claiming the instance. `apply_pending_update_at_startup` installs a bundle that was downloaded earlier if it still matches the target and signature; otherwise it is deleted (`[self-update/startup] ...`). Dev builds and `EGL_DISABLE_SELF_UPDATE` / `-disable-self-update` skip all of this.
2. Flags hydrate (LaunchDarkly), the stable target is read, the frontend store computes a decision (`none`, encouraged, forced).
3. Download after the random hold: `download_update_only` (lazy, `{ targetVersion, manifestUrls, userInitiated, staffPatch }`) or `download_forced_only` (forced). The setup is staged on disk with its metadata (`get_pending_update_info`).
4. Install: `install_pending_update` (`{ expectedFlow }`) runs the NSIS setup quietly. During the swap `EpicGamesLauncherUpdate.exe` (copied to `update-splash\EpicGamesLauncherUpdate-<version>.exe`) shows a splash: args `--close-file`, `--ready-file`, `--show-file`, `--timeout-ms 120000`, `--idle-timeout-ms 300000`, `--message`. The launcher then relaunches (`relaunch_installed_app`).
5. `discard_pending_update` drops a stale bundle when the target moves.

Staff tools: `-patch-to-version=<version>` (+ `-patch-lazy`) and the EG Staff pane call `download_and_install_update` / start a lazy staff patch; `-self-update-dev` lets a local build hand off to an installed bundle.

## What's new

`fetch_whats_new` (`{ cdnBase, locale }`) reads `{cdnBase}/patch-notes/{locale}.json` (cdnBase must be https and on an allowed host; falls back to `en`). Shown when `whats-new-modal-enabled` is on.

URL: https://content-download-egs.distro.on.epicgames.com/Builds/EGLv2/patch-notes/en.json \
Method: GET \
Auth Required: No

```json
[
  {
    "version": "0.95.2",
    "date": "2026-10-14",
    "changes": [
      {
        "category": "fix",
        "title": "Sign-in",
        "description": "Fixed a bug that caused sign-in to fail after migrating from the old launcher."
      }
    ]
  }
]
```

Categories seen: `fix`, `enhancement`.

## v1 migration

The UE-based launcher ("v1") is detected (`detect_previous_launcher`) and imported on first run:

1. `run_v1_migration`: install scan of v1 item manifests and `LauncherInstalled.dat`, sign-in carry-over (see [V1 Carryover](Auth/V1Carryover.md)), play history (`ImportScan.V1PlayHistoryCarried`), Fab vault import (`fab_migration`), cloud save baselines. Runs once per session (`Previous-launcher migration already ran this session; replaying its report`).
2. `preview_v1_settings_migration` / `run_v1_settings_migration`: carry settings (`[<account>_Portal.SaveSync]` per-game cloud save switches, game settings).
3. Removal: `v1_uninstall_offer` -> `prepare_v1_removal` -> `run_v1_uninstall` spawns `EpicGamesLauncherMigrate.exe` (args `--close-v1 --relaunch` to close v1; `--v1-uninstall --await-pid <pid> --await-timeout-ms <ms> --result-file <path> --archive-dir <dir> --in-flight-mutex <name>` to remove it), guarded by `Local\com.epicgames.eglv2-v1-removal`. `decline_v1_uninstall` records a decline. The env vars `EGL_V1_UNINSTALL_FOR_REAL` and `EGL_V1_DISPOSAL` touch this path; their exact effect was not traced.
