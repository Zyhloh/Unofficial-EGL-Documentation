# Sign In

eglv2 signs in through the system browser with OAuth 2.0 authorization code + PKCE ("SISU", `eglv2_lib::auth::sisu`) and a loopback redirect. There is no embedded login webview, no password grant and no custom URL scheme in the flow. The browser token is an EAS token; the launcher immediately trades it for an EG1 token, which is what every other service call uses.

Clients, ids and secrets: [Clients](../Auth/Clients.md). IPC: [Auth IPC](../Auth/IPC.md).

## Browser sign-in

Trigger: login screen calls `auth_sign_in_browser { pageStrings, createAccount }`. Task: `sub_1400DC690`.

1. Refuse if one is already running (`sign_in_already_in_progress`) or if the SISU client is not configured.
2. Generate PKCE `code_verifier` / `code_challenge` (S256) from the OS RNG (`OS RNG unavailable while generating PKCE material`) and a per-attempt `state`.
3. Bind a loopback listener on `127.0.0.1:0` (OS-assigned port, `EGL_SISU_REDIRECT_PORT` overrides). No IPv4 loopback: retry on `[::1]`. Errors: `loopback_port_unavailable`, `loopback_bind_denied`, `loopback_bind_failed`.
4. Open in the system browser (`Auth.Sisu.BrowserOpened`; the query itself is not logged). Query from the 0.115 binary:
   - sign in: [`https://www.epicgames.com/id/login`](../../EpicGames/Web/Id/Authorize.md)`?client_id=c85f4c6238b04d3399bc0080e83b83fc&response_type=code&redirect_uri=http://127.0.0.1:<port>/launcher/authorized&scopes=basic_profile friends_list country presence&code_challenge=<challenge>&code_challenge_method=S256&state=<state>&lang=<lang>&prompt=select_account` (0.95 used `/id/authorize`)
   - create account: [`https://www.epicgames.com/id/register`](../../EpicGames/Web/Id/Register.md) with the same query minus `prompt`
5. Wait for `GET /launcher/authorized?code=...&state=...` (or `error=access_denied`). The listener serves a static HTML result page built from `pageStrings`. Timeout: `Browser sign-in timed out`; `auth_cancel_browser_sign_in` aborts.
6. Redeem the code: [`POST /account/api/oauth/token`](../../EpicGames/AccountService/OAuth/Token.md), Basic `egs-desktop`, `grant_type=authorization_code&code=<code>&code_verifier=<verifier>&redirect_uri=<same>&token_type=eas` (`Exchanging PKCE authorization code for EAS tokens (SISU)`). DPoP proof attached when enabled ([DPoP](../Auth/DPoP.md)).
7. EAS to EG1 (`eas_for_eg1`): [`GET /account/api/oauth/exchange`](../../EpicGames/AccountService/OAuth/Exchange.md) with the EAS bearer and `consumingClientId`, then `POST /account/api/oauth/token` `grant_type=exchange_code&exchange_code=<code>&token_type=eg1`. The EAS and EG1 account ids must match (`EG1 account mismatch: EAS ... vs EG1 ...`).
8. Account check: [`GET /account/api/public/account/:accountId`](../../EpicGames/AccountService/Account/GetAccount.md). Reads `displayName`, `email`, `emailVerified`, `cabinedMode`.
9. Email gate (LaunchDarkly `login-email-gate-enabled`, `login-email-gate-allowed`): during the internal beta only accounts on allowlisted domains get in (`epicgames.com`, `xa.epicgames.com`, `3lateral.com`, `mediatonic.co.uk`, `psyonix.com` are in the binary). Denied: `INTERNAL_BETA_RESTRICTED`, `access-denied-event`.
10. Persist: refresh token to the keyring, access token to the DPAPI cache, account info + `via_system_browser: true` to `auth.json` ([Token Storage](../Auth/TokenStorage.md)).
11. Install the session (`Auth.SessionLifetime.Installed`), emit `auth-state-changed-event`, schedule refresh, start EOS login ([EOS](../Auth/EOS.md)) and the other session starters.

Live sign-in on launcher 0.115 with the browser already signed in to epicgames.com took 3.4 s from click to session (`User.AuthSignInCompleted duration_ms=3356`):

