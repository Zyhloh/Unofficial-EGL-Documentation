# Social Overlay - Chat Message Signing

Every chat message the overlay sends is signed client-side with a per-session Ed25519 key, and every received message is verified before display.

## Key registration

1. On first send the app generates an Ed25519 key pair (`@noble/curves` `ed25519.keygen()`).
2. The raw public key is base64 encoded and registered: [Register Public Key](../../EpicGames/PublicKeyService/PublicKey/Register.md) with body `{ "algorithm": "rsa", "key": "<base64>" }` (the `algorithm` value is literally `rsa`).
3. The response `jwt` is kept as the key certificate.

## Signing a message

1. Build the payload object:

```json
{
  "mid": "<sourceMsgId>",
  "sid": "<sender accountId>",
  "rid": "<conversationId>",
  "msg": "<text>",
  "tst": 1728900000000,
  "seq": 1,
  "rec": false,
  "mts": [],
  "cty": "Persistent"
}
```

2. `payload = base64(utf8(JSON.stringify(obj)))`.
3. `signature = base64(ed25519.sign(utf8(payload + "\0"), privateKey))`.
4. The chat body becomes:

```json
{
  "message": { "body": "<payload>" },
  "metadata": { "Sig": "<signature>", "Pub": "<jwt>", "TmV": "2" }
}
```

## Verifying a message

1. Split `metadata.Pub` (JWT), base64url decode header/payload. Reject if `payload.expiration` is in the past.
2. Fetch [Signing Keys](../../EpicGames/PublicKeyService/PublicKey/SigningKeys.md) once (cached) and pick the key whose `kid` matches the JWT's `kid`; the key must be `crv: "Ed25519"` and its `x` is base64url.
3. Verify the JWT signature over `<header>.<payload>`.
4. JWT `account_id` must equal the message `senderId` (else `eos.social.jwt-does-not-match-sender`).
5. Decode the JWT `key` (base64) and verify `Sig` over `utf8(message.body + "\0")`.
6. Decode the body; its `sid` must equal `senderId`. The displayed text is `msg`.

The same `pl` / `sg` / `pk` triplet (payload, signature, JWT) is what gets uploaded to Emerald when a conversation is reported ([Upload Text](../../EpicGames/EmeraldService/Text/Upload.md)).
