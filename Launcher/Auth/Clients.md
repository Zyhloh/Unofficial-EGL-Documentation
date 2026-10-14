# OAuth Clients

All ids and secrets below are compiled into `EpicGamesLauncher.exe` 0.95.1 as defaults. Each can be overridden by an environment variable at startup. The environment (`prod` vs `gamedev`/`ci`) picks the secret.

| Client | Client Id | Secret (prod) | Secret (gamedev / ci) | Used for |
|---|---|---|---|---|
| `egs-desktop` (SISU) | `c85f4c6238b04d3399bc0080e83b83fc` | `1371757d-23ee-4676-90cc-f6948e98b7ed` | `50ef2c17-52b8-425d-8194-b1dee709eb33` | Browser sign-in (PKCE), EAS to EG1 exchange, refresh of browser sessions |
| `launcherAppClient2` | `34a02cf8f4414e29b15921876da36f9a` | `daafbccc737745039dffe53d94fc76cf` | `5a71e767c4e24e119beb54574321ee77` | EOS SDK client, refresh of non-browser sessions, v1 carry-over |

The `egs-desktop` name comes from the error string `SISU browser login is not configured (no egs-desktop client yet)`. `launcherAppClient2` is the public name of `34a02cf8...` (same id and prod secret as the old launcher).

## Selection

`sub_1404E75B0(env, use_sisu)` returns the Basic-auth pair for token requests:

- `use_sisu = true`: the SISU config (`sub_1405611A0`)
- `use_sisu = false`: `34a02cf8f4414e29b15921876da36f9a` with the environment's secret

The refresh task passes a per-session flag; that it is the `via_system_browser` field stored in `auth.json` is inferred (it is the only boolean in `AuthEntry`). Sessions created by the browser flow therefore refresh with `egs-desktop`.

## SISU config

| Env var | Default |
|---|---|
| `EGL_SISU_CLIENT_ID` | `c85f4c6238b04d3399bc0080e83b83fc` |
| `EGL_SISU_CLIENT_SECRET` | see table |
| `EGL_SISU_SCOPES` | `basic_profile friends_list country presence` |
| `EGL_SISU_REDIRECT_HOST` | `127.0.0.1` |
| `EGL_SISU_REDIRECT_PORT` | unset (OS-assigned port) |
| `EGL_SISU_REDIRECT_PATH` | `/launcher/authorized` |
| `EGL_SISU_BROWSER_SINK` | unset (debug hook for where the authorize URL goes) |

Values that are empty or start with `REPLACE_WITH_` disable browser sign-in (`SISU browser login is not configured`).

## EOS platform config

| Env var | prod | gamedev / ci |
|---|---|---|
| `EGL_EOS_PRODUCT_ID` | `42c61cfdc3d24af5a8333b3284d47240` | `06dd02469db44fa4998bfdcc7ac75821` |
| `EGL_EOS_SANDBOX_ID` | `53221ede0f814ce2915a624137e4b5f1` | `ef1ade5a77464b0da09bc8c097af3d7f` |
| `EGL_EOS_DEPLOYMENT_ID` | `83364c64d38841d49c4de2f6f0eb3360` | `507f5a45b7604da799183e32fdf04b13` |
| `EGL_EOS_CLIENT_ID` | `34a02cf8f4414e29b15921876da36f9a` | `34a02cf8f4414e29b15921876da36f9a` |
| `EGL_EOS_CLIENT_SECRET` | `daafbccc737745039dffe53d94fc76cf` | `5a71e767c4e24e119beb54574321ee77` |
| `EGL_EOS_ENCRYPTION_KEY` | `1db6223f2a051367ac9e978a0473163f7d9591050de5171006d4a5babaf2ce7f` | `ff955acfe72862b011cc90819e1a792874956c640e998982d792f7f05e95f3cc` |
| `EGL_EOS_BACKEND_ENVIRONMENT` | unset | `GameDev` |

Field order is taken from `sub_140A9B660` (product, sandbox, deployment, client id, secret, encryption key) matched to the order the env vars are read in `sub_140DFDAD0`.

## Other

| Client | Where |
|---|---|
| IGDB / Twitch app (`EGL_IGDB_CLIENT_ID`, `EGL_IGDB_CLIENT_SECRET`) | `client_credentials` grant at `https://id.twitch.tv/oauth2/token`, used for external library metadata (`https://api.igdb.com/v4/games`). No default id in the binary. |
| Cloudflare Access (`egsZeroTrust` setting) | Staff only. Reads a `CF_Authorization` JWT for `epicgamesinc.cloudflareaccess.com` and injects it into the store webview (`EgsZeroTrustAction::ApplyToken`, `Store.EgsV2SignIn*`). Not an Epic OAuth client. |
