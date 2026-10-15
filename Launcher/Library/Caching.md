# Library Caching

The launcher keeps JSON caches so the library renders before any network call. Caches are per account (a per-account cache directory is created on first write, "Failed to create account cache directory") under the launcher data directory (`%LOCALAPPDATA%\com.epicgames.eglv2` on Windows; shared caches in `cache\<env>\` (e.g. `cache\prod\catalog-cache.json`), per-account ones in `cache\<env>\account\`).

## Files

| File | Contents | Struct | Invalidation |
| ---- | -------- | ------ | ------------ |
| `library-cache.json` | Library records | `CachedLibrary` (5 fields: `expiresAt`, `cachedAt`, `stateToken` + 2 not separated, likely `items` and `schemaVersion`) | 1 hour; schema version, or an invalid `stateToken`. A valid token extends `expiresAt` by 1 hour. An expired copy is still shown while the refresh runs. Not written when the library is empty |
| `catalog-cache.json` | Catalog items | `CachedCatalog` (`schemaVersion`, `locale`, `entries`); `CachedCatalogEntry` (`item`, `expiresAt`, `cachedAt`) | 30 minutes per entry ("Removed expired catalog cache entries"), locale mismatch, schema mismatch |
| `collections-cache.json` | Collection definitions | `CachedCollections` | 5 minutes; rewritten after every fetch / mutation |
| collection items cache | Items of one collection | `CachedCollectionItems` | 5 minutes; rewritten after fetch (`Collections.ItemsCacheServed`) |
| `playtime-cache.json` | Playtime per artifact | `CachedPlaytime` | 5 minutes; background refresh after serving |
| `store-tags-cache.json` | Tag dictionaries per group + locale | `CachedStoreTagsCache` / `CachedStoreTagsEntry` | 7 days |
| `sd-cache.json` | Selective-download components | `CachedSdCache` / `CachedSdEntry` (`info`, `buildVersion`, `platform`, `sdMetaHash`, locale) | 30 minutes; `buildVersion` / `sdMetaHash` change, platform or locale mismatch, missing sizes |
| `product-mapping-cache.json` | Namespace → store slug | `CachedProductMapping` | 24 hours |
| `product-art-cache.json` | Store hero / logo art per slug | `CachedProductArtCache` / `CachedProductArtEntry` | 24 hours; negative entries (no store page) 7 days |
| `platform-availability-cache.json` | Per-platform build availability | | |
| `ue-gates-cache.json`, `engines-cache.json`, `tools-cache.json` | Unreal Engine tab | | Engines / tools: no expiry, served and then refreshed every time |
| `disk-size-cache.json` | Installed sizes | | |

Local-only state (not caches of a service):

| File | Contents |
| ---- | -------- |
| `library-settings.json` | View settings incl. `hiddenItems` |
| `recently-played.json`, `last-played.json` | Recency data for sorting |
| `playtimejournal.json` | Unpublished play intervals |
| `installations.jsonl` | Install records (`Installation`: `installationId`, `dir`, `platform`, `namespace`, `itemId`, `artifactId`, `version`, `tags`, `pendingVersion`, `pendingTags`, `parentInstallationId`, `mainArtifactId`, `isFab`, `prereqSha1Hash`, `lastPrereqSucceededSha1Hash`, `componentSelection`, `dependencyConfig`, `sidecar`, `launchCommand`, `launchExecutable`, `writtenAt`) |
| `external-library.json`, `igdb-metadata-cache.json` | External sources, see [External Sources](ExternalSources.md) |

`clear_caches` / `get_cache_size` operate on these caches (the cache kinds are named `library`, `catalog`, `collections`, `collection_items`, `playtime`, `engines`, `tools`, `ue_gates`, `platform_availability`, `selective_download`, `store_tags`, `product_mapping`, `product_art`, `account`).

## State token

The last page of [Library Items](../../EpicGames/LibraryService/Library/Items.md) returns `responseMetadata.stateToken`. It is stored in `library-cache.json`. Each refresh first asks [State Token Status](../../EpicGames/LibraryService/StateToken/Status.md); `valid: true` means the server-side library is unchanged since that walk, so the walk and catalog fetch are skipped and only the cache TTL is extended.

## Images

Cover and hero images live in the image cache (`eglv2_lib::image_cache`), keyed by the key image `md5` (or `sha1(url)` when the catalog omits it) and served to the webview through a custom protocol (`img://` / `tauri://` local URLs, `Cache-Control: public, max-age=31536000, immutable`). See [Artwork](Artwork.md).
