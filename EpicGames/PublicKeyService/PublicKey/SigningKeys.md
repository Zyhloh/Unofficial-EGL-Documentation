## Public Key Service - Public Key: Get Signing Keys

Keys that sign the public key JWTs returned by [Register Public Key](Register.md). Fetched once and cached by the overlay; used to verify every incoming chat message. A voice client can use the same keys to verify a peer's `signed_public_key` from signaling `user_joined`.

URL: https://publickey-service-prod.ecbc.live.use1a.on.epicgames.com/publickey/v2/publickey/signing \
Method: GET \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>

---

_Example Response_

```json
{
  "keys": [
    {
      "crv": "P-256",
      "kid": "1",
      "kty": "EC",
      "x": "Z1wgnXPU2cGuQ7gmt8ErapzyH4iFOcq6zgM1I5hnT9Y",
      "y": "7Ckc161-P7jkbMtSjToMXrR-3s-O450w_W899513d34"
    },
    {
      "crv": "Ed25519",
      "kid": "20230621",
      "kty": "OKP",
      "x": "zsas3J1p4mt_5V6LdnA1BEqwvFtvG9nYtERMVOEfLoc"
    }
  ]
}
```

These are Epic's public signing keys (JWK, `x` / `y` base64url). Every key JWT seen so far (chat and voice) used `kid` `20230621`, the Ed25519 key.

## Verifying a key JWT

The JWT header carries no `kid`, only `{"alg":"EdDSA","typ":"JWT"}`. The `kid` is a payload claim.

1. Split the JWT into `header.payload.signature` and base64url-decode the payload.
2. Pick the key from this response whose `kid` equals the payload `kid`.
3. Verify the Ed25519 signature (base64url-decoded third part) over the ASCII bytes `header.payload` with the key's `x` (raw 32 bytes after base64url decoding).
4. Check `expiration` and that `account_id` matches the sender (for voice: the `user_token` of the `user_joined`).

Confirmed live (2026-10-14): the JWT from a fresh [Register Public Key](Register.md) verified against `kid` `20230621`. The verified `key` claim is the public key that checks the peer's [audio signatures](../../../Launcher/Voice/AudioSigning.md#receiving).
