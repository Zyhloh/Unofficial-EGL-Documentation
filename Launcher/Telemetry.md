# Telemetry

Events and log rows the launcher sends, as seen in its own spool (launcher 0.115, one normal session: start, sign-in, library refresh, update checks, Fortnite launch, a voice party). Sinks, endpoints and sampling flags are in [Architecture](Architecture.md#telemetry).

## Spool

Every event is written to `%LOCALAPPDATA%\com.epicgames.eglv2\telemetry\spool\seg-<wallMs>-<pid>-<seq>.jsonl` before it is sent (`spool.lock` guards the folder). Each line is one operation:

```json
{"op": "rec", "id": "<event uuid>", "env": "prod", "wallMs": 1794624367159, "lane": "events", "dests": {"dataRouter": {...}, "mixpanel": {...}}}
{"op": "ack", "id": "<event uuid>.log", "dest": "dataRouter"}
```

`rec` holds one copy of the event per sink (`dataRouter`, `mixpanel`, `eosDataRouter`); `ack` marks a copy as delivered. The folder also holds `session-running.marker`, `session-ever-ran.marker` and `in-flight\` (used to report the previous exit as clean or not, `prior_exit`).

Event copy:

```json
{
  "kind": "event",
  "name": "User.AppOpened",
  "eventId": "03a892b5-cb72-40f4-aa3a-4b51b25292e0",
  "distinctId": "$device:<device id>",
  "accountId": null,
  "deviceId": "<device id>",
  "wallMs": 1794624367159,
  "monotonicMs": 45,
  "props": {
    "cold_start_ms": 49,
    "is_first_session": false,
    "open_type": "cold_start",
    "prior_exit": "clean",
    "v1_detected": false,
    "v1_migrated": false,
    "sample_rate": 1.0,
    "schema_version": 6,
    "...": "common props"
  }
}
```

Mixpanel copies use the bare device id as `distinctId`. Log rows (`Launcher.Log`, Data Router only) have `kind: "log"` with `level`, `category`, `origin`, `callSite`, `frames`, `metadata`, `envelope`, `sampleRate`.

Common props on every event: `environment`, `event_id`, `launcher_version`, `os`, `release_channel`, `release_type`, `schema_version` (6), `session_id`, `session_time_ms`, `wall_ms`. Most also carry `device_id`, `account_id` once signed in, and `sample_rate`.

## Events seen

| Event | Sinks | Own props |
| --- | --- | --- |
| `User.AppOpened` | Data Router, Mixpanel | `cold_start_ms`, `is_first_session`, `open_type`, `prior_exit`, `v1_detected`, `v1_migrated` |
| `User.AppMinimized` | Data Router, Mixpanel | `target` |
| `User.TabVisited` | Data Router, Mixpanel | `tab` |
| `User.AuthSignInStarted` | Data Router, Mixpanel | `create_account`, `method`, `sign_in_attempt_id`, `surface` |
| `User.AuthSignInCompleted` | Data Router, Mixpanel | `duration_ms`, `is_session_restore`, `method`, `result`, `sign_in_attempt_id`, `surface` |
| `User.AuthSignOut` | Data Router, Mixpanel | `cause`, `type` |
| `Auth.SignInSurfaceShown` | Data Router, Mixpanel | `surface` |
| `User.GameLaunchCompleted` | Data Router, Mixpanel | `app_name`, `item_id`, `namespace_id`, `launch_attempt_id`, `launch_ms`, `blocker_in_flight`, `install_blocker`, `catalog_refresh`, `not_found_kind`, `os_error_code`, `ovt_result`, `ovt_error_kind` |
| `User.GameEnded` | Data Router, Mixpanel | `app_name`, `item_id`, `namespace_id`, `launch_attempt_id`, `session_duration_ms`, `exit_code`, `early_exit`, `result` |
| `Library.Refreshed` | Data Router, Mixpanel | `duration_ms`, `forced`, `item_count`, `result`, `trigger` |
| `UpdateCheck.Completed` | Data Router, Mixpanel | `duration_ms`, `error_code`, `failure_count`, `game_count`, `update_count`, `result`, `trigger` |
| `Library.InstalledSnapshot` | Data Router | `installed_count`, `dlc_count`, `fab_asset_count`, `incomplete_count`, `selective_download_count`, `load_health` |
| `App.Heartbeat` | Data Router | `action`, `app_running`, `app_version`, `library_count`, `location`, `status` (every `telemetry-heartbeat-interval-secs`) |
| `Startup.Completed` | Data Router | `cold_start_ms`, `fmp_ms`, `js_parse_ms`, `react_render_ms`, `landing_view`, `timed_out` |
| `System.Specs` | Data Router | `app_format`, `arch`, `cpu_brand`, `cpu_cores`, `gpu_name`, `gpu_vendor`, `gpu_vram_mb`, `disk_kind`, `disk_free_gb`, `disk_total_gb`, `locale`, `os_version`, `primary_display_resolution` |
| `Settings.Snapshot` | Data Router | `default_install_dir`, `download_speed_limit`, `download_speed_limit_gameplay`, `download_speed_unit`, `enable_notifications`, `language`, `minimize_to_tray`, `perf_preset`, `show_build_badges`, `show_whats_new_on_startup`, `startup_location` |
| `Playtime.Published` | Data Router | `segment_count`, `oldest_segment_age_secs`, `result`, `error_code` |
| `Account.TimezoneReported` | Data Router | `duration_ms`, `result` (the [K3S time zone report](../EpicGames/KWS/Settings/UpdateUser.md)) |
| `eos.social.party-leave` | EOS Data Router | `AccountId`, `RoomName`, `Source`, `DisconnectReason`, `AvgJitterBufferDelaySec`, `AvgRoundTripTimeSec`, `IncomingAvgPacketLossFraction`, `OutgoingAvgPacketLossFraction`, `VoiceChatIncomingActivitySec`, `VoiceChatOutgoingActivitySec`, `VoiceModerationEnabled`, `VoiceModerationEnabledDurationSec` |

The binary has more event groups that this session did not trigger (source files `telemetry\{download,install,cloud_save,eula,fab,store,selfupdate,update_check,v1_removal,previous_launcher,social}_events.rs`).
