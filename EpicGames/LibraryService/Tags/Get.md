## Library Service - Tags: Get

Localized store tag dictionary for one tag group. Library records carry tag ids in `tags`; this maps them to names for the genre / feature filters. Backs `get_store_tags` (cached in `store-tags-cache.json` per group + locale).

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/tags \
Method: GET \
Auth Required: Yes (`library:public:tags READ`)

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

Values are placeholders. Field names from `RawStoreTagsResponse`, `RawStoreTag` (7 fields) and `RawPagination`; the success body was not captured live.

A plain user token (tested with `launcherAppClient2`) is rejected:

_Example Response (403)_

```json
{
  "errorCode": "errors.com.epicgames.common.missing_permission",
  "errorMessage": "Sorry your login does not posses the permissions 'library:public:tags READ' needed to perform the requested operation",
  "messageVars": [
    "library:public:tags",
    "READ"
  ],
  "numericErrorCode": 1023,
  "originatingService": "library-service",
  "intent": "prod"
}
```

Library records already include tag `name` / `groupName` (see [Library Items](../Library/Items.md)).
