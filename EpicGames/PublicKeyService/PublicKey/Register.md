## Public Key Service - Public Key: Register Public Key

Registers the per-session Ed25519 chat signing key on first send. See [Signing](../../../Launcher/Social/Signing.md).

URL: https://publickey-service-prod.ecbc.live.use1a.on.epicgames.com/publickey/v2/publickey/ \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>

## Body
```json
{
  "algorithm": "rsa",
  "key": "<base64 raw 32 byte ed25519 public key>"
}
```

`algorithm` is sent as `rsa` even though the key is Ed25519.

---

_Example Response (shape from client; only `jwt` is read)_. JWT payload fields read: `account_id`, `key` (base64 public key), `kid`, `expiration`.

```json
{
  "jwt": "<header>.<payload>.<signature>"
}
```
