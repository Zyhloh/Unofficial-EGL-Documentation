## Library Service - Collections: List Items

Members of one collection, cursor-paginated. Backs `list_collection_items` (cached per collection). The client follows `cursor` and stops after 200 pages (`Library.CollectionItemsPageCapReached`).

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/collection/:collectionId/item/account/:accountId \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`collectionId`: The collection id, `EGS_STATIC_FAV_COLLECTION` for favorites <br/>
`accountId`: The account id

## Query Parameters
`cursor`: Cursor of the previous page, omitted on the first page <br/>

---

_Example Response (shape from client)_

```json
{
  "items": [
    {
      "sandbox": "fn",
      "catalogId": "4fe75bbc5a674f4f9b356b5c90567da5"
    }
  ],
  "responseMetadata": {
    "nextCursor": "eyJ..."
  }
}
```

Each item is a `RawCollectionItem` (`sandbox` = namespace, `catalogId` = catalog item id). The envelope (`RawCollectionItemsPage`) field names were not separated in the binary; `items` / `responseMetadata.nextCursor` are inferred from the cursor handling and the library response shape.
