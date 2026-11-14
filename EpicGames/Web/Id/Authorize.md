## Epic Games Id - Login (authorize)

OAuth 2.0 authorization code + PKCE page opened in the system browser by `auth_sign_in_browser` (`createAccount: false`). Built by `eglv2_lib::auth::sisu` (log: `Opening SISU authorize URL in system browser endpoint=`). See [Sign In](../../../Launcher/Flows/SignIn.md).

Launcher 0.115 opens `/id/login`; 0.95 opened `/id/authorize`. The 0.115 binary no longer contains `/id/authorize`.

URL: https://www.epicgames.com/id/login \
Method: GET (browser navigation) \
Auth Required: No

## Query Parameters

Appended in this order:

| Name | Value |
|---|---|
| `client_id` | `c85f4c6238b04d3399bc0080e83b83fc` (`EGL_SISU_CLIENT_ID` override) |
| `response_type` | `code` |
| `redirect_uri` | `http://127.0.0.1:<port>/launcher/authorized` (`http://[::1]:<port>/launcher/authorized` when no IPv4 loopback) |
| `scopes` | `basic_profile friends_list country presence` (`EGL_SISU_SCOPES` override). The key is plural in 0.115 |
| `code_challenge` | base64url(SHA-256(code_verifier)) |
| `code_challenge_method` | `S256` |
| `state` | Per-attempt value held next to the PKCE verifier; read back from the callback (comparison inferred) |
| `lang` | UI language, `_` replaced by `-`; omitted when empty |
| `prompt` | `select_account`; sent on sign-in only, omitted for [Register](Register.md) |

`<port>` is an OS-assigned ephemeral port unless `EGL_SISU_REDIRECT_PORT` is set (`EGL_SISU_REDIRECT_HOST` / `EGL_SISU_REDIRECT_PATH` override the rest of the redirect). PKCE material comes from the OS RNG (`OS RNG unavailable while generating PKCE material` on failure).

## Callback

The browser is redirected to the loopback listener (`src\auth\sisu\loopback.rs`):

```
http://127.0.0.1:<port>/launcher/authorized?code=<code>&state=<state>
http://127.0.0.1:<port>/launcher/authorized?error=access_denied&state=<state>
```

The listener reads `code`, `state` and `error`, answers with a small HTML page (`<title>Epic Games Launcher</title>`, heading/body from the `pageStrings` passed to `auth_sign_in_browser`) and closes. Requests without the expected fields are dropped (`Auth.Sisu.IncompleteRequestDropped`).
