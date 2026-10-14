## Library Service - Collections: Rename

Renames a custom collection. Backs `rename_collection`.

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/collection/:collectionId/account/:accountId \
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
