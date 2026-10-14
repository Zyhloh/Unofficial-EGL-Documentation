## EOS Auth Service - OAuth: Public Keys (v2)

JWKS for Epic account tokens. Fetched by the EOS SDK (`RequestPublicKeysTask`, route `FetchPublicKeysv2`) to check Epic account JWTs locally (`EOS_Auth_VerifyIdToken`, key cache `IdTokenCacheMinExpirySeconds`). The SDK reads the `Date` response header for clock skew (`JWKS endpoint did not return server date, using local system time`). Whether eglv2's flow ever triggers it is not confirmed.

URL: https://api.epicgames.dev/epic/oauth/v2/.well-known/jwks.json \
Method: GET \
Auth Required: No

## Headers
`X-Epic-Correlation-ID`: random id <br/>

---

_Example Response_

```json
{
  "keys": [
    {
      "kty": "RSA",
      "e": "AQAB",
      "kid": "WMS7EnkIGpcH9DGZsv2WcY9xsuFnZCtxZjj4Ahb-_8E",
      "alg": "RS256",
      "n": "l6XI48ujknQQlsJgpGXg4l2i_DuUxuG2GXTzkOG7UtX4MqkVBCfW1t1JIIc8q0kC..."
    }
  ]
}
```

The SDK deserializer reads `kty`, `e`, `use`, `kid` and more per key; keys with an empty `kid` are rejected (`FRequestPublicKeysTask received a jwk with an empty kid`).
