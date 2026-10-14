# Auth IPC

Tauri commands and events of `eglv2_lib::commands::auth` (`src\commands\auth.rs`) and the bridge commands that hand auth data to webviews. Wrappers live in the frontend's `bindings-*.js`.

## Commands

| Command | Args | Returns | Notes |
|---|---|---|---|
| `auth_get_state` | - | `AuthState` | Polled on startup |
| `auth_has_cached_session` | - | `bool` | A refresh token exists for the current environment |
| `auth_sign_in_browser` | `pageStrings: BrowserPageStrings`, `createAccount: bool` | `AuthState` | Browser PKCE flow, see [Sign In](../Flows/SignIn.md). `A browser sign-in is already in progress` if repeated |
| `auth_cancel_browser_sign_in` | - | - | Aborts the loopback wait (`Browser sign-in was cancelled`) |
| `auth_force_refresh` | - | - | `auth_force_refresh: dev-triggered token refresh` |
| `auth_sign_out` | - | - | Full sign-out drain |
| `auth_recheck_cabined_mode` | - | - | See [Cabined Mode](CabinedMode.md) |
| `auth_open_parental_consent` | - | - | See [Cabined Mode](CabinedMode.md#parental-consent) |
| `cabined_gate_acknowledge` | `appId` | - | Unblocks a cabined launch |
| `prefetch_exchange_code` | - | - | Warm the launch exchange code, see [Game Launch](../Flows/GameLaunch.md) |
| `open_account_link` | `link` | - | See [Account Links](AccountLinks.md) |
| `open_partner_account_link` | `provider`, `pageStrings` | - | [Id/Link](../../EpicGames/Web/Id/Link.md) |
| `bridge_get_access_token` | - | `string` | EG1 access token for Store / Fab webviews (`ue.launcher.getaccesstoken()`) |
| `bridge_get_signed_in_user` | - | `EpicUser \| null` | `ue.common.getsignedinuser()` |

`BrowserPageStrings` (loopback result page): `lang`, `successHeading`, `successBody`, `errorHeading`, `errorBody`. The login screen fills them from `login.successTitle`, `login.successBody`, `login.errorTitle`, `login.errorBody`.

## AuthState

```json
{
  "authenticationStatus": "authenticated",
  "accountId": "94b1569506b04f9f8557af611e8c5e47",
  "displayName": "Player",
  "email": "player@example.com",
  "errorCode": null,
  "cabinedMode": false
}
```

| `authenticationStatus` | Meaning (doc comments in the binary) |
|---|---|
| `restoring` | Session restore is in progress; no result yet |
| `unauthenticated` | No valid session (restore found no credentials, or user signed out) |
| `authenticated` | Valid authenticated session |

`cabinedMode` is `true` on signed-out transitions (fail-closed).

## EpicUser (bridge)

Fields: `accesstoken`, `cabinedmode`, `country`, `displayname`, `email`, `externalauthtypes`, `lastname`, `name`, `offlinemode`, `region`, `userid`. `null` when signed out.

## Events

| Event | Payload |
|---|---|
| `auth-state-changed-event` | `AuthStateChangedPayload` (`authenticationStatus`, `accountId`, verified email for LaunchDarkly `identify()`, `cabinedMode`) |
| `cabined-mode-changed-event` | `{ cabinedMode }` |
| `cabined-launch-blocked-event` | `{ appId, ... }` |
| `access-denied-event` | `AccessDeniedPayload` (internal beta gate) |
| `store-auth-injected-event` | Store webview received the bearer |
| `partner-account-link-completed-event` | `{ provider }` |

## Sign-in failure reasons

Telemetry / error codes used by the browser flow: `network_transient`, `too_many_sessions`, `expired_token`, `unknown`, `loopback_port_unavailable`, `loopback_bind_denied`, `loopback_bind_failed`, `sign_in_already_in_progress`, `rate_limited`, `server_error`, `access_restricted`.

Session end causes: `user_cancelled`, `credential_rejected`, `refresh_transient`, `session_cap_reached`, `session_expired`, `unauthorized_after_refresh`, `unauthorized_without_refresh`, `forbidden`, `dpop`, `other`.
