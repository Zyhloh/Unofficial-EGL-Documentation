## Catalog Service - Catalog: Namespace Offers

Offers in a namespace, used to find a product's release date for the store-art / detail view (cached as an "offer release-date" entry). A full page triggers a warning ("Offer page is full; a base game beyond it would not be seen").

URL: https://catalog-public-service-prod06.ol.epicgames.com/catalog/api/shared/namespace/:namespace/offers \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`namespace`: The catalog namespace

## Query Parameters
`country`: Always `US` <br/>
`locale`: UI locale <br/>
`returnItemDetails`: Always `false` <br/>
`count`: Page size, e.g. `10` <br/>

---

_Example Response_

Shortened to one offer; long text, key images and most store / pricing fields removed.

```json
{
  "metadata": {},
  "elements": [
    {
      "id": "8b620ab6eaad4c6182d44f07830fd8f6",
      "title": "Aztez",
      "description": "Aztez is a unique hybrid of beat 'em up and turn-based strategy, set in the world of the Aztec Empire. ...",
      "keyImages": [],
      "categories": [
        { "path": "games" },
        { "path": "games/edition/base" },
        { "path": "games/edition" },
        { "path": "applications" }
      ],
      "namespace": "5b325322a4c04b9e9e780b9a1e9b2d70",
      "status": "ACTIVE",
      "internalName": "Aztez",
      "items": [
        {
          "id": "fc5c077c77604e96ab1704acec3d542a",
          "keyImages": [],
          "categories": [],
          "namespace": "5b325322a4c04b9e9e780b9a1e9b2d70",
          "unsearchable": false
        }
      ],
      "currencyCode": "USD",
      "currentPrice": 1999,
      "seller": {
        "id": "o-ndzqj36dmhqmfklcq44yywpgfnbmbd",
        "name": "Team Colorblind"
      },
      "tags": [1216, 1344, 1370, 9549, 1263],
      "offerType": "BASE_GAME",
      "releaseDate": "2020-02-06T16:00:00.000Z",
      "urlSlug": "gruntgeneralaudience",
      "publisherDisplayName": "Team Colorblind",
      "developerDisplayName": "Team Colorblind",
      "supportedPlatforms": ["Windows", "macOS"]
    }
  ],
  "paging": {
    "count": 10,
    "start": 0,
    "total": 2
  }
}
```

The client reads `RawOfferSearchResponse`, `RawSearchOffer` (`offerType`, `releaseDate`, `pcReleaseDate`), `RawOffer` (`title`, `keyImages`, `items`), `RawOfferItem` and `RawPagination`. Non-base offers come back in the same list (e.g. `offerType` `OTHERS`); the client looks for the base game. `pcReleaseDate` was absent on the offers captured.
