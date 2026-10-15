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

_Example Response_

```json
{
  "responseMetadata": {},
  "records": [
    {
      "sandbox": "5b325322a4c04b9e9e780b9a1e9b2d70",
      "catalogId": "9d60f0d4300a407e817ce5548f12f12d"
    },
    {
      "sandbox": "fn",
      "catalogId": "4fe75bbc5a674f4f9b356b5c90567da5"
    }
  ]
}
```

Each record is a `RawCollectionItem` (`sandbox` = namespace, `catalogId` = catalog item id). `responseMetadata` is empty when there is no further page; the client follows `responseMetadata.nextCursor` when present.
