# IPC - App

Settings, environment, self update, windows, EULA, flags, telemetry.

Args are the keys of the object the frontend passes to `invoke` (camelCase). Wrappers: `bindings-*.js` (`commands.*`).

## Settings and environment

| Command | Args | Purpose |
| --- | --- | --- |
| `get_settings` | - | `settings/app-settings.json` |
| `patch_settings` | `patch` | Partial update |
| `get_environment_config` | - | `{ value, source }`, see [Environments](../Environments.md) |
| `set_environment` | `env` | Persist `prod` / `gamedev` / `ci` (relaunch follows) |
| `get_top_bar` | - | Top bar layout |
| `get_staff_eligibility` | - | Epic staff check |
| `set_minimize_to_tray` | `enabled` | Setting |
| `set_backend_locale` | `locale` | Locale for tray / backend strings |
| `get_launch_locale` | - | Locale from command line / OS |
| `clear_caches` | - | Clear caches |
| `get_cache_size` | - | Cache size |
| `open_logs_folder` | - | Open `logs` |
| `open_third_party_notices` | - | Open `ThirdPartyNotices.txt` |
| `open_windows_graphics_settings` | - | `ms-settings:display-advancedgraphics` |
| `open_url` | `url` | Open in the system browser |
| `open_account_link` | `link` | Open an account page, see [Deep Links](../DeepLinks.md#external-pages) |
| `get_platform_capabilities` | - | `{ platform, supportsPerfMonitor, buildPlatforms }` |
| `get_eos_sdk_version` | - | EOS SDK version string |

## Self update

| Command | Args | Purpose |
| --- | --- | --- |
| `get_release_channel` | - | `stable` / `stage` / `canary` / `manual` |
| `set_release_channel` | `channel` | Change channel |
| `get_stable_target` | - | `stable-target.json` answer |
| `check_for_launcher_update` | - | Manual check (re-reads the stable target) |
| `download_update_only` | `targetVersion`, `manifestUrls`, `userInitiated`, `staffPatch` | Lazy download of `targetVersion` from `manifestUrls` |
| `download_forced_only` | `targetVersion`, `manifestUrls`, `userInitiated` | Forced download |
| `download_and_install_update` | `targetVersion`, `manifestUrls` | Staff patch-to-version |
| `install_pending_update` | `expectedFlow` | Install the staged bundle (`expectedFlow`) |
| `discard_pending_update` | - | Delete the staged bundle |
| `get_pending_update_info` | - | Staged bundle metadata |
| `apply_pending_update_at_startup` | `expectedTargetVersion`, `expectedManifestUrls` | Apply at boot if it still matches |
| `get_self_update_dev_override` | - | `-self-update-dev` state |
| `take_launch_patch_version` | - | `-patch-to-version` value, once |
| `relaunch_installed_app` | - | Relaunch after install |
| `fetch_whats_new` | `cdnBase`, `locale` | Patch notes `{cdnBase}/patch-notes/{locale}.json` |
| `get_build_branch` | - | Build branch string |
| `get_applabel` | - | `-applabel` |

## Window, tray, shell

| Command | Args | Purpose |
| --- | --- | --- |
| `quit_app` | - | Quit |
| `relaunch` | - | Relaunch |
| `raise_shell` | - | Bring the shell to front |
| `is_tray_available` | - | Tray present |
| `update_tray_menu` | `games`, `authenticated` | Recent games + auth state for the tray menu |
| `get_window_geometry` | `label`, `minWidth`, `minHeight` | Saved geometry of a detached window |
| `set_window_snap_bounds` | `bounds` | Snap layout bounds |
| `apply_detached_window_chrome` | `label` | Rounded corners / snap styles for a detached window |
| `get_webview_browser_args` | - | WebView2 browser arguments for JS created webviews |
| `register_webview_label` | `label` | Label a JS created webview for the perf monitor |
| `set_layout` | `contentHole`, `socialHole`, `interactive`, `devicePixelRatio` | Content / social hole rects for the shell |
| `toast_harden_window` | - | Make `toast-window` non-activating |
| `toast_reposition` | `width`, `height` | Resize / move the toast window |
| `get_startup_info` | - | Startup timings |
| `record_frontend_startup_phase` | `phase`, `ms` | Phases: `html-loaded`, `js-parse`, `react-render`, `react-commit`, `fmp`, `landing-content`, `auth-restore-complete`, `library-data-loaded`, `first-grid-render` |
| `perf_monitor_set` | `enabled` | Perf overlay on / off |
| `perf_monitor_get_history` | - | Perf samples |

## EULA, flags, telemetry, feedback

| Command | Args | Purpose |
| --- | --- | --- |
| `accept_eula` | `promptId` | Accept the prompt from `eula-prompt-event` ([Accept](../../EpicGames/EulaTrackingService/Agreements/AcceptAgreement.md)) |
| `dismiss_eula` | `promptId` | Decline it |
| `get_feature_flags` | - | Current LaunchDarkly flag values |
| `get_flag_overrides` | - | Local `ld-overrides.json(c)` values |
| `log_emit` | `level`, `category`, `message`, `metadataJson`, `callSite` | Frontend log line into the Rust log / telemetry |
| `submit_feedback` | `input` | Send a feedback report |
| `get_feedback_history` | - | Sent reports |
| `debug_sentry_log` | `message` | Sentry debug line |
| `debug_sentry_test_mode` | - | `-sentry-test` mode |
| `debug_sentry_trigger_ipc_error` | - | Test IPC error |
| `mock_reset` | - | Mock backend reset (mock builds) |
