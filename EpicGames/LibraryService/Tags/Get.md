## Library Service - Tags: Get

Localized store tag dictionary for one tag group. Library records carry tag ids in `tags`; this maps them to names for the genre / feature filters. Backs `get_store_tags` (cached in `store-tags-cache.json` per group + locale).

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/tags \
Method: GET \
Auth Required: Yes (`library:public:tags READ`; a user token of the `egs-desktop` client `c85f4c6238b04d3399bc0080e83b83fc` has it, a `launcherAppClient2` token does not)

## Query Parameters
`groupName`: Tag group, see table <br/>
`locale`: UI language, e.g. `en` <br/>

| groupName (requested by the frontend) |
| ------------------------------------- |
| genre                                 |
| feature                               |
| epicfeature                           |

---

_Example Response_

```json
{
  "elements": [
    {
      "id": "1216",
      "name": "Action",
      "groupName": "genre"
    },
    {
      "id": "1117",
      "name": "Adventure",
      "groupName": "genre"
    },
    {
      "id": "1367",
      "name": "RPG",
      "groupName": "genre"
    }
  ],
  "total": 38
}
```

Shortened. `total` is the number of tags in the group (live: `genre` 38, `feature` 11, `epicfeature` 2). `epicfeature` holds `Achievements` (`19847`) and `Cloud Saves` (`21894`).

A token without that permission (tested with a `launcherAppClient2` user token) is rejected. An `egs-desktop` user token (from an exchange code) is accepted. Rejected:

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
