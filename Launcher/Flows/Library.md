# Library

How the launcher builds the Library tab: what it reads from disk at startup, which services it calls, how it refreshes and how library records become tiles with art.

Rust modules: `eglv2_lib::api::{library, catalog, collections, store_tags}`, `eglv2_lib::commands::{library, collections}`, `src\refresh\mod.rs`, `src\refresh\auto_refresh.rs`, `eglv2_lib::image_cache`.

## Data model

- **Library item** (`LibraryItem`): `relationshipId` (`{namespace}:{catalogItemId}:{appName}`), `appId` (`{ namespaceId, itemId, appName }`), `recordType` (`APPLICATION` / `SUBSCRIPTION`), `acquisitionDate`, `tags`, `owned`. Comes from [Library Items](../../EpicGames/LibraryService/Library/Items.md). It carries no catalog data.
- **Catalog item** (`CatalogItem`): title, key images, categories, release info, `mainGameItem`, custom attributes, DLC list, EULA ids. Comes from [Catalog Bulk Items](../../EpicGames/CatalogService/Catalog/BulkItems.md) and is keyed by `appId.itemId`.
- A library item is joined to its catalog item by `itemId`. Add-ons point at their parent through `mainGameItem` ("... is an add-on of catalog item ..."); a cycle in those links is treated as "no parent".

## Startup

1. `index.html` invokes `get_library_boot_bundle` at HTML-parse time, before the JS bundle loads, and parks the promise on `window.__BOOTSTRAP_PROMISE__`. In parallel it invokes `auth_has_cached_session` (file-existence check).
2. During setup the backend pre-reads the library cache ("Pre-read library cache during setup", `Library.CachePreRead`), so the boot bundle is served from disk without network.
3. The boot bundle (`LibraryBootBundle`) carries: `accountId`, `library`, `catalog` (slim: `BootCatalogItem`, flagged `catalogIsSlim: true`), `collections`, `installedGames`, `productStates`, `librarySettings`, `globalAppSettings`, `incompatibleOnPlatform`, `availabilityFailures`, `pendingOnPlatform`, `externalGames`.
4. The frontend `library-bundle` query (TanStack Query, `staleTime` 5 min, `gcTime` 1 h, `offlineFirst`) consumes that promise; if it is missing or rejects it calls `get_library_full_bundle`.
5. While the catalog is slim the query refetches on window focus; otherwise only after 30 min. `get_library_full_bundle` waits for auth (`Library.BundleAuthPending` / `BundleAuthReady` / `BundleAuthTimedOut`), then returns the cached library ("Returning cached library (full bundle)") or waits for the first refresh ("No library cache, waiting for refresh"), plus the full catalog and cached collections (`Library.BundleStepsTimed` logs per-step timings).
6. When the authoritative refresh finishes, the backend pushes `library-updated-event` and `catalog-updated-event`; the frontend swaps them into the bundle.

## Refresh

A refresh is a `RefreshRequest` on an internal channel (`src\refresh\mod.rs`). Requests are coalesced (`Library.RefreshCoalesced`) and skipped when signed out.

Triggers (`trigger` values found next to the refresh code: `periodic`, `automatic`, `focus`, `systray_restore`, `store_exit`, `retry`):

| Trigger | Source |
| ------- | ------ |
| periodic | `auto_refresh.rs` timer, starts after authentication |
| automatic | Background (e.g. late purchase grant, "Library reflected a change after store") |
| focus | Window focus |
| systray_restore | Restoring from the tray |
| store_exit | Leaving the store webview ("requested library reconcile (force:false, store_exit)") |
| retry | Scheduled retry after a failure |
| (sign-in) | Auth `LoggedIn` event (`Library.RefreshRequestedOnSignIn`) |
| (forced) | `forced` flag: `get_library { forceRefresh: true }`, `refresh_catalog_from_server`, post-purchase ownership checks |

Steps:

1. No cached `stateToken` → full refresh.
2. Otherwise [State Token Status](../../EpicGames/LibraryService/StateToken/Status.md):
   - `valid: true` → extend the library cache TTL and stop; no frontend events ("Refresh skipped (state token valid)"). If the catalog cache is unusable, the catalog is re-fetched for the cached library without walking it ("enriching from cached library (no walk)").
   - `valid: false` → full refresh.
3. Full refresh: walk [Library Items](../../EpicGames/LibraryService/Library/Items.md) (500 per page, `cursor`, max 50 pages, dedupe), save `library-cache.json` with the new `stateToken`.
4. Group records by namespace and call [Catalog Bulk Items](../../EpicGames/CatalogService/Catalog/BulkItems.md) for each (`fetch_catalog_batch`), with the UI locale. Progressive snapshots are pushed as `catalog-updated-event { partial: true }` (merged, never dropping entries); the final one has `partial: false` and replaces the frontend catalog. Saved to `catalog-cache.json`.
5. Seed product states (`Library.ProductStatesSeeded`) and emit `library-updated-event { items, fromCache, cachedAt, refreshFailed }`. On failure `refreshFailed: true` is sent with empty `items` and the caches stay untouched.

A catalog item the library does not list (first seen by an install) is fetched on demand and pushed as `catalog-item-cached-event`.

## Collections, favorites, hidden

- Collections are server-side: [List](../../EpicGames/LibraryService/Collections/List.md), [Create](../../EpicGames/LibraryService/Collections/Create.md), [Rename](../../EpicGames/LibraryService/Collections/Rename.md), [Delete](../../EpicGames/LibraryService/Collections/Delete.md), [Reorder](../../EpicGames/LibraryService/Collections/Reorder.md), [List Items](../../EpicGames/LibraryService/Collections/ListItems.md), [Add Item](../../EpicGames/LibraryService/Collections/AddItem.md), [Remove Item](../../EpicGames/LibraryService/Collections/RemoveItem.md). IPC: `list_collections`, `list_collection_items`, `create_collection`, `rename_collection`, `delete_collection`, `reorder_collections`, `set_collection_item { collectionId, sandbox, catalogId, member }`.
- Favorites is the collection `EGS_STATIC_FAV_COLLECTION` (name `Favorites`); the Favorites tab is that collection's items.
- Items are identified by `sandbox` (namespace) + `catalogId`, not by app name.
- Hiding is local only: `set_library_item_hidden { appId, hidden }` writes `hiddenItems` in `library-settings.json` (`LibraryViewSettings`: `installedOnly`, `keywordFilter`, `sortOrder`, `viewMode`, `platformFilters`, `genreFilters`, `featureFilters`, `hiddenItems`, `hiddenExternalItems`, `showHiddenItems`). External titles use `hide_external_item` / `unhide_external_item`.

## Tags

Library records list tag ids. The genre / feature filters resolve them with [Tags](../../EpicGames/LibraryService/Tags/Get.md) (`get_store_tags { groupName, locale }`, groups `genre`, `feature`, `epicfeature`), cached in `store-tags-cache.json`.

## Playtime and recency

- `get_playtime` → [Playtime Get All](../../EpicGames/LibraryService/Playtime/GetAll.md), served from `playtime-cache.json` and refreshed in the background.
- Play sessions are written to a local journal (`playtimejournal.json`) and uploaded with [Playtime Publish Bulk](../../EpicGames/LibraryService/Playtime/PublishBulk.md) → `playtime-published-event`. Unpublished time is lost if the journal is corrupt.
- `get_recently_played` and `get_last_played` are local only (`recently-played.json`, `last-played.json`); `get_last_played` returns `{ appName: ISO timestamp }`.

## Art

See [Artwork](../Library/Artwork.md). Grid covers come from catalog `keyImages`, preferring `DieselGameBoxTall`, and are downsampled into a local image cache.

## Related

- [Caching](../Library/Caching.md)
- [External Sources](../Library/ExternalSources.md)
- [Install and Update](InstallAndUpdate.md)
