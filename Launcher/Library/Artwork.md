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
- Covers are downloaded by a background worker (`src\image_cache\worker.rs`). The CDN request adds `resize=1&w=<w>&h=<h>&quality=medium`; if the resized fetch fails the original URL is fetched (`Images.ResizedFetchFellBack`). `EGL_IMAGE_CDN_RESIZE=0` / `off` disables resizing, `EGL_IMAGE_FETCH_CONNECTIONS` sets parallelism.
- When an image lands, `image-cached-event` tells the frontend to swap the CDN URL for the local one in place.
- `set_priority_covers { items }` moves visible covers to the front of the queue; `recache_cover { cdnUrl, md5 }` forces one cover to be fetched again.

## Hero art

- `get_hero` / `prefetch_hero { hero }` and `cache_detail_hero { sourceUrl }` keep detail-pane hero images in a separate hero cache (`HeroInfo`: `localUrl`, `palette`); the palette is computed from the image and is empty when that fails. `heroCopy` on the catalog landscape image points at that copy.
- `get_store_product_art { namespace }` returns `StoreProductArt` (`slug`, `logoUrl`, `landscapeUrl`, `portraitUrl`, `media`, `releaseDate`, `videoUrl`, `landscapeHeroCopy`). It maps the namespace to a store slug (cached in `product-mapping-cache.json`), reads the store CMS product page (cached in `product-art-cache.json`, misses cached as negative entries) and the release date from [Catalog Namespace Offers](../../EpicGames/CatalogService/Catalog/Offers.md). The CMS calls go to `store-content.ak.epicgames.com` (not documented here).