| Time | Event |
| ---- | ----- |
| +0 ms | `auth_sign_in_browser { createAccount: false }`, loopback listener bound on `127.0.0.1`, OS port (54135 in this run) |
| +35 ms | Browser opened, waiting for the callback |
| +2.5 s | Callback received; PKCE code redeemed for EAS tokens. DPoP proof 535 bytes, no nonce yet; the launcher then caches a 56-byte nonce from the response (`Auth.Dpop.NonceCached`) |
| +2.6 s | Exchange code minted with the EAS token |
| +3.0 s | Exchange code redeemed for EG1. DPoP proof 624 bytes, nonce attached. Token lifetime 129600 s (36 h) |
| +3.4 s | Account check, refresh token to the keyring, DPAPI access token cache, `auth.json`; session 2 installed; library refresh and EOS login start |

The EOS login that follows mints its own exchange code with `consumingClientId` = the EOS client (`EosClient.Login.ExchangeCodeMinting`).

The client used for step 7's token request is not logged. Indirect evidence that it is `egs-desktop`: the launcher's own calls to [Library Tags](../../EpicGames/LibraryService/Tags/Get.md) return 200 (`Store.TagsFetched`), and that route needs `library:public:tags READ`, which an `egs-desktop` token has and a `launcherAppClient2` token does not (403 `missing_permission`). Since browser sessions later refresh with the client selected by `via_system_browser`, the EG1 token is inferred to be issued to `egs-desktop` as well.

## Session restore (cold start)

`src\auth\session_restore.rs`, `auth:restore_begin`, `AuthState.authenticationStatus = restoring`.

1. Read the refresh token for the environment from the keyring (migrate from `auth.json` if found there). None: `unauthenticated`.
2. Sandbox-scoped (`pfsid`) token: delete and show sign-in (issue #1623).
3. "Lever 2": if the DPAPI access token cache is still valid, use it and the cached account info, skip the network.
4. Otherwise refresh (below), then the account check.
5. Restore is capped at 5 s (`Session restore timed out after 5 seconds`); timeouts and transient errors keep the token for the next start. A rejected credential deletes it.

## Refresh

`src\auth\refresh.rs`, scheduler `sub_1400C99F0`.

- Request: `POST /account/api/oauth/token` `grant_type=refresh_token&refresh_token=<token>&token_type=eg1`, Basic auth from `sub_1404E75B0` (`egs-desktop` for browser sessions, `launcherAppClient2` otherwise).
- Lead time: `min(expires_in / 2, 1800 s)` before `expires_at`. The timer sleeps at most 1500 s per arm and re-checks (`Auth.Refresh.RearmedStillFresh`), so laptop sleep does not skip it.
- Also on demand: any API call getting 401 refreshes once and retries (`Got 401, attempting token refresh`); `refresh_if_stale` before sensitive work; `auth_force_refresh`.
- Concurrent callers wait on the in-flight refresh (`Auth.Refresh.DedupWaiting`, capped).
- After refresh: account check again (401 signs out, transport failure keeps the session, malformed fails closed), email gate, cabined-mode update.
- Revoked / `TOKEN_NOT_FOUND`: sign out. Transient: exponential backoff, session and token retained.

## Sign out

`auth_sign_out` (`src\auth\sign_out.rs`, `session_lifetime.rs`). Stages: `before_credentials_clear`, `stop_publishers`, `close_transports`, `overlay_and_sdk` (EOS logout, DPoP unconfigure), then credentials are cleared: keyring entry deleted, `auth.json` entry removed, DPAPI cache deleted. Emits `auth:signed_out` / `Auth.SignedOut`.

Confirmed live on 0.115: sign-out sends no request to revoke the launcher's own EG1 session (no `sessions/kill` or revoke in the verbose log, which records every launcher request URL). Order seen: restore generation bumped, shell and store webview browsing data cleared, `Auth.SignedOut`, then `stop_publishers` (5 tasks), `close_transports` (1), `overlay_and_sdk` (EOS tear-down: overlay notifications cleared, social panel destroyed, `EOS_UI_HideFriends`, party analytics cleared, `EOS_Auth_Logout`). The only revoke is the EOS SDK's own, for its EOS token: `RevokeToken RevokeReason=Logout` ([Revoke](../../EpicGames/EOSAuthService/OAuth/Revoke.md)). The drain took 119 ms. Whether the old refresh token still works afterwards was not tested.

## Other entry points

- [v1 carry-over](../Auth/V1Carryover.md): first-run reuse of the old launcher's remembered refresh token.
- Store webview: gets `Authorization: Bearer <EG1>` on every store request (native WebView2 hook, `store-auth-injected-event`) and through `ue.launcher.getaccesstoken()` → `bridge_get_access_token`.
- `egsZeroTrust` setting: staff-only Cloudflare Access token for the store, see [Clients](../Auth/Clients.md#other).
