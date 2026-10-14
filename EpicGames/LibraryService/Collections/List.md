## Library Service - Collections: List

Lists the account's collection definitions. Backs `list_collections` (cached in `collections-cache.json`). The favorites list is the collection with id `EGS_STATIC_FAV_COLLECTION` (named `Favorites`).

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/collection/account/:accountId \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`accountId`: The account id

---

_Example Response (shape from client)_

```json
{
  "collections": [
    {
      "collectionId": "EGS_STATIC_FAV_COLLECTION",
      "name": "Favorites",
      "libraryItemContentVersion": 3
    },
    {
      "collectionId": "94b1569506b04f9f8557af611e8c5e47",
      "name": "Shooters",
      "libraryItemContentVersion": 1
    }
  ]
}
```

Values are placeholders. The URL is shared with [Create](Create.md) (same builder). GET is inferred: the list call goes through the client's GET helper and has no body type.
