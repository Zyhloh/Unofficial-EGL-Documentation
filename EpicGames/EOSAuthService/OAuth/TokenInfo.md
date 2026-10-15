## EOS Auth Service - OAuth: Token Info (v2)

Checks whether an EOS Epic account token is still active. The EOS SDK repeats it while a session lives (`AuthClient.VerifyTokenInterval` = 60 in the platform config).

URL: https://api.epicgames.dev/epic/oauth/v2/tokenInfo \
Method: POST \
Auth Required: Yes (Basic Authentication where the username is the Client Id and the password is the Client Secret)

## Headers
`Content-Type`: application/x-www-form-urlencoded <br/>

## Body

`token`: The access token from [Epic Account Token](EpicToken.md)

---

_Example Response_

```json
{
  "active": true,
  "scope": "basic_profile friends_list country presence",
  "token_type": "bearer",
  "expires_in": 129599,
  "expires_at": "2026-10-17T00:33:23.211Z",
  "account_id": "94b1569506b04f9f8557af611e8c5e47",
  "client_id": "34a02cf8f4414e29b15921876da36f9a",
  "application_id": "fghi4567KEIkE93BQjKGjnyql0oI6X1a"
}
```

_Example Response (revoked or expired token)_

```json
{
  "active": false
}
```
