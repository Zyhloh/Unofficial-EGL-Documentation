## Catalog Service - Catalog: Bulk Items

Catalog metadata for a batch of catalog items in one namespace. The library refresh groups library records by namespace and calls this per namespace (`fetch_catalog_batch`); `refresh_catalog_item`, `refresh_catalog_from_server`, the EULA gate and install-time lookups ("Fetched the uncached catalog entry of ...") use it too. Results are cached in `catalog-cache.json` (per locale; a cache in another language is treated as a miss).

URL: https://catalog-public-service-prod06.ol.epicgames.com/catalog/api/shared/namespace/:namespace/bulk/items \
Method: GET \
Auth Required: Yes (Bearer access token)

The URL is built by pushing `:namespace`, `bulk`, `items` as path segments onto `/catalog/api/shared/namespace`; a namespace containing `/`, `?` or `#` is rejected client-side ("Invalid catalog namespace").

## Path Parameters
`namespace`: The catalog namespace (sandbox id)

## Query Parameters
`id`: Catalog item id, repeated once per item <br/>
`includeDLCDetails`: Always `true` <br/>
`includeMainGameDetails`: Always `true` <br/>
`country`: Always `US` (hardcoded) <br/>
`locale`: UI locale <br/>

---

_Example Response_

Object keyed by catalog item id. Shortened to one key image and three custom attributes.

```json
{
  "9d60f0d4300a407e817ce5548f12f12d": {
    "id": "9d60f0d4300a407e817ce5548f12f12d",
    "title": "Aztez",
    "description": "Aztez",
    "keyImages": [
      {
        "type": "DieselGameBoxTall",
        "url": "https://cdn1.epicgames.com/5b325322a4c04b9e9e780b9a1e9b2d70/item/EGS_TeamColorblind_Aztez_S2-860x1148-0d2b32f59c7ce18bdb7f2c538c4cb3fa.jpg",
        "md5": "0d2b32f59c7ce18bdb7f2c538c4cb3fa",
        "width": 860,
        "height": 1148,
        "size": 192699,
        "uploadedDate": "2020-02-05T17:35:34.847Z"
      }
    ],
    "categories": [
      { "path": "public" },
      { "path": "games" },
      { "path": "applications" }
    ],
    "namespace": "5b325322a4c04b9e9e780b9a1e9b2d70",
    "status": "ACTIVE",
    "creationDate": "2019-12-05T20:51:43.793Z",
    "lastModifiedDate": "2020-02-06T15:11:50.571Z",
    "customAttributes": {
      "CanRunOffline": { "type": "STRING", "value": "true" },
      "PresenceId": { "type": "STRING", "value": "5b325322a4c04b9e9e780b9a1e9b2d70" },
      "FolderName": { "type": "STRING", "value": "Aztez" }
    },
    "entitlementName": "9d60f0d4300a407e817ce5548f12f12d",
    "entitlementType": "EXECUTABLE",
    "itemType": "DURABLE",
    "releaseInfo": [
      {
        "id": "f729c3179f6743c4b1924c46bad6e050",
        "appId": "Grunt",
        "platform": ["Windows", "Mac"],
        "dateAdded": "2020-02-05T17:36:36.008Z"
      }
    ],
    "developer": "Team Colorblind",
    "developerId": "o-ndzqj36dmhqmfklcq44yywpgfnbmbd",
    "eulaIds": ["egstore"],
    "endOfSupport": false,
    "mainGameItemList": [],
    "ageGatings": {},
    "selfRefundable": true,
    "unsearchable": false
  }
}
```

The client deserializes `RawCatalogItem` (19 fields), `RawKeyImage` (`type`, `url`, `width`, `height`, `size`, `md5`), `RawCategory` (`path`), `RawReleaseInfo` (`appId`, `platform`, `compatibleApps`), `RawMainGameRef`, `RawDlcRef` (`id`) and `RawCustomAttribute` (`type`, `value`); extra server fields (`uploadedDate`, `creationDate`, `endOfSupport`, `ageGatings`, ...) are ignored. The client only reads `customAttributes` by key (e.g. `AdditionalCommandLine`, matched case-insensitively). Other keys seen live: `MonitorPresence`, `UseAccessControl`, `RequirementsJson`, `CanSkipKoreanIdVerification`, `CloudSaveFolder`, `CloudSaveFolder_MAC`. Base games return `mainGameItemList: []`; the client's `mainGameItem` (DLC / add-on parent link) and `dlcItemList` were absent for the base games captured.

Key image `type` values the frontend looks for: `DieselGameBoxTall`, `DieselGameBox`, `DieselGameBoxWide`, `Thumbnail`, `OfferImageWide`, `DieselStoreFront`. See [Artwork](../../../Launcher/Library/Artwork.md).
