## Library Service - Collections: Remove Item

Removes a catalog item from a collection. Backs `set_collection_item` with `member: false`.

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/collection/:collectionId/item/account/:accountId/sandbox/:sandbox/catalog/:catalogId \
Method: DELETE \
Auth Required: Yes (Bearer access token)

## Path Parameters
`collectionId`: The collection id <br/>
`accountId`: The account id <br/>
`sandbox`: The item namespace (`AppId.namespaceId`) <br/>
`catalogId`: The catalog item id (`AppId.itemId`)
