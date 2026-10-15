## Library Service - Collections: List

Lists the account's collection definitions. Backs `list_collections` (cached in `collections-cache.json`). The favorites list is the collection with id `EGS_STATIC_FAV_COLLECTION` (named `Favorites`).

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/collection/account/:accountId \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`accountId`: The account id

---

_Example Response_

```json
{
  "collections": [
    {
      "collectionId": "EGS_STATIC_FAV_COLLECTION",
      "name": "Favorites",
      "libraryItemContentVersion": 5
    }
  ]
}
```

An account with no custom collections returns only the favorites collection. Custom collections use the same fields. The URL is shared with [Create](Create.md) (same builder).
