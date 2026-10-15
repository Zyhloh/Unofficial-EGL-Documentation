## Ecommerce Integration Service - Ownership Token: Create

Mints an ownership verification token for a game whose catalog custom attribute `OwnershipToken` is set. The launch flow (`eglv2_lib::ovt`, `src\api\ownership_token.rs`) writes the token to a `.ovt` file and hands the path to the game. See [Game Launch](../../../Launcher/Flows/GameLaunch.md).

URL: https://ecommerceintegration-public-service-ecomprod02.ol.epicgames.com/ecommerceintegration/api/public/platforms/EPIC/identities/:accountId/ownershipToken \
Method: POST \
Auth Required: Yes (Bearer access token)

## Headers
`Content-Type`: application/x-www-form-urlencoded <br/>

## Path Parameters
`accountId`: The account id

## Body
`nsCatalogItemId`: `{namespace}:{catalogItemId}` of the game

---

_Example Response_

```json
{
  "token": "egoc1~eyJraWQiOiJWbWdpMDFoQ2V2dXVEbUtWZFZubXphWnhpT2lBa0dEZWdRQmdDdWc4dkRZIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOi..."
}
```

The token is `egoc1~` followed by an RS512 JWT (`kid` `Vmgi01hCevuuDmKVdVnmzaZxiOiAkGDegQBgCug8vDY`). Decoded payload:

```json
{
  "sub": "<accountId>",
  "ip": "<caller ip>",
  "clid": "34a02cf8f4414e29b15921876da36f9a",
  "ent": [
    {
      "namespace": "e97659b501af4e3981d5430dad170911",
      "catalogItemId": "864c7bc2c2394f7dbd1b534aa068ff56",
      "owned": true
    }
  ],
  "exp": 1792033555,
  "iat": 1792033255,
  "jti": "a54701aa3ffd4477b9e6e085b86a72d3"
}
```

The token is valid for 5 minutes. An item the account does not own still returns 200 with `"owned": false` in `ent`. A request without `nsCatalogItemId` returns 500 `errors.com.epicgames.common.server_error`.

The launcher reads only `token`; empty or missing means `launching without a token`. It writes the token to `<installDir>\.egstore\<accountId>\<namespace><catalogItemId>.ovt` and passes the path as `-epicovt=<path>`. Only titles with the catalog custom attribute `OwnershipToken: "true"` get one (Hogwarts Legacy, Just Cause 4, Football Manager 2020).
