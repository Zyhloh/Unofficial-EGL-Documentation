# External Library Sources

Games from other stores shown in the library (`eglv2_lib::external_library`). IPC: `get_external_library`, `get_external_source_states`, `set_external_source_enabled { source, enabled }`, `start_external_discovery { source }`, `launch_external_game { id }`, `hide_external_item { id }`, `unhide_external_item { id }`, `get_external_game_metadata { source, title }`. Changes are announced with the payload-free `external-library-updated-event`; the frontend then re-reads `get_external_library`.

## Sources

| Source | Discovery | Network |
| ------ | --------- | ------- |
| `steam` | Local: Steam install root, `steamapps/libraryfolders.vdf`, then each folder's app manifests | None. Launch hands off to `steam://rungameid/<id>` |
| `xbox` | Local: installed packages via the Windows package manager, `AppxManifest.xml` / `MicrosoftGame.config`, Xbox game roots | None. Launch through `shell:AppsFolder\<AUMID>` |

Results are stored in `external-library.json`. A background rescan runs on an interval (`externalRescanIntervalMinutes` setting, `externalSourcesEnabled` per source). Entries on drives that are temporarily unreachable are retained (`ExternalLibrary.UnreachableEntriesRetained`).

## Metadata

`get_external_game_metadata` looks titles up on IGDB (`https://api.igdb.com/v4/games`, `Client-ID` + `Authorization: Bearer` headers) with an app token minted from Twitch (`https://id.twitch.tv/oauth...`, client credentials from build-time `EGL_IGDB_CLIENT_ID` / `EGL_IGDB_CLIENT_SECRET`). Fields read: `name`, `summary`, `first_release_date`, `genres`, `involved_companies` (`IgdbGame`, `IgdbGenre`, `IgdbCompany`, `IgdbInvolvedCompany`). Results are cached in `igdb-metadata-cache.json`.

## Partner titles

EA app and Ubisoft Connect titles (`ea_app`, `ubisoft_connect`) are not external sources: they are Epic library items whose catalog attributes name a partner provider and go through the partner flow (`get_partner_titles`, `begin_partner_client_acquisition`, ...). The partner client installers come from the [Launcher Content Build](../../EpicGames/LauncherService/Assets/LauncherContent.md).
