# Cabined Mode / Parental Controls

A cabined account is a restricted (age-gated) Epic account. eglv2 reads the flag from `cabinedMode` on [Get Account](../../EpicGames/AccountService/Account/GetAccount.md) and fails closed: a missing field, missing auth state or failed re-check counts as cabined.

Modules: `eglv2_lib::auth::cabined_mode` (`src\auth\cabined_mode.rs`), `eglv2_lib::auth::cabined_gate` (`src\auth\cabined_gate.rs`). Issue refs in strings: #1960, `REQ-CABIN-060`.

## Where the flag comes from

1. Sign-in / restore: account lookup after the token grant. Stored in `auth.json` `account_info.cabined_mode`.
2. Restore with cached account info: `Re-verifying cached cabined mode after restore` runs a fresh lookup.
3. Refresh: `Cabined mode changed on token refresh cabined_mode=` (`Auth.CabinedModeChanged`).
4. `auth_recheck_cabined_mode` (frontend, after the parental consent page): `Cabined-mode re-check: unchanged` / `Cabined mode changed on re-check`. A 401 leaves it to the refresh cycle; other failures keep the previous value.

Changes are pushed to the frontend as `cabined-mode-changed-event` (`CabinedModeChangedPayload { cabinedMode }`). `AuthState.cabinedMode` carries the current value.

## What it restricts

| Surface | Behaviour |
|---|---|
| Game launch | Blocked until acknowledged: `Launch of <app> requires the cabined-account restriction notice to be acknowledged`, event `cabined-launch-blocked-event` (`CabinedLaunchBlockedPayload`). Error code `cabined_blocked`. |
| Launch gate ack | `cabined_gate_acknowledge { appId }` then the launcher re-checks the account (timeout means still restricted) and replays the refused launch (`Cabined launch gate: acknowledged; replaying the refused launch`). If the account is no longer cabined the launch proceeds. |
| Catalog attribute `CanSkipCabinedWarning` | Read from the item's custom attributes; skips the notice (inferred from name) |
| Fab | `Fab surface refused: account is cabined` |
| Social overlay | `Account is cabined; skipping overlay notification registration`; overlay treats unknown auth as cabined |
| Store / bridges | `EpicUser.cabinedmode` passed to the Store webview |

`-simulate-cabined` (needs `-debugtools`) or `EGL_SIMULATE_CABINED` forces every restriction on for one run.

## Parental consent

`auth_open_parental_consent`:

1. Mint an exchange code ([OAuth/Exchange](../../EpicGames/AccountService/OAuth/Exchange.md)).
2. Open `https://www.epicgames.com/id/exchange?exchangeCode=<code>&redirectUrl=https://www.epicgames.com/account/parental-controls?lang=<lang>` in the system browser ([Id/Exchange](../../EpicGames/Web/Id/Exchange.md)).
3. No token or mint failure: open `https://www.epicgames.com/account/parental-controls?lang=<lang>` signed out.
4. The frontend arms a one-shot `window` `focus` listener; when the launcher regains focus it calls `auth_recheck_cabined_mode` (`Auth.Cabined.RecheckFailed` on error).

Gamedev uses `https://epicgames-gamedev.ol.epicgames.net/account/parental-controls`.
