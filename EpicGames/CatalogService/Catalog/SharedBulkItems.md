## Catalog Service - Catalog: Shared Bulk Items

Catalog metadata for a batch of catalog items across namespaces. Since launcher 0.115 the library refresh uses this route for all its catalog lookups (`fetch_catalog_batch`) instead of the per-namespace [Bulk Items](BulkItems.md).

URL: https://catalog-public-service-prod06.ol.epicgames.com/catalog/api/shared/bulk/items \
Method: GET \
Auth Required: Yes (Bearer access token)

## Query Parameters
`id`: Catalog item id, repeated once per item (the launcher sent batches of 1 to 10 ids) <br/>
`includeDLCDetails`: `false` in launcher 0.115 <br/>
`includeMainGameDetails`: `false` in launcher 0.115 <br/>
`country`: `US` <br/>
`locale`: UI locale, e.g. `en-US`

Request as logged by launcher 0.115:

```
GET /catalog/api/shared/bulk/items?id=<itemId>&id=<itemId>&includeDLCDetails=false&includeMainGameDetails=false&country=US&locale=en-US
```

---

Response: not captured yet. Expected to be the same object as [Bulk Items](BulkItems.md), keyed by catalog item id; to be confirmed with a live call.
