# IPC - Library

Library, catalog, collections, playtime, external and partner titles.

Args are the keys of the object the frontend passes to `invoke` (camelCase). Wrappers: `bindings-*.js` (`commands.*`).

## Library and catalog

| Command | Args | Purpose |
| --- | --- | --- |
| `get_library` | `forceRefresh` | Library records (cache first, `forceRefresh` to refetch) |
| `get_library_boot_bundle` | - | Small boot bundle: catalog, collections, installed games, product states, library settings |
| `get_library_full_bundle` | - | Full bundle after boot |
| `get_catalog` | - | Cached catalog items |
| `refresh_catalog_from_server` | - | Refetch catalog for all library items |
| `refresh_catalog_item` | `appId` | Refetch one catalog item |
| `get_app_configuration` | `parentAppId` | DLC / add-on configuration of a parent app |
| `set_app_configuration` | `parentAppId`, `configs`, `allowUninstall` | Apply add-on selection (install / uninstall add-ons) |
| `get_dlc_manifest_sizes` | `parentAppId`, `items` | Download sizes for add-ons |
| `get_installed_games` | - | Installed games list |
| `get_all_product_states` | - | Backend computed tile state for every app |
| `get_store_tags` | `groupName`, `locale` | Tag dictionary for a group ([Library Service Tags](../../EpicGames/LibraryService/Tags/Get.md)) |
| `get_store_product_art` | `namespace` | Store art / trailer for a namespace ([Store Content](../../EpicGames/StoreContentService)) |
| `get_fn_deployment_info` | `catalogItemId` | Fortnite backend build info ([Fortnite App Service](../../EpicGames/FortniteAppService)) |
| `get_library_settings` | - | Library filters / sort |
| `set_library_settings` | `settings` | Save library filters / sort |
| `set_library_item_hidden` | `appId`, `hidden` | Hide / unhide a title |
| `set_priority_covers` | `items` | Tell the image cache which covers to fetch first |
| `recache_cover` | `cdnUrl`, `md5` | Refetch one cover (`cdnUrl`, `md5`) |
| `cache_detail_hero` | `sourceUrl` | Cache a detail page hero image |
| `prefetch_hero` | `hero` | Prefetch a hero image |
| `get_hero` | `hero` | Local URL of a cached hero |
| `get_platform_availability` | - | Cached per-app platform availability |
| `probe_platform_availability` | `appIds` | Probe availability for apps |

## Collections

| Command | Args | Purpose |
| --- | --- | --- |
| `list_collections` | - | [Collections List](../../EpicGames/LibraryService/Collections/List.md) |
| `list_collection_items` | `collectionId` | Items of a collection |
| `create_collection` | `name` | Create |
| `rename_collection` | `collectionId`, `name` | Rename |
| `delete_collection` | `collectionId` | Delete |
| `reorder_collections` | `orderedCollectionIds` | Reorder |
| `set_collection_item` | `collectionId`, `sandbox`, `catalogId`, `member` | Add (`member: true`) / remove an item |

## Playtime

| Command | Args | Purpose |
| --- | --- | --- |
| `get_playtime` | - | Playtime per app |
| `get_last_played` | - | Last played timestamps |
| `get_recently_played` | - | Recently played list |
| `get_running_games` | - | Currently running games |

## External sources (Steam / Xbox)

| Command | Args | Purpose |
| --- | --- | --- |
| `get_external_library` | - | Discovered external games |
| `get_external_source_states` | - | Per-source enabled / discovery state |
| `set_external_source_enabled` | `source`, `enabled` | Enable / disable a source |
| `start_external_discovery` | `source` | Rescan a source |
| `launch_external_game` | `id` | Launch through Steam / Xbox shell |
| `hide_external_item` | `id` | Hide an external game |
| `unhide_external_item` | `id` | Unhide |
| `get_external_game_metadata` | `source`, `title` | IGDB metadata for a title ([IGDB](../../ThirdParty/IGDB/Games/Search.md)) |

## Partner titles (EA app / Ubisoft Connect)

| Command | Args | Purpose |
| --- | --- | --- |
| `get_partner_titles` | - | Partner-managed titles and their state |
| `open_partner_account_link` | `provider`, `pageStrings` | Open the account linking page for a provider |
| `begin_partner_client_acquisition` | `appId`, `action` | Download / start the partner client installer (`action`) |
| `cancel_partner_client_acquisition` | `appId` | Cancel it |
| `end_partner_install_wait` | `appId` | Stop waiting for a partner side install |
| `redeem_partner_codes` | `appId` | [Partner Integration](../../EpicGames/PartnerIntegrationService) code redemption |
| `refresh_partner_install_disk_size` | `appId` | Re-measure a partner install |
