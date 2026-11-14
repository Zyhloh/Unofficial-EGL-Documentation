## Library Service - Collections: Rename

Renames a custom collection. Backs `rename_collection`.

URL: https://distro-gateway-prod.ol.epicgames.com/library/api/public/collection/:collectionId/account/:accountId \
Method: PUT \
Auth Required: Yes (Bearer access token)

## Headers
`Content-Type`: application/json <br/>

## Path Parameters
`collectionId`: The collection id <br/>
`accountId`: The account id

## Body
```json
{
  "name": "New Name"
}
```
