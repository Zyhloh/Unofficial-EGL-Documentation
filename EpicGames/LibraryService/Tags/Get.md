## Library Service - Tags: Get

Localized store tag dictionary for one tag group. Library records carry tag ids in `tags`; this maps them to names for the genre / feature filters. Backs `get_store_tags` (cached in `store-tags-cache.json` per group + locale).

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/tags \
Method: GET \
Auth Required: Yes (Bearer access token)

## Query Parameters
`groupName`: Tag group, see table <br/>
`locale`: UI language, e.g. `en` <br/>

| groupName (requested by the frontend) |
| ------------------------------------- |
| genre                                 |
| feature                               |
| epicfeature                           |

---

_Example Response (shape from client)_

```json
{
  "elements": [
    {
      "id": "1216",
      "name": "Action",
      "groupName": "genre",
      "namespace": "epic",
      "status": "ACTIVE",
      "referenceCount": 100,
      "aliases": []
    }
  ],
  "paging": {
    "count": 1,
    "total": 1
  }
}
```

Values are placeholders. Field names from `RawStoreTagsResponse`, `RawStoreTag` (7 fields) and `RawPagination`.
