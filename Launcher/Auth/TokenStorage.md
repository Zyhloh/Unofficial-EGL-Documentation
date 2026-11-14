# Token Storage

`eglv2_lib::auth::credential_store` (`src\auth\credential_store.rs`). Everything is keyed by environment (`prod`, `gamedev`, `ci`).

Data dir: `%LOCALAPPDATA%\com.epicgames.eglv2` (a `run:roaming_migration` step moves older files from `%APPDATA%\com.epicgames.eglv2`).

## Refresh token: OS keyring

| | |
|---|---|
| Backend | `keyring` crate, Windows Credential Manager (generic credential) |
| Service | `com.epicgames.eglv2.<env>` (format `{}.{}`), e.g. `com.epicgames.eglv2.prod` |
| User | `credentials` |
| Payload | JSON `KeyringPayload`: `refresh_token`, plus optional `access_token`, `via_system_browser`, `written_at_ms`, `issued_at_ms` (5 fields in 0.115; 0.95 had 3) |

Malformed JSON is treated as no entry (`Auth.Credentials.KeyringPayloadCorrupt`). Sign-out deletes the entry; a delete failure is ignored.

A refresh token whose JWT carries `pfsid` (sandbox-scoped, issued by an old EOS login path) is refused on write and deleted on restore (`Auth.Credentials.SandboxTokenRefused`, issue #1623).

## auth.json

Path: `%LOCALAPPDATA%\com.epicgames.eglv2\auth\auth.json`. Map from environment name to `AuthEntry`:

| Field | Notes |
|---|---|
| `refresh_token` | Only on the plaintext fallback (no usable keyring; Linux without libsecret) or a legacy file awaiting migration |
| `access_token` | Legacy field |
| `account_info` | `CachedAccountInfo` |
| `via_system_browser` | true for sessions from the browser (SISU) flow |

`CachedAccountInfo` (8 fields in 0.115): `email`, `display_name`, `cached_at_ms`, `via_system_browser`, `country`, `cabined_mode`, `under_18`, `minor_status_read`. The last two are new for [Quiet Hours](QuietHours.md).

On start a refresh token found in `auth.json` is copied to the keyring and cleared from the file (`Auth.Credentials.LegacyTokenMigrated`). `EGLV2_FORCE_KEYRING` forces the keyring path. Writes are atomic (temp file + rename).

## Access token cache: DPAPI

`eglv2_lib::auth::credential_store::access_token_dpapi`. File name `access-token-<env>.dpapi` (format `access-token-{}.dpapi`), next to `auth.json` (directory inferred). Content is `CachedAccessToken` JSON encrypted with `CryptProtectData` (`dwFlags = 0`, i.e. current user; `pOptionalEntropy = NULL`).

`CachedAccessToken` (5 fields): `access_token`, `account_id`, `expires_at_ms`, `refresh_expires_at_ms`, `expires_in`.

Used by session restore as "Lever 2": if the cached token is still valid the launcher skips the token request and the account lookup (`Using cached account_info (skipping account API call)`). Deleted on sign-out (`Auth.Credentials.DpapiDeleted`).

## Retained accounts

Added in 0.115 for `auth_change_account` (`src\auth\credential_store\retained.rs`, events `Auth.RetainedAccounts.*`). Instead of deleting the outgoing account's tokens, the launcher keeps them (`Auth.ChangeAccountRetained`; `Auth.ChangeAccountTokensNotKept` when there is nothing to keep):

| File | Content |
|---|---|
| `auth\retained-accounts-<env>.json` | Index of kept accounts |
| `auth\retained-<env>-<accountId>.dpapi` | That account's tokens, DPAPI protected |

When a kept account signs in again its entry is removed. No IPC command or frontend code lists or restores kept accounts in 0.115, so there is no switch-back UI yet. Neither sign-out nor account change calls a revoke endpoint; the binary references no `/oauth/sessions/kill`.

## Isolated credentials

Added in 0.115: `-isolated-credentials` or `EGL_ISOLATED_CREDENTIALS` (any value except `0`, `no`, `off`). For that run the OS keyring and the CNG DPoP key are neither read, written nor cleared. Instead, under the data root:

| File | Content |
|---|---|
| `auth\auth.isolated.json` | The only credential store; the normal `auth.json` is never opened |
| `auth\dpop-key.isolated.pkcs8` | The only DPoP key: an ES256 key as a PKCS#8 document, minted on first use and stored owner-only (`Auth.DpopIsolatedKeyLoaded`) |

This lets a second session sign in with another account without touching the user's normal profile. If the write fails the key is regenerated on the next launch.

## In memory

`TokenResponse` (9 fields, see [OAuth/Token](../../EpicGames/AccountService/OAuth/Token.md)) lives in managed Tauri state. Exposed to:

- the shell UI: never the token, only `AuthState` (see [IPC](IPC.md))
- the Store / Fab / social webviews: `bridge_get_access_token`, `bridge_get_signed_in_user` (`EpicUser.accesstoken`)
- the EOS SDK: `EOS_Auth_SetAccessTokenOverride` (see [EOS](EOS.md))
- games: never directly, an exchange code instead (see [Game Launch](../Flows/GameLaunch.md))
