# IPC - Unreal Engine and Fab

Engines, tools, projects and the native half of the Fab bridge.

Args are the keys of the object the frontend passes to `invoke` (camelCase). Wrappers: `bindings-*.js` (`commands.*`).

## Engines and tools

| Command | Args | Purpose |
| --- | --- | --- |
| `list_engine_versions` | - | Installed + available UE versions |
| `check_engine_install_requirements` | `appId` | EULA / entitlement gate for one engine |
| `check_engine_install_requirements_bulk` | `appIds` | Same, bulk |
| `acquire_engine_entitlement` | `appId`, `eulaKey` | Accept EULA and grant the engine entitlement |
| `list_engine_plugins` | `engineAppId` | Marketplace plugins for an engine |
| `set_engine_plugin_installed` | `engineAppId`, `pluginAppId`, `shouldBeInstalled` | Install / remove a plugin |
| `list_ue_tools` | - | UE tools (e.g. Twinmotion) |
| `check_tool_install_requirements_bulk` | `appIds` | Tool gates |
| `acquire_tool_entitlement` | `appId`, `eulaKey` | Accept EULA and grant the tool entitlement |
| `acquire_uefn_entitlement` | - | Grant UEFN |
| `scan_local_ue_engines` | - | Find source / custom engines |
| `add_custom_ue_engine` | `path` | Register a custom engine |
| `list_custom_ue_engines` | - | List them |
| `remove_custom_ue_engine` | `path` | Unregister |
| `launch_ue_engine` | `path` | Start an editor |
| `reveal_ue_engine` | `version` | Reveal engine folder |
| `open_ue_engine_dir` | `path` | Open engine folder |
| `get_ue_news_feed` | `query` | Unreal news feed page (`query`: `limit` 1..N, `skip`) |

## Projects

| Command | Args | Purpose |
| --- | --- | --- |
| `list_ue_projects` | - | Discovered `.uproject` files |
| `launch_ue_project` | `uprojectPath`, `engineVersion` | Open a project |
| `reveal_ue_project` | `uprojectPath` | Reveal |
| `set_ue_project_engine` | `uprojectPath`, `engineAssociation` | Change `EngineAssociation` |
| `delete_ue_project` | `projectDir` | Delete project folder |
| `ue_projects_total_size` | `projectDirs` | Sizes |
| `ue_missing_project_files` | `descriptorPaths` | Which descriptors are gone |

## Fab (native side of `window.ue.fab`)

| Command | Args | Purpose |
| --- | --- | --- |
| `fab_egl_get_api_version` | - | `getapiversion` |
| `fab_egl_get_settings` | - | `getsettings` |
| `fab_egl_save_settings` | `settings` | `savesettings` |
| `fab_egl_get_listings` | `userid`, `listings` | `getlistings` |
| `fab_egl_search_local_listings` | `userid`, `q`, `page`, `itemperpage`, `format` | `searchlocallistings` (local vault) |
| `fab_egl_remove_local_listing` | `id` | `removelocallisting` |
| `fab_egl_show_listing_on_disk` | `path` | `showlistingondisk` |
| `fab_egl_reveal_listing_by_uid` | `uid` | Reveal a listing |
| `fab_egl_download_ondemand` | `url`, `metadata` | `downloadondemand` |
| `fab_egl_download_unreal_listings` | `listings`, `metadata` | `downloadunreallistings` |
| `fab_egl_export_asset` | `listinguid`, `metadata` | `exportasset` (DCC export) |
| `fab_egl_export_bulk` | `params` | `exportlistingbulk` |
| `fab_egl_prepare_add_to_project` | `listings`, `metadata` | `addtoproject` preparation |
| `fab_egl_pick_folder` | - | Folder picker |
| `fab_egl_plugin` | `target`, `action` | DCC plugin install / remove / open (`target`, `action`) |
| `fab_egl_show_logs` | - | `showlogs` |
| `fab_ue_compatible_targets` | `listingUid`, `compatibility`, `distributionMethod` | Projects / engines a listing can go into |
| `fab_ue_add_to_project` | `listingUid`, `targetKind`, `targetPath` | Add asset pack / project to a target |
| `fab_ue_install_code_plugin_to_engine` | `listingUid`, `enginePath` | Install a code plugin into an engine |
| `fab_ue_install_code_plugin_to_project` | `listingUid`, `projectPath` | Install a code plugin into a project |
| `fab_ue_project_thumbnail` | `projectDir` | Project thumbnail |
