# DPoP

eglv2 binds its tokens to a device key with OAuth DPoP (RFC 9449). Modules: `eglv2_lib::auth::dpop_nonce`, `dpop_nonce_gate`, `dpop_test_hooks`; token code in `src\auth\token_exchange.rs`.

## Key and proof

| | |
|---|---|
| Algorithm | `ES256` |
| Header | `DPoP: <proof JWT>` on token requests to [OAuth/Token](../../EpicGames/AccountService/OAuth/Token.md) |
| Thumbprint | `jkt`, logged on attach (`Attaching DPoP proof to token request jkt=`) |
| Clock | `iat` taken from a trusted clock (`src\auth\trusted_clock.rs`) anchored on server `Date` headers, with outlier screening |

If the signer cannot produce a proof the request goes out without the header (`DPoP enabled but proof unavailable; sending request without DPoP header`).

## Nonce

The account service may answer `use_dpop_nonce` with a `DPoP-Nonce` response header. The launcher stores the nonce and retries with it (`DPoP nonce challenge; retrying with the harvested nonce retries_left=`). A rejected nonce with no replacement is evicted and the request retried nonce-less. Non-convergence and `invalid_dpop_proof` are classified transient so the session is not torn down.

## EOS SDK

After sign-in the same key is handed to the SDK: `EOS_Auth_ConfigureDpop` with `algorithm=ES256` and a sign callback that must return base64url text (`EosClient.Dpop.*`). Done once per session; `EOS_Auth_UnconfigureDpop` on sign-out.

## Switches

| Switch | Effect |
|---|---|
| `-disable-dpop` / `EGL_DISABLE_DPOP` | DPoP off for the run |
| `-disable-dpop-nonce` / `EGL_DISABLE_DPOP_NONCE` | Nonce handling off |
| LaunchDarkly `dpop-nonce-enabled` | Server-side gate for nonce handling |
| `-dpop-iat-offset-seconds`, `-dpop-suppress-nonce-harvest`, `-dpop-seed-bad-nonce` | QA hooks (`App.CommandLine.DpopTestHookActive` / `...Rejected`; arming condition not resolved) |
