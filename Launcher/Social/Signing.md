# Social Overlay - Chat Message Signing

Every chat message the overlay sends is signed client-side with a per-session Ed25519 key, and every received message is verified before display. Confirmed both ways: messages signed by a standalone client with this procedure are accepted by the Chat Service and shown in EGL, and messages sent from EGL verify with the procedure below.

## Key registration

1. On first send the app generates an Ed25519 key pair (`@noble/curves` `ed25519.keygen()`).
2. The raw 32-byte public key is base64 encoded (standard alphabet) and registered: [Register Public Key](../../EpicGames/PublicKeyService/PublicKey/Register.md) with body `{ "algorithm": "rsa", "key": "<base64>" }`. The overlay literally sends `rsa`; `ed25519` works the same.
3. The response contains `key`, `account_id`, `key_guid`, `kid`, `expiration`, `type` and `jwt`. Only `jwt` is kept, as the key certificate (`Pub`).

`jwt` decoded. The header holds only `alg` / `typ`; `kid` is in the payload:

```json
{
  "alg": "EdDSA",
  "typ": "JWT"
}
```

```json
{
  "account_id": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "generated": 1792001305,
  "key_guid": "6a7b8c9d-0e1f-4a2b-8c3d-4e5f6a7b8c9d",
  "kid": "20230621",
  "key": "<base64 raw 32 byte public key>",
  "expiration": "2026-12-13T18:08:25.097580678Z",
  "type": "legacy"
}
```

## Signing a message

1. Build the payload object. `rid` is the conversation id; it is omitted for the first DM, sent with [Send Direct Message](../../EpicGames/ChatService/Messages/SendDirectMessage.md) before any conversation exists:

```json
{
  "mid": "<sourceMsgId>",
  "sid": "<sender accountId>",
  "rid": "<conversationId>",
  "msg": "<text>",
  "tst": 1792001306956,
  "seq": 1,
  "rec": false,
  "mts": [],
  "cty": "Persistent"
}
```

2. `payload = base64(utf8(JSON.stringify(obj)))`: compact JSON (no spaces), keys in the order above, standard base64 with padding.
3. `signature = base64(ed25519.sign(utf8(payload + "\0"), privateKey))`.
4. The chat body becomes:

```json
{
  "message": { "body": "<payload>" },
  "metadata": { "Sig": "<signature>", "Pub": "<jwt>", "TmV": "2" }
}
```

5. `mid` is also passed as the `sourceMsgId` query parameter of [Send Direct Message](../../EpicGames/ChatService/Messages/SendDirectMessage.md) / [Send Message](../../EpicGames/ChatService/Messages/SendMessage.md).

Example decoded payload of a message sent from EGL:

```json
{"mid":"2f6e4d3c-7081-4c9d-aebf-2a3b4c5d6e7f","sid":"94b1569506b04f9f8557af611e8c5e47","rid":"GBD2ExampleConversationId00001","msg":"hello","tst":1792015544211,"seq":1,"rec":false,"mts":[],"cty":"Persistent"}
```

## Verifying a message

1. Split `metadata.Pub` (JWT), base64url decode header/payload. Reject if `payload.expiration` is in the past.
2. Fetch [Signing Keys](../../EpicGames/PublicKeyService/PublicKey/SigningKeys.md) once (cached) and pick the key whose `kid` matches the `kid` claim of the JWT payload; the key must be `crv: "Ed25519"` and its `x` is base64url.
3. Verify the JWT signature over `<header>.<payload>`.
4. JWT `account_id` must equal the message `senderId` (else `eos.social.jwt-does-not-match-sender`).
5. Decode the JWT `key` (base64) and verify `Sig` over `utf8(message.body + "\0")`.
6. Decode the body; its `sid` must equal `senderId`. The displayed text is `msg`.

The same `pl` / `sg` / `pk` triplet (payload, signature, JWT) is what gets uploaded to Emerald when a conversation is reported ([Upload Text](../../EpicGames/EmeraldService/Text/Upload.md)).
