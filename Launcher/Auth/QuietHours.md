# Quiet Hours

Added in 0.115. For accounts under 18 the launcher shows no toasts and plays no message chime between 22:00 and 06:00 local time. The flag registry calls it a legal requirement (`REQ-NOTIF-056`, #6720). Code: `eglv2_lib::quiet_hours` (`src\quiet_hours.rs`), frontend `hooks/useQuietHoursAccountSync.ts` and the notification store.

## Who it applies to

The [Get Account](../../EpicGames/AccountService/Account/GetAccount.md) response decides it, read on every token grant. The launcher reads `age` and `minorStatus`:

| `age` | `minorStatus` | Result |
|---|---|---|
| Number from 0 to under 18 | any | Minor: quiet hours apply |
| Number 18 or more | any | Not a minor |
| Missing or not a number | `NOT_MINOR` | Not a minor |
| Missing or not a number | anything else or missing | Unknown: quiet hours apply (`Account API response has no usable age or minorStatus - quiet hours apply (fail-closed)`) |

The result is cached as `under_18` / `minor_status_read` in `CachedAccountInfo` ([Token Storage](TokenStorage.md#authjson)) and exposed as `quietHoursApply` in `AuthState` ([IPC](IPC.md#authstate)).

The frontend reads `auth_get_state` whenever the signed-in account changes. Quiet hours apply when the account is not authenticated, the account id does not match, or `quietHoursApply` is true (`Auth.QuietHoursResolved`; `Auth.QuietHoursReadFailed` keeps them on). The signed-out default is `quietHoursApply: true`.

## What it does

The window is local time, hour >= 22 or hour < 6.

Toasts: the notification store picks one suppression reason in this order:

| Reason | When |
|---|---|
| `disabled` | Notifications are off in settings |
| `quiet-hours` | Quiet hours apply and the clock is in the window |
| `do-not-disturb` | OS do-not-disturb is on (`get_os_do_not_disturb`) |
| `silenced` | `suppressNotificationsWhileGaming` and a game is running |

A suppressed toast logs `Toast.Suppressed`. Toasts the user triggered (`userInitiated`) or with `quietTimeCategory: "FORCE_SEND"` are exempt. Toasts carry a category for telemetry, e.g. `GAME INVITE`, default `INFO`. While quiet hours apply, each non-social toast sends `Notification.QuietTimeToastResolved` with `result` (`suppressed` / shown), `reason` (`suppressed_by_policy` / `outside_quiet_time`), `toast_category` and `type`.

Chat chime: the social message chime is skipped too (`Social.Chime.QuietHoursSuppressed`, `social.chime.quiet_hours_suppressed chime=`).

## Kill switch

LaunchDarkly `quiet-hours-enabled`, boolean, default `true`. False lifts quiet hours for every account and stops the telemetry event. A missing flag reads as on. Changes are logged as `QuietHours.FlagChanged`.
