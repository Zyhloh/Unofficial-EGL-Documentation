# Hosts

This are some (not all) Hosts that you can access the Public Key Service from

- publickey-service-prod.ecbc.live.use1a.on.epicgames.com

<br/>

Recommended Hosts:

- publickey-service-prod.ecbc.live.use1a.on.epicgames.com

Called without `X-Epic-Agent` / `X-EPIC-CORRELATION-ID`. Plain EG1 bearer token from any client.

| Method | Path | Page |
| --- | --- | --- |
| POST | `/publickey/v2/publickey/` | [Register Public Key](PublicKey/Register.md) (chat signing and voice moderation) |
| GET | `/publickey/v2/publickey/signing` | [Get Signing Keys](PublicKey/SigningKeys.md) (verify key JWTs) |
| POST | `/publickey/v2/so/` | SDK route `CreatePublicKeyV2SO`; rejects EG1, not documented further |
