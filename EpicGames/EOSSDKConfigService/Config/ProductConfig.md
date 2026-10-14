## EOS SDK Config Service - Config: Product Config

Per-product overrides on top of [Platform Config](PlatformConfig.md). Fetched by the EOS SDK (`FSDKConfigProductUpdateTask`, route `GetProductConfigRoute`) after platform creation, with the launcher's product and deployment ids ([Clients](../../../Launcher/Auth/Clients.md#eos-platform-config)).

URL: https://api.epicgames.dev/sdk/v1/product/:productId \
Method: GET \
Auth Required: Yes (Bearer JWT; an unauthenticated request returns 401 `errors.com.epicgames.common.oauth.invalid_token` "Jwt is missing". Which SDK token is sent is not resolved statically)

## Headers
`X-Epic-Correlation-ID`: random id <br/>
`If-None-Match`: Value kept from the previous product config response, when present <br/>

## Path Parameters
`productId`: EOS product id, `42c61cfdc3d24af5a8333b3284d47240` for the prod launcher

## Query Parameters
`platformId`: SDK platform id, `WIN` on Windows (inferred) <br/>
`deploymentId`: EOS deployment id, `83364c64d38841d49c4de2f6f0eb3360` for the prod launcher <br/>

---

_Example Response (shape from client)_

```json
{
  "client": {},
  "services": {
    "EmeraldService": { "BaseUrl": "https://..." }
  },
  "watermark": 794601937
}
```

Only `client`, `services` and `watermark` are deserialized. The `EmeraldService` entry is inferred: it is missing from the platform config but the SDK needs it for [Emerald uploads](../../EmeraldService/SDK/SOInit.md). Needs a live capture.
