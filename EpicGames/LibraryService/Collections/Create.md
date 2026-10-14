## Library Service - Collections: Create

Creates a custom collection. Backs `create_collection`.

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/collection/account/:accountId \
Method: POST \
Auth Required: Yes (Bearer access token)

## Headers
`Content-Type`: application/json <br/>

## Path Parameters
`accountId`: The account id

## Body
```json
{
  "name": "Shooters"
}
```

---

_Example Response (shape from client)_

```json
{
  "collectionId": "94b1569506b04f9f8557af611e8c5e47",
  "name": "Shooters",
  "libraryItemContentVersion": 1
}
```

Response shape inferred from `RawCollectionDefinition` (the only collection definition type the client deserializes).
