# IPC

The React frontend talks to the Rust backend only through Tauri `invoke` (commands) and Tauri events. Commands are generated with tauri-specta: every typed wrapper in `bindings-*.js` looks like

```js
async socialOverlay(e) {
  try { return { status: `ok`, data: await t(`social_overlay`, { action: e }) } }
  catch (e) { if (e instanceof Error) throw e; return { status: `error`, error: e } }
}
```

so a command either resolves `{ status: "ok", data }` or `{ status: "error", error }` where `error` is the serialized backend error. Error kinds in the binary: `io_error`, `not_authenticated`, `user_cancelled`, `auth_failed`, `install_location_unavailable`, `refused_by_state`, `invalid_input`, `platform_unavailable`, `partner_handoff_failed`, `partner_redemption_required`, `network`, `access_restricted`, `cabined_blocked`, `cloud_save_decision_required`. 16 commands are untyped wrappers that return the raw value (`quit_app`, `relaunch`, `raise_shell`, `deeplink_take_pending`, ...).

305 commands in total: 288 typed wrappers, 16 untyped wrappers and `create_desktop_shortcut` (invoked directly).

| Page | Area |
| --- | --- |
| [Auth IPC](../Auth/IPC.md) | `auth_*`, `bridge_get_access_token`, `bridge_get_signed_in_user`, `open_account_link`, `open_partner_account_link`, `cabined_gate_acknowledge`, `prefetch_exchange_code` |
| [Library](Library.md) | Library, catalog, collections, playtime, external and partner titles |
| [Games](Games.md) | Install, downloads, launch, cloud saves, install scan, v1 migration |
| [Unreal Engine and Fab](UnrealFab.md) | Engines, tools, projects, Fab native bridge |
| [Store and Fab webviews](StoreFab.md) | Content webviews and bridge commands |
| [Social](Social.md) | Social panel and social bridge |
| [App](App.md) | Settings, environment, self update, windows, EULA, flags, telemetry |
| [Events](Events.md) | Backend events, tray / toast / social channels, injected bridge objects |

Names in `js_commands.txt` that are not commands: `account_changed`, `before_send`, `buffer_overflow`, `build_branch`, `cloud_save_retry`, `event_processor`, `failed_url`, `invalid_game_payload`, `item_not_an_object`, `items_not_an_array`, `left_library`, `modal_closed`, `network_error`, `not_an_object`, `queue_overflow`, `quick_launch`, `ratelimit_backoff`, `remove_v1`, `sample_rate`, `unknown_item_id`, `unknown_version`, `user_selected`, `view_changed` (error / analytics codes) and the shell menu keys `account_settings`, `account_balance`, `epic_rewards`, `terms_of_service`, `privacy_policy`, `store_refund_policy`, `publisher_index` (passed to `open_account_link`, see [Deep Links](../DeepLinks.md#external-pages)).
