## EOS Auth Service - OAuth: Token (v1)

EOS client token (no user). It is the token the [Product Config](../../EOSSDKConfigService/Config/ProductConfig.md) accepts. The launcher's own Rust code has the URL in its environment table but no request to it was seen; the EOS SDK uses the same route for client tokens.

URL: https://api.epicgames.dev/auth/v1/oauth/token \
Method: POST \
Auth Required: Yes (Basic Authentication where the username is the Client Id and the password is the Client Secret)

## Headers
`Content-Type`: application/x-www-form-urlencoded <br/>

## Body

`grant_type`: `client_credentials` <br/>
`deployment_id`: EOS deployment, `83364c64d38841d49c4de2f6f0eb3360` for the launcher

---

_Example Response_

```json
{
  "access_token": "eyJraWQiOiIyMDIyLTA2...",
  "token_type": "bearer",
  "expires_at": "2026-10-15T13:33:23.648Z",
  "features": [],
  "organization_id": "o-aa83a0a9bc45e98c80c1b1c9d92e9e",
  "product_id": "42c61cfdc3d24af5a8333b3284d47240",
  "sandbox_id": "53221ede0f814ce2915a624137e4b5f1",
  "deployment_id": "83364c64d38841d49c4de2f6f0eb3360",
  "expires_in": 3599
}
```

Valid for one hour. The response tells which organization, product and sandbox the client and deployment belong to.
