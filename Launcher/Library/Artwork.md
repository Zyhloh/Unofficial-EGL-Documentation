# Library Artwork

## Key image types

Covers come from catalog `keyImages` (`type`, `url`, `width`, `height`, `size`, `md5`, plus client-side `localUrl` and `heroCopy`).

| Use | Preference order (first match wins, else first image) |
| --- | ---------------------------------------------------- |
| Grid cover / detail cover | `DieselGameBoxTall`, `DieselGameBox`, `DieselGameBoxWide`, `Thumbnail` |
| Wide art (list view / hero fallback) | `DieselGameBoxWide`, `OfferImageWide`, `DieselStoreFront`, `DieselGameBox`, `DieselGameBoxTall`, `Thumbnail` |

The frontend uses `localUrl` (downsampled local copy) when present, else the CDN `url`. If the local copy fails to load it falls back to the CDN URL, then to the original URL.

## Image cache

- Before the catalog crosses IPC, `image_cache::decorate_catalog_items` sets `localUrl` on images already on disk.
- Covers are downloaded by a background worker (`src\image_cache\worker.rs`, priority and cold tiers, 8 connections by default). The image CDN resizes on request: covers are fetched with `?resize=1&w=600&h=800&quality=medium`, detail heroes with `?resize=1&w=1920&quality=medium` (a 1200x1600 2.2 MB PNG cover comes back as a 26 KB JPEG). URLs that already carry these parameters are left alone. If the resized fetch fails the original URL is fetched (`Images.ResizedFetchFellBack`).
- `EGL_IMAGE_CDN_RESIZE=0` / `false` / `off` disables resizing. `EGL_IMAGE_FETCH_CONNECTIONS` sets parallelism (default 8, clamped to 1..64).
- Only https images on `epicgames.com`, `epicgames.net` and `unrealengine.com` hosts are fetched.
- Covers are stored as `images\<md5>.jpg` (catalog key image `md5`, SHA-1 of the URL when missing) with an `_index.json`, and served to the frontend as `http://img.localhost/<md5>` (`Cache-Control: public, max-age=31536000, immutable`). Old files are evicted at startup by total size.
- When an image lands, `image-cached-event` tells the frontend to swap the CDN URL for the local one in place.
- `set_priority_covers { items }` moves visible covers to the front of the queue; `recache_cover { cdnUrl, md5 }` forces one cover to be fetched again.

## Hero art

- `get_hero` / `prefetch_hero { hero }` and `cache_detail_hero { sourceUrl }` keep detail-pane hero images in a separate hero cache (`HeroInfo`: `localUrl`, `palette`); the palette is computed from the image and is empty when that fails. `heroCopy` on the catalog landscape image points at that copy.
- `get_store_product_art { namespace }` returns `StoreProductArt` (`slug`, `logoUrl`, `landscapeUrl`, `portraitUrl`, `media`, `releaseDate`, `videoUrl`, `landscapeHeroCopy`). It maps the namespace to a store slug (cached in `product-mapping-cache.json`), reads the store CMS product page (cached in `product-art-cache.json`, misses cached as negative entries) and the release date from [Catalog Namespace Offers](../../EpicGames/CatalogService/Catalog/Offers.md). The CMS calls are [Product Mapping](../../EpicGames/StoreContentService/Content/ProductMapping.md) (`namespace` -> slug) and [Product](../../EpicGames/StoreContentService/Content/Product.md) (`pages[].data.hero`: `logoImage.src` -> `logoUrl`, `backgroundImageUrl` -> `landscapeUrl`, `portraitBackgroundImageUrl` -> `portraitUrl`, carousel images -> `media`). Cache keys are `<locale>:<slug>`; a namespace without a slug is cached as `<locale>:ns:<namespace>` with every URL `null`, and the library falls back to the catalog key images. Entries live 24 hours, negative entries 7 days.
- Trailers are media refs resolved with `POST https://store.epicgames.com/graphql` `query getVideo($mediaRefId: String!) { Media { getMediaRef(mediaRefId: $mediaRefId) { outputs { url key contentType } } } }`; the CMS carousel can also embed `recipes` (HLS / DASH on `media-cdn.epicgames.com`).

## Example (Fortnite)

```json
{
  "slug": "fortnite",
  "logoUrl": "https://cdn2.unrealengine.com/24br-s24-egs-launcher-logo-350x100-350x100-b63249f937d9.png",
  "landscapeUrl": "https://cdn2.unrealengine.com/fnbr-42-00-c7s4-hacking-logo-egs-launcher-blade-2560x1440-2560x1440-00f5395fc1e7.jpg",
  "portraitUrl": "https://cdn2.unrealengine.com/fnbr-42-00-c7s4-hacking-egs-launcher-blade-1200x1600-1200x1600-0138e7df7bb0.jpg",
  "media": [
    "https://cdn2.unrealengine.com/en-fn-og-42-10-c1sx-egs-launcher-blade-2560x1440-2560x1440-319ff81b274e.jpg"
  ],
  "releaseDate": "2017-07-25T04:00:00.000Z",
  "developer": "Epic Games",
  "videoUrl": "https://epic-games-store-cdn.qstv.on.epicgames.com/output/06deadf1-68ce-4e85-a5c7-eada52711226/output.mp4",
  "landscapeHeroCopy": null
}
```

## Unreal Engine and tools

The Unreal Engine tab's engines (`UE_4.0` to `UE_5.8`, namespace `ue`) and tools (Twinmotion, RealityScan, Quixel Bridge, Fab plugin) are seeded in the launcher binary and filled in from the catalog (`engines-cache.json`, `tools-cache.json`); the engine entries in `engines-cache.json` have empty `keyImages`.
