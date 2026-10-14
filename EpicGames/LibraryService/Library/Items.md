## Library Service - Library: Items (v2)

Paginated list of every library record the account owns. Used by the library refresh (`get_library`, `get_library_full_bundle`, periodic / sign-in / focus refreshes). Pages are walked with `cursor` until `responseMetadata.nextCursor` is absent; the walk stops after 50 pages (25,000 records) and returns a partial library. Duplicate records across pages are removed client-side.

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/v2/items \
Method: GET \
Auth Required: Yes (Bearer access token)

## Query Parameters
`includeMetadata`: Always `true` <br/>
`count`: Page size, always `500` <br/>
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

---

_Example Response (shape from client)_

Values are placeholders. `RawLibraryRecord` has 8 serde fields; 7 are named below, the 8th was not separated from neighbouring field-name runs (likely `namespace`, inferred from the 3-part app id the client builds from each record).

```json
{
  "records": [
    {
      "namespace": "fn",
      "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
      "appName": "Fortnite",
      "acquisitionDate": "2023-08-20T00:00:00.000Z",
      "recordType": "APPLICATION",
      "sandboxType": "PUBLIC",
      "tags": ["94b1569506b04f9f8557af611e8c5e47"],
      "catalogItem": {
        "title": "Fortnite",
        "keyImages": []
      }
    }
  ],
  "responseMetadata": {
    "nextCursor": "eyJ...",
    "stateToken": "94b1569506b04f9f8557af611e8c5e47"
  }
}
```

| recordType   |
| ------------ |
| APPLICATION  |
| SUBSCRIPTION |

`stateToken` (last page) is stored with the library cache and later checked with [State Token Status](../StateToken/Status.md). `catalogItem` is a partial catalog seed (title and key images at most); full catalog data comes from [Catalog Bulk Items](../../CatalogService/Catalog/BulkItems.md).
