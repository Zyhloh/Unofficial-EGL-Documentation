## Store Content Service - Content: Product

Store CMS document for a product slug. `get_store_product_art` builds `StoreProductArt` (`logoUrl`, `landscapeUrl`, `portraitUrl`, `media`, `releaseDate`, `videoUrl`, `landscapeHeroCopy`) from it. Trailers are media ref ids resolved with [Get Media Ref](../../../EpicGamesStore/GraphQL/GetMediaRef.md).

URL: https://store-content.ak.epicgames.com/api/:locale/content/products/:slug \
Method: GET \
Auth Required: No

## Headers
`Accept-Language`: UI locale <br/>

## Path Parameters
`locale`: e.g. `en-US` <br/>
`slug`: Product slug from [Product Mapping](ProductMapping.md), e.g. `fortnite`

---

A 404 is logged as `Store CMS has no page for slug`. The response is the full store CMS document; keys read by the client include `logoImage`, `backgroundImageUrl`, `portraitBackgroundImageUrl`, `video`, `releaseDate`, `developer`.
