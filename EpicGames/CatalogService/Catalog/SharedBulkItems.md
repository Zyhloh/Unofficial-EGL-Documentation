## Catalog Service - Catalog: Shared Bulk Items

Catalog metadata for a batch of catalog items across namespaces. Since launcher 0.111 at the latest (somewhere between 0.96 and 0.111; older logs are gone) the library refresh uses this route for all its catalog lookups (`fetch_catalog_batch`) instead of the per-namespace [Bulk Items](BulkItems.md).

URL: https://catalog-public-service-prod06.ol.epicgames.com/catalog/api/shared/bulk/items \
Method: GET \
Auth Required: Yes (Bearer access token)

## Query Parameters
`id`: Catalog item id, repeated once per item. Launcher 0.115 dedupes the library's ids and sends the first 100 in batches of 10 (so the library fills in quickly), the rest in batches of 50 <br/>
`includeDLCDetails`: `false` in launcher 0.115 <br/>
`includeMainGameDetails`: `false` in launcher 0.115 <br/>
`country`: `US` <br/>
`locale`: UI locale, e.g. `en-US`

Request as logged by launcher 0.115:

```
GET /catalog/api/shared/bulk/items?id=<itemId>&id=<itemId>&includeDLCDetails=false&includeMainGameDetails=false&country=US&locale=en-US
```

---

_Example Response (shortened)_

```json
{
  "4fe75bbc5a674f4f9b356b5c90567da5": {
    "id": "4fe75bbc5a674f4f9b356b5c90567da5",
    "title": "Fortnite",
    "namespace": "fn",
    "status": "ACTIVE",
    "itemType": "DURABLE",
    "entitlementType": "EXECUTABLE",
    "entitlementName": "Fortnite",
    "developer": "Epic Games",
    "developerId": "o-aa83a0a9bc45e98c80c1b1c9d92e9e",
    "eulaIds": ["epicgames_tos"],
    "endOfSupport": false,
    "unsearchable": true,
    "keyImages": [
      {
        "type": "AndroidIcon",
        "url": "https://cdn1.epicgames.com/item/fn/FNBR_43-00_MSEE_Char-01_Crop_Android_AppIcon_512x512_512x512-99e377afc4b846b7a1e5fa1828fd1fe0",
        "md5": "664cc6ca91ea7cec6a6d689156d9651d",
        "width": 512,
        "height": 512,
        "size": 398310,
        "uploadedDate": "2026-10-27T19:25:51.520Z"
      }
    ],
    "categories": [{ "path": "games" }, { "path": "applications" }],
    "releaseInfo": [
      {
        "id": "6eec1fba0c494bb8bf157073483ffc4e",
        "appId": "Fortnite",
        "compatibleApps": [],
        "platform": ["Windows", "Mac", "Android"],
        "dateAdded": "2014-09-11T00:00:00.000Z"
      }
    ],
    "dlcItemList": [{ "id": "d75daf91c89b49ecb110b69a7bd68996", "namespace": "fn", "unsearchable": false }],
    "mainGameItemList": [],
    "ageGatings": {
      "PEGI": {
        "ratingSystem": "PEGI",
        "ageControl": 12,
        "gameRating": "PARENTAL GUIDANCE RECOMMENDED",
        "element": "Users Interact,In-Game Purchases (Includes Random Items)",
        "isIARC": false
      }
    }
  }
}
```

Same object as the namespaced [Bulk Items](BulkItems.md), keyed by catalog item id. With `includeDLCDetails=false` the `dlcItemList` entries are references only (`id`, `namespace`, `unsearchable`). Items from different namespaces can be mixed in one request (tested: Fortnite and Rocket League together), and items the account does not own are returned too.
