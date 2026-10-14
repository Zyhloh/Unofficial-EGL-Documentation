# IPC - Store and Fab webviews

Content webviews and the store / Fab / checkout bridge.

Args are the keys of the object the frontend passes to `invoke` (camelCase). Wrappers: `bindings-*.js` (`commands.*`).

## Store webview

| Command | Args | Purpose |
| --- | --- | --- |
| `store_create_webview` | `route`, `bounds`, `revealOnLoad` | Create `store-webview` at `route` with `bounds` |
| `store_webview` | `action` | Show / hide / destroy (`action`) |
| `store_navigate_to` | `route` | Navigate to a store route |
| `store_set_bounds` | `bounds` | Resize |
| `store_nav` | `action` | Back / forward / reload (`action`) |
| `store_get_navigation_state` | - | canGoBack / canGoForward |
| `store_get_status` | - | Load status |
| `store_heartbeat` | - | Liveness ping |
| `store_webview_focus` | `entry` | Move keyboard focus into the store |
| `store_bridge_focus_launcher` | `direction` | Store hands focus back (`direction`) |
| `egs_zero_trust` | `action` | Staff: Cloudflare Zero Trust sign-in for the EGS v2 store (`action`) |

## Fab webview

| Command | Args | Purpose |
| --- | --- | --- |
| `fab_create_webview` | `bounds`, `revealOnLoad` | Create `fab-webview` |
| `fab_webview` | `action` | Show / hide / destroy |
| `fab_get_status` | - | Load status |
| `fab_get_navigation_state` | - | canGoBack / canGoForward |
| `fab_webview_focus` | `entry` | Focus into Fab |
| `fab_bridge_focus_launcher` | `direction` | Fab hands focus back |

## Store / Fab bridge (called from injected scripts)

| Command | Args | Purpose |
| --- | --- | --- |
| `bridge_get_signed_in_user` | - | `ue.common.getsignedinuser` |
| `bridge_get_access_token` | - | `ue.launcher.getaccesstoken` |
| `bridge_get_client_version` | - | `getversion`; advertises `19.0.0` and API versions `purchase` / `signin` / `layout` `1.0.0` |
| `bridge_request_purchase` | `offers` | `RequestPurchase` / `RequestPurchaseV2` ([Purchase](../Flows/Purchase.md)) |
| `bridge_request_purchase_cart` | `cart` | `RequestPurchaseCart` |
| `bridge_checkout_complete` | `reason` | Checkout overlay finished (`reason`) |
| `bridge_open_native_library` | `offerId`, `sandboxId`, `sort`, `url` | Jump to the native library for an offer |
| `bridge_open_external_url` | `url` | `launchexternalurl` |
| `bridge_notify_store_first_paint` | `url` | Store painted |
| `bridge_notify_content_painted` | `label` | Any bridged webview painted (`label`) |
| `bridge_log_web_perf` | `label`, `metric`, `ms` | Web perf metric |
| `bridge_take_pending_focus_entry` | - | Focus hand-off entry point |
| `shell_nav` | `action` | Back / forward from a content webview |
