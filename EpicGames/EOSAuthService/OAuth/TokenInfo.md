## EOS Auth Service - OAuth: Token Info (v2)

Called by the EOS SDK (`FVerifyTokenTask`, route `TokenInfov2`) to check that the Epic account session is still active. The SDK config sets `AuthClient.VerifyTokenInterval` to `60`, so it is repeated while the launcher's EOS session lives (interval use inferred from the config key name). Not called by eglv2's Rust code.

URL: https://api.epicgames.dev/epic/oauth/v2/tokenInfo \
Method: POST \
Auth Required: Yes (set by the SDK task; type not resolved statically)

## Headers
`Content-Type`: application/x-www-form-urlencoded <br/>
`X-Epic-Correlation-ID`: random id <br/>
`X-Epic-Login-ID`: SDK login id, when set <br/>

## Body

| Field | Value |
|---|---|
| `token` | The access token to check |
| `token_type_hint` | Token type hint |

---

_Example Response (shape from client)_

```json
{
  "active": true,
  "scope": "basic_profile friends_list presence",
  "token_type": "bearer",
  "expires_in": 7199,
  "expires_at": "2026-10-14T18:00:00.000Z",
  "account_id": "94b1569506b04f9f8557af611e8c5e47",
  "client_id": "34a02cf8f4414e29b15921876da36f9a",
  "application_id": "..."
}
```

`active: true` with any of the other fields missing fails the task (`FVerifyTokenTask failed as the token is active but the required fields are not set`).
