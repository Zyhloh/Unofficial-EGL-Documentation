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
`nsCatalogItemId`: `{namespace}:{catalogItemId}` of the game (key name from the binary, value format inferred from the UE launcher)

---

_Example Response (shape from client)_

```json
{
  "token": "..."
}
```

Only `token` is read. Empty or missing means `launching without a token`.
