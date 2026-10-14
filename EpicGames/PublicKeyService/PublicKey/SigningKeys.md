## Public Key Service - Public Key: Get Signing Keys

Keys that sign the public key JWTs. Fetched once and cached; used to verify every incoming chat message.

URL: https://publickey-service-prod.ecbc.live.use1a.on.epicgames.com/publickey/v2/publickey/signing \
Method: GET \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>

---

_Example Response (shape from client; JWK fields `kid`, `crv`, `x` are read)_

```json
{
  "keys": [
    { "kid": "...", "crv": "Ed25519", "x": "<base64url public key>" }
  ]
}
```
