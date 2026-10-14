# Token Storage

`eglv2_lib::auth::credential_store` (`src\auth\credential_store.rs`). Everything is keyed by environment (`prod`, `gamedev`, `ci`).

Data dir: `%LOCALAPPDATA%\com.epicgames.eglv2` (a `run:roaming_migration` step moves older files from `%APPDATA%\com.epicgames.eglv2`).

## Refresh token: OS keyring

| | |
|---|---|
| Backend | `keyring` crate, Windows Credential Manager (generic credential) |
| Service | `com.epicgames.eglv2.<env>` (format `{}.{}`), e.g. `com.epicgames.eglv2.prod` |
| User | `credentials` |
| Payload | JSON `KeyringPayload` (3 fields, one of them `refresh_token`) |

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

`CachedAccountInfo` (6 fields): `email`, `display_name`, `cached_at_ms`, `country`, `cabined_mode` + one shared name (account id, inferred).

On start a refresh token found in `auth.json` is copied to the keyring and cleared from the file (`Auth.Credentials.LegacyTokenMigrated`). `EGLV2_FORCE_KEYRING` forces the keyring path. Writes are atomic (temp file + rename).

## Access token cache: DPAPI

`eglv2_lib::auth::credential_store::access_token_dpapi`. File name `access-token-<env>.dpapi` (format `access-token-{}.dpapi`), next to `auth.json` (directory inferred). Content is `CachedAccessToken` JSON encrypted with `CryptProtectData` (`dwFlags = 0`, i.e. current user; `pOptionalEntropy = NULL`).

`CachedAccessToken` (5 fields): `access_token`, `account_id`, `expires_at_ms`, `refresh_expires_at_ms` + one more (not resolved).

Used by session restore as "Lever 2": if the cached token is still valid the launcher skips the token request and the account lookup (`Using cached account_info (skipping account API call)`). Deleted on sign-out (`Auth.Credentials.DpapiDeleted`).

## In memory

`TokenResponse` (9 fields, see [OAuth/Token](../../EpicGames/AccountService/OAuth/Token.md)) lives in managed Tauri state. Exposed to:

- the shell UI: never the token, only `AuthState` (see [IPC](IPC.md))
- the Store / Fab / social webviews: `bridge_get_access_token`, `bridge_get_signed_in_user` (`EpicUser.accesstoken`)
- the EOS SDK: `EOS_Auth_SetAccessTokenOverride` (see [EOS](EOS.md))
- games: never directly, an exchange code instead (see [Game Launch](../Flows/GameLaunch.md))
