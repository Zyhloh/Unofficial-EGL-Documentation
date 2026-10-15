## Library Service - Library: Items (v2)

Paginated list of every library record the account owns. Used by the library refresh (`get_library`, `get_library_full_bundle`, periodic / sign-in / focus refreshes). Pages are walked with `cursor` until `responseMetadata.nextCursor` is absent; the walk stops after 50 pages (5,000 records at the server's 100-record page cap) and returns a partial library. Duplicate records across pages are removed client-side.

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/v2/items \
Method: GET \
Auth Required: Yes (Bearer access token)

## Query Parameters
`includeMetadata`: Always `true` <br/>
`count`: Page size, always `500` (the server caps it at 100) <br/>
`includeCategories`: Repeated once per category, see table <br/>
`cursor`: `responseMetadata.nextCursor` of the previous page, omitted on the first page <br/>

| includeCategories |
| ----------------- |
| games             |
| software          |
| engines           |
| digitalextras     |
| mods              |
| addons            |
| subscription      |

Full first-page request as built by the client:

```
GET /library/api/public/v2/items?includeMetadata=true&count=500&includeCategories=games&includeCategories=software&includeCategories=engines&includeCategories=digitalextras&includeCategories=mods&includeCategories=addons&includeCategories=subscription
```

The server returns at most 100 records per page regardless of `count` (live: `count=500` returned 95 records and a `nextCursor` of `{"offset":100}`). `nextCursor` is base64 JSON, e.g. `eyJvZmZzZXQiOjEwMH0=` = `{"offset":100}`.

---

_Example Response_

Shortened to one record.

```json
{
  "responseMetadata": {
    "nextCursor": "eyJvZmZzZXQiOjEwMH0=",
    "stateToken": "3d9a6f1e-7b2c-4e8a-9f5d-1c2b3a4e5f60"
  },
  "records": [
    {
      "namespace": "5b325322a4c04b9e9e780b9a1e9b2d70",
      "catalogItemId": "9d60f0d4300a407e817ce5548f12f12d",
      "appName": "Grunt",
      "productId": "ca72a212479d4f658b053d06fa37330e",
      "sandboxName": "Aztez",
      "sandboxType": "PUBLIC",
      "recordType": "APPLICATION",
      "acquisitionDate": "2020-02-17T19:37:32.328Z",
      "dependencies": [],
      "tags": [
        {
          "id": "1216",
          "name": "Action",
          "groupName": "genre"
        },
        {
          "id": "1370",
          "name": "Single Player",
          "groupName": "feature"
        }
      ]
    }
  ]
}
```

| recordType   |
| ------------ |
| APPLICATION  |
| SUBSCRIPTION |

`tags` entries already carry the localized `name` and `groupName`. `productId` is a hex id or a slug (`prod-fn` for Fortnite). `stateToken` is a uuid; the last page's token is stored with the library cache and later checked with [State Token Status](../StateToken/Status.md). Full catalog data comes from [Catalog Bulk Items](../../CatalogService/Catalog/BulkItems.md).
