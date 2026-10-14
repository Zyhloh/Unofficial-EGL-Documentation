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
`count`: Page size (value set at runtime, not a constant in the binary) <br/>

---

_Example Response (shape from client)_

```json
{
  "elements": [
    {
      "id": "94b1569506b04f9f8557af611e8c5e47",
      "title": "Fortnite",
      "offerType": "BASE_GAME",
      "releaseDate": "2017-07-25T13:00:00.000Z",
      "pcReleaseDate": "2017-07-25T13:00:00.000Z",
      "keyImages": [],
      "items": [
        { "id": "4fe75bbc5a674f4f9b356b5c90567da5" }
      ]
    }
  ],
  "paging": {
    "count": 1,
    "total": 1
  }
}
```

Values are placeholders. Field names from `RawOfferSearchResponse`, `RawSearchOffer` (`offerType`, `releaseDate`, `pcReleaseDate`), `RawOffer` (`title`, `keyImages`, `items`), `RawOfferItem` and `RawPagination`; the envelope names (`elements`, `paging`) are inferred from the shared `RawPagination` type.
