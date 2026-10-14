# IPC - Games

Install, downloads, launch, cloud saves, install scan, v1 migration.

Args are the keys of the object the frontend passes to `invoke` (camelCase). Wrappers: `bindings-*.js` (`commands.*`).

## Install, update, uninstall

| Command | Args | Purpose |
| --- | --- | --- |
| `install_game` | `appId`, `installPath`, `selectedTags`, `operationId` | Start an install (`selectedTags` for selective download, `operationId` correlation) |
| `modify_install` | `appId`, `newTags` | Change selected components |
| `uninstall_game` | `appId` | Uninstall |
| `update_game` | `appId` | Update one game |
| `check_for_updates` | `appIds` | Check updates for apps |
| `trigger_update_check` | - | Run the periodic update check now |
| `set_retry_canceled_updates` | `enabled` | Setting: retry canceled updates |
| `get_manifest_info` | `appId`, `selectedTags` | Download / install size for a selection |
| `get_install_path_depth` | `appId`, `selectedTags` | Path depth check for the install folder |
| `prefetch_manifest` | `appId`, `hold` | Prefetch a manifest (`hold` keeps it) |
| `get_selective_download_info` | `appId` | Selective download components |
| `verify_game_files` | `appId` | Verify |
| `cancel_verify` | `appId` | Cancel verify |
| `resume_incomplete_install` | `appId` | Resume an interrupted install in place |
| `open_install_location` | `appId` | Reveal the install folder |
| `create_desktop_shortcut` | `appId`, `title` | Desktop shortcut (invoked directly, not in bindings) |
| `get_install_disk_sizes` | - | On-disk sizes |
| `refresh_install_disk_size` | `appId` | Re-measure one install |
| `get_install_state_health` | - | Installation records health |
| `get_disk_free_space` | `path` | Free space of a path |
| `get_disk_usage` | - | Per-volume usage |
| `check_install_location_writable` | `path` | Writable check |
| `get_build_label` | - | Build label override (staff) |
| `set_build_label` | `label` | Switch build label (staff) |

## Download queue

| Command | Args | Purpose |
| --- | --- | --- |
| `get_downloads` | `paused` | Active + queued rows (`paused` filter) |
| `get_download_queue_state` | - | Queue snapshot |
| `pause_download` | `appId` | Pause |
| `resume_download` | `appId` | Resume |
| `cancel_download` | `appId` | Cancel |
| `prioritize_download` | `appId` | Move to front |
| `deprioritize_download` | `appId` | Move back |
| `reorder_download` | `appId`, `targetIndex` | Move to index |
| `get_download_history` | `accountId` | History for an account |
| `archive_download_history` | `accountId`, `entries` | Archive entries |
| `clear_download_history` | `accountId` | Clear |
| `get_install_activity` | `accountId` | Install activity log |

## Launch

| Command | Args | Purpose |
| --- | --- | --- |
| `launch_game` | `appId`, `extraLaunchOptionId`, `source`, `catalogRefresh` | Launch (see [Game Launch](../Flows/GameLaunch.md)); `source`, `catalogRefresh`, optional extra launch option |
| `get_extra_launch_options` | `appId` | Catalog defined launch options |
| `preview_launch_args` | `appId` | Resolved command line preview |
| `get_game_settings` | `appId` | Per-game settings (args, cloud saves, ...) |
| `set_game_settings` | `appId`, `settings` | Save per-game settings |
| `open_fortnite_logs` | `appId` | Open the Fortnite log folder |
| `cabined_gate_acknowledge` | `appId` | Acknowledge the cabined account warning |
| `prefetch_exchange_code` | - | Warm the launch exchange code |
| `deeplink_take_pending` | - | Take a deep link received before the UI was ready |
| `deeplink_take_pending_uninstall` | - | Same for uninstall links |
| `deeplink_cancel_pending_launch` | `appId` | Cancel a deferred deep link launch |
| `install_proton_runtime` | `appId` | Linux: install Proton for an app |
| `cancel_proton_install` | - | Linux: cancel it |
| `get_linux_install_flavor` | - | Linux: `deb` / `appimage` |

## Cloud saves

| Command | Args | Purpose |
| --- | --- | --- |
| `cloud_save_state` | `appId` | Sync state of an app |
| `cloud_save_sync_now` | `appId` | Sync now |
| `cloud_save_resolve` | `appId`, `questionId`, `choice` | Answer a conflict question (`questionId`, `choice`) |
| `cloud_save_probe` | `appId` | Debug probe (list, sign, read manifests) |
| `cloud_save_debug_upload` | `appId` | Debug upload |
| `cloud_save_open_folder` | `appId` | Open the local save folder |
| `set_cloud_save_enabled` | `appId`, `enabled` | Per-game toggle |

## Install scan and v1 migration

| Command | Args | Purpose |
| --- | --- | --- |
| `start_install_scan` | `origin` | Scan disks for existing installs (`origin`) |
| `get_install_scan_state` | - | Scan state |
| `cancel_install_scan` | - | Cancel |
| `install_scan_has_completed` | - | Completed flag |
| `detect_previous_launcher` | - | Is the UE-based launcher installed |
| `run_v1_migration` | - | Import v1 installs, sign-in and settings (see [Self Update](../SelfUpdate.md#v1-migration)) |
| `preview_v1_settings_migration` | - | Preview which v1 settings will be applied |
| `run_v1_settings_migration` | - | Apply v1 settings |
| `v1_uninstall_offer` | `surface` | Should the v1 removal offer be shown on `surface` |
| `prepare_v1_removal` | - | Close v1 and prepare its removal |
| `run_v1_uninstall` | `surface` | Run v1 removal via `EpicGamesLauncherMigrate.exe` |
| `decline_v1_uninstall` | `exitRoute` | User declined (`exitRoute`) |
| `reveal_previous_launcher` | - | Reveal v1 install folder |
