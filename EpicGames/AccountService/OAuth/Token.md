## Account Service - OAuth: Token

Token endpoint used by `src\auth\token_exchange.rs`. eglv2 sends three grants here: the PKCE code from the browser sign-in, the exchange code that turns an EAS token into an EG1 token, and refresh. See [Sign In](../../../Launcher/Flows/SignIn.md).

URL: https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token \
Method: POST \
Auth Required: Yes (Basic Authentication where the username is the Client Id and the password is the Client Secret)

## Headers
`Content-Type`: application/x-www-form-urlencoded <br/>
`Authorization`: Basic {base64(clientId:clientSecret)} <br/>
`DPoP`: ES256 proof JWT, only when DPoP is enabled (see [DPoP](../../../Launcher/Auth/DPoP.md)) <br/>

## Body

Fields are sent in the order below.

`authorization_code` (browser sign-in, client `egs-desktop`, log label `authorization_code_pkce`)

| Field | Value |
|---|---|
| `grant_type` | `authorization_code` |
| `code` | `code` from the loopback callback |
| `code_verifier` | PKCE verifier |
| `redirect_uri` | Same value sent to [/id/authorize](../../Web/Id/Authorize.md), `http://127.0.0.1:<port>/launcher/authorized` |
| `token_type` | `eas` |

`exchange_code` (EAS to EG1 step of sign-in, log label `eas_for_eg1`, also the v1 carry-over chain)

| Field | Value |
|---|---|
| `grant_type` | `exchange_code` |
| `exchange_code` | `code` from [OAuth/Exchange](Exchange.md) |
| `token_type` | `eg1` |

`refresh_token` (proactive refresh, 401 retry, session restore, v1 carry-over label `refresh_token_v1_carryover`)

| Field | Value |
|---|---|
| `grant_type` | `refresh_token` |
| `refresh_token` | Stored refresh token |
| `token_type` | `eg1` |

```
grant_type=refresh_token&refresh_token=<refresh_token>&token_type=eg1
```

## Errors handled

| Condition | Launcher behaviour |
|---|---|
| Refresh token invalid or revoked | `Auth.Refresh.TokenRevoked`, sign out (`token_revoked`) |
| `TOKEN_NOT_FOUND` | `Auth.Refresh.TokenNotFound`, sign out (`refresh_token_not_found`) |
| `use_dpop_nonce` + `DPoP-Nonce` response header | retry with the harvested nonce |
| `invalid_dpop_proof` | classified transient, session kept |
| Network / 5xx | retried with backoff, session and token retained |

---

_Example Response (shape from client, `struct TokenResponse with 9 elements`)_

```json
{
  "access_token": "eg1~...",
  "refresh_token": "eg1~...",
  "expires_in": 7200,
  "expires_at": "2026-10-14T14:00:00.000Z",
  "token_type": "bearer",
  "account_id": "94b1569506b04f9f8557af611e8c5e47",
  "displayName": "Player",
  "refresh_expires": 28800,
  "refresh_expires_at": "2026-10-14T20:00:00.000Z"
}
```

Values are placeholders; only the field names come from the binary.
