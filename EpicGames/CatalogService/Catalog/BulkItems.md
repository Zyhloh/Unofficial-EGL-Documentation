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

_Example Response (shape from client)_

Object keyed by catalog item id (inferred: no wrapper struct exists for this response in the client; the items are stored keyed by id). Values are placeholders.

```json
{
  "4fe75bbc5a674f4f9b356b5c90567da5": {
    "id": "4fe75bbc5a674f4f9b356b5c90567da5",
    "namespace": "fn",
    "title": "Fortnite",
    "description": "",
    "longDescription": "",
    "technicalDetails": "",
    "keyImages": [
      {
        "type": "DieselGameBoxTall",
        "url": "https://cdn1.epicgames.com/offer/fn/Fortnite_GameBoxTall.jpg",
        "width": 1200,
        "height": 1600,
        "size": 123456,
        "md5": "94b1569506b04f9f8557af611e8c5e47"
      }
    ],
    "categories": [
      { "path": "games" },
      { "path": "applications" }
    ],
    "releaseInfo": [
      {
        "appId": "Fortnite",
        "platform": ["Windows", "Mac"],
        "compatibleApps": []
      }
    ],
    "mainGameItem": null,
    "customAttributes": {
      "CanRunOffline": { "type": "STRING", "value": "false" }
    },
    "dlcItemList": [
      { "id": "94b1569506b04f9f8557af611e8c5e47" }
    ],
    "developer": "Epic Games",
    "developerId": "94b1569506b04f9f8557af611e8c5e47",
    "eulaIds": [],
    "entitlementName": "Fortnite_Free",
    "entitlementType": "EXECUTABLE",
    "itemType": "DURABLE",
    "status": "ACTIVE"
  }
}
```

Field names from `RawCatalogItem` (19 fields), `RawKeyImage` (`type`, `url`, `width`, `height`, `size`, `md5`), `RawCategory` (`path`), `RawReleaseInfo` (`appId`, `platform`, `compatibleApps`), `RawMainGameRef`, `RawDlcRef` (`id`), `RawCustomAttribute` (`type`, `value`). The client only reads `customAttributes` by key (e.g. `AdditionalCommandLine`, matched case-insensitively). `mainGameItem` is non-null for DLC / add-ons and is how an add-on is linked to its parent game.

Key image `type` values the frontend looks for: `DieselGameBoxTall`, `DieselGameBox`, `DieselGameBoxWide`, `Thumbnail`, `OfferImageWide`, `DieselStoreFront`. See [Artwork](../../../Launcher/Library/Artwork.md).
