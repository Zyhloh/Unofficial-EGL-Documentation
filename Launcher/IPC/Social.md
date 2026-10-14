# IPC - Social

Social panel and the social bridge. Auth commands are in [Auth IPC](../Auth/IPC.md).

Args are the keys of the object the frontend passes to `invoke` (camelCase). Wrappers: `bindings-*.js` (`commands.*`).

## Social panel

| Command | Args | Purpose |
| --- | --- | --- |
| `social_overlay` | `action` | Show / hide / reload the `social` webview (`action`) |
| `get_social_overlay_defaults` | - | Default overlay URL / build |
| `social_panel_disabled` | - | Panel disabled flag |
| `social_panel_focus` | `entry` | Focus the panel |
| `social_chat_focus_self` | `signal` | Chat pop-out focus |
| `social_get_badge_count` | - | Unread badge count |
| `social_notification_actioned` | `query` | Toast action forwarded to the overlay |
| `game_invite_respond` | `senderId`, `accept` | Accept / decline a game invite |
| `debug_simulate_invite` | `invite` | Staff: fake invite |
| `social_webview_console_log` | `level`, `message` | Console forwarder of the overlay |

## Social bridge (`window.ue.social` / `ue.launcher` in the `social` webview)

| Command | Args | Purpose |
| --- | --- | --- |
| `social_bridge_get_client_token` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_get_version` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_get_friends_list` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_get_friend_status` | `args` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_has_third_party_accounts` | `args` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_get_third_party_accounts` | `args` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_get_third_party_friends` | `args` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_open_friend_linking` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_join_game` | `args` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_decline_game` | `args` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_set_away` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_set_online` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_get_online_status` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_set_show_notifications_enabled` | `args` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_is_show_notifications_enabled` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_get_features` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_send_intent` | `args` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_notify` | `notification` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_set_badge_counter` | `args` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_get_badge_counter` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_register_response_callback` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_register_states_listener` | `args` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_register_notification_actioned` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_register_badge_counter_update_actioned` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_show_social` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_hide_social` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_is_social_visible` | - | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
| `social_bridge_focus_launcher` | `direction` | v1 `USocialJSBridge` method, see [Bridge](../Social/Bridge.md) |
