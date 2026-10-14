## Public Key Service - Public Key: Register Public Key

Registers an Ed25519 public key for the signed-in account and returns it as a signed JWT. Two users:

- Social overlay chat signing: per-session key on first send, `algorithm` sent as `rsa` ([Signing](../../../Launcher/Social/Signing.md)).
- Party voice moderation: the EOS SDK (`PublicKey::CreatePublicKeyV2`, `Moderation::GenerateKeys`) registers a key whose JWT is the `signed_public_key` of the signaling `join` ([Moderation](../../../Launcher/Voice/Moderation.md#voice-moderation-key)). A standalone client registering with `algorithm: "ed25519"` and a plain EG1 token gets a JWT that the media server accepts.

Both `rsa` and `ed25519` are accepted for an Ed25519 key.

URL: https://publickey-service-prod.ecbc.live.use1a.on.epicgames.com/publickey/v2/publickey/ \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>

## Body
```json
{
  "algorithm": "ed25519",
  "key": "KjiNzdIo9qri4fFyUm0u7zYV00jgNYjFxWgYkrdVH/w="
}
```

`key`: standard base64 of the raw 32-byte Ed25519 public key.

The SDK also has `POST /publickey/v2/so/` (`CreatePublicKeyV2SO`); it rejects an EG1 token (expects a different token type, not identified).

---

_Example Response_

```json
{
  "key": "KjiNzdIo9qri4fFyUm0u7zYV00jgNYjFxWgYkrdVH/w=",
  "account_id": "94b1569506b04f9f8557af611e8c5e47",
  "key_guid": "9f3c2a71-5e84-4b0d-a6c9-1d7e2f8b4a30",
  "kid": "20230621",
  "expiration": "2026-12-13T16:53:45.412484099Z",
  "jwt": "<jwt>",
  "type": "legacy"
}
```

The top-level fields repeat the JWT claims. Clients only need `jwt`.

`jwt` decoded:

```json
{
  "alg": "EdDSA",
  "typ": "JWT"
}
```

```json
{
  "account_id": "94b1569506b04f9f8557af611e8c5e47",
  "generated": 1791996825,
  "key_guid": "9f3c2a71-5e84-4b0d-a6c9-1d7e2f8b4a30",
  "kid": "20230621",
  "key": "KjiNzdIo9qri4fFyUm0u7zYV00jgNYjFxWgYkrdVH/w=",
  "expiration": "2026-12-13T16:53:45.412484099Z",
  "type": "legacy"
}
```

| Claim | Notes |
| --- | --- |
| `account_id` | owner; verifiers compare it with the sender |
| `generated` | unix seconds |
| `key_guid` | id of this registration |
| `kid` | signing key id, look it up in [Signing Keys](SigningKeys.md). It is in the payload, not the header |
| `key` | the registered public key, base64 |
| `expiration` | about two months after `generated` |
| `type` | `legacy` |

The JWT is signed (EdDSA over `header.payload`) by the Epic key with the matching `kid` from [Get Signing Keys](SigningKeys.md#verifying-a-key-jwt); verification confirmed live.
