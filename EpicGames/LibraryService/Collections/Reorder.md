## Library Service - Collections: Reorder

Sets the display order of the account's collections. Backs `reorder_collections` (`orderedCollectionIds`).

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/collection/order/account/:accountId \
Method: PUT \
Auth Required: Yes (Bearer access token)

## Headers
`Content-Type`: application/json <br/>

## Path Parameters
`accountId`: The account id

## Body
```json
{
  "orderedCollectionIdList": [
    "EGS_STATIC_FAV_COLLECTION",
    "94b1569506b04f9f8557af611e8c5e47"
  ]
}
```
