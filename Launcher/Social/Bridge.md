# Social Overlay - Native Bridge

The overlay talks to the launcher only through globals injected into the `social` webview. Two layers exist:

1. `social-bridge.js` (launcher, embedded in the exe): `window.ue.social`, `window.ue.common`, `window.ue.launcher`, each method proxied to a Tauri command over `window.__TAURI_INTERNALS__.invoke`.
2. EOS SDK overlay bridge (injected after it, `EOSOverlayCommonJS`): merges camelCase methods onto the same `window.ue.social` object: `getNextChanges`, `getNextNotifications`, `getFeatures`, `sendIntent`, `getVersion`, `getCodeVerifier`, `verifyIntent`, `sanitizeStrings`.

Remote access is granted by the capability `social-bridge-remote` (`webviews: ["social"]`, `remote.urls: ["https://api.epicgames.dev", "https://api-gamedev.ol.epicgames.net"]`, 32 commands + `core:event:allow-listen`). The `social-chat` popup gets only `social_webview_console_log`.

## Bridge selection

The app checks `window.ue.social.getNextChanges && window.social.broker` (`isUnifiedBridge()`):

- Unified: `getNextChanges` is present (SDK bridge attached). SDK state is long-polled with `getNextChanges({ features })`, launcher requests travel as notifications (below).
- Legacy: methods are called directly on `window.ue.social` / `window.ue.launcher`, intents via `sendintent({ feature, name, payload: JSON.stringify(payload) })`, SDK state via `window.eos.registerStatesListener`.

## window.ue.social (launcher)

| Method | Tauri command | Args | Returns |
| --- | --- | --- | --- |
| `getclienttoken()` | `social_bridge_get_client_token` | | `{ token, productId, organizationId }` |
| `getversion()` | `social_bridge_get_version` | | `FSdkVersionInfo` (`version` read; `>= 1.0.1` enables `window.open` and `ue.launcher`) |
| `getfriendslist()` | `social_bridge_get_friends_list` | | `{ friends: FriendState[] }` |
| `getfriendstatus(friendId)` | `social_bridge_get_friend_status` | `args: { friendId }` | `FriendState` |
| `hasthirdpartyaccounts(service)` | `social_bridge_has_third_party_accounts` | `args: { service }` | bool |
| `getthirdpartyaccounts(service, maxAccounts)` | `social_bridge_get_third_party_accounts` | `args: { service, maxAccounts }` | JSON string |
| `getthirdpartyfriends(service, userId, maxFriends)` | `social_bridge_get_third_party_friends` | `args: { service, userId, maxFriends }` | JSON string |
| `openfriendlinking()` | `social_bridge_open_friend_linking` | | |
| `joingame(friendId)` | `social_bridge_join_game` | `args: { friendId }` | |
| `declinegame(friendId)` | `social_bridge_decline_game` | `args: { friendId }` | |
| `setaway()` | `social_bridge_set_away` | | |
| `setonline()` | `social_bridge_set_online` | | |
| `getonlinestatus()` | `social_bridge_get_online_status` | | `Online` / `Away` / `Offline` |
| `setshownotificationsenabled(enabled)` | `social_bridge_set_show_notifications_enabled` | `args: { enabled }` | |
| `isshownotificationsenabled()` | `social_bridge_is_show_notifications_enabled` | | bool |
| `getfeatures()` | `social_bridge_get_features` | | string[] |
| `sendintent({ feature, name, payload })` | `social_bridge_send_intent` | `args: { feature, name, payload }` (payload is a JSON string) | bool |
| `notify(n)` | `social_bridge_notify` | `notification: { type, title, message, payload }` | |
| `setbadgecounter(count)` | `social_bridge_set_badge_counter` | `args: { count }` (clamped `>= 0`) | |
| `getbadgecounter()` | `social_bridge_get_badge_counter` | | u32 |
| `registerresponsecallback(fn)` | `social_bridge_register_response_callback` | | |
| `registerstateslistener(fn, features)` | `social_bridge_register_states_listener` | `args: { features }` | |
| `notificationactioned(fn)` | `social_bridge_register_notification_actioned` | | |
| `badgecounterupdateactioned(fn)` | `social_bridge_register_badge_counter_update_actioned` | | |

## window.ue.common / window.ue.launcher

| Method | Tauri command | Notes |
| --- | --- | --- |
| `common.getsignedinuser()` | `bridge_get_signed_in_user` | `accesstoken` is used as the elevated bearer for every REST/GraphQL call |
| `common.launchexternalurl(url)` | none | `window.open(url)` after checking `https:` and host `epicgames.com` / `epicgames.dev` / `epicgames.net` (+ subdomains) |
| `launcher.showsocial()` | `social_bridge_show_social` | |
| `launcher.hidesocial()` | `social_bridge_hide_social` | no-op on macOS, `InvalidState` on Windows/Linux; also bound to Esc |
| `launcher.issocialvisible()` | `social_bridge_is_social_visible` | |
| `launcher.socialvisibilitychanged(cb)` | event `social-window://visibility-changed` | fires a synthetic `cb(true)` on subscribe |

Other commands used by the injected scripts: `social_webview_console_log` (`{ level, message }`), `bridge_notify_content_painted` (`{ label: "social" }`), `social_bridge_focus_launcher` (`{ direction: "forward" | "backward" }`), `bridge_take_pending_focus_entry` (returns `first` / `last`).

## Push events (launcher -> page)

Tauri events targeted at `WebviewWindow{label:"social"}`:

| Event | Payload | Dispatched to |
| --- | --- | --- |
| `social-window://auth-token-refreshed` | | ignored by the bridge |
| `social-window://response-callback` | any | `registerresponsecallback` fn |
| `social-window://states-listener` | any | `registerstateslistener` fn |
| `social-window://notification-actioned` | `{ query }` | `notificationactioned` fn |
| `social-window://badge-counter-update` | `{ count }` | `badgecounterupdateactioned` fn |
| `social-window://visibility-changed` | `{ visible }` | `socialvisibilitychanged` callbacks |

The shell (main frontend) separately listens to `social://notify` (`{ type, title, message, conversationId, actionQuery }` -> toast), `social://badge-count-updated` (`{ count }`), `social://conversation-read`, `social://game-invite-received`, `social://game-invite-accepted`, `social://game-invite-dismissed`, `social://game-invite-store`, `social://open-friend-linking`, `social://resize-panel`.

## Unified bridge: notification channel

In unified mode every launcher-side request is wrapped as a broker intent:

```json
{ "feature": "application", "name": "send-notification", "payload": { "content": "{\"feature\":\"social\",\"name\":\"get-version\",\"payload\":{}}" } }
```

The broker forwards it with `window.ue.social.sendIntent` (SDK). Answers and pushes come back from `window.ue.social.getNextNotifications()` (long poll, JSON string per message, `{ name, payload }`); request/response pairs match on `<name>-response`. The launcher handles these in `src\social\handlers\{common,social,game,productinfo,stt,tts}.rs` (inferred routing: SDK host callback -> launcher, from the matching handler names).

| feature | name | payload | response / push |
| --- | --- | --- | --- |
| `social` | `get-version` | | `get-version-response` `{ version }` |
| `social` | `notify` | notification object | |
| `social` | `set-show-notifications-enabled` | `{ enabled }` | |
| `social` | `is-show-notifications-enabled` | | `...-response` `{ enabled }` |
| `social` | `notification-actioned-subscribe` | | push `notification-actioned` `{ query }` |
| `social` | `is-screen-reader-enabled` | | `...-response` `{ enabled }` |
| `social` | `screen-reader-state-changed-subscribe` | | push `screen-reader-state-changed` `{ enabled }` |
| `social` | `mic-permission-changed-subscribe` / `mic-permission-changed-unsubscribe` | | push `mic-permission-changed` `{ isAllowed }` |
| `social` | `get-idle-state` | | `...-response` `{ state }` (`UserActive` = active) |
| `social` | `subscribe-idle-state-changes` | | push `idle-state-changed` `{ state }` |
| `social` | `conversation-read` | `{ conversationId }` | |
| `social` | `voice-party-state-changed` | `{ state }` | |
| `social` | `set-local-voice-setting` | `{ configName, configValue }` | |
| `social` | `get-local-voice-setting` | `{ configName }` | `...-response` `{ configValue }` |
| `social` | `resize-panel` | `{ width }` | |
| `social` | `open-friend-linking` | | |
| `common` | `launch-external-url` | `{ url }` | |
| `common` | `get-window-state` | | `...-response` `{ state }` (`Minimized`, `SystemTray`, `Focused`, ...) |
| `common` | `subscribe-window-state-changes` | | push `window-state-changed` `{ state }` |
| `common` | `get-connection-state` | | `...-response` `{ state }` (`Online` / `Offline`) |
| `common` | `subscribe-connection-state-changes` | | push `connection-state-changed` `{ state }` |
| `game` | `accept-game-invite` / `dismiss-game-invite` / `join-game` | `{ friendId }` | push `game-invite-received`, `game-invite-accepted` `{ friendId }`, `game-invite-dismissed` `{ friendId }` |
| `productinfo` | `get-installed-apps` | | `...-response` `{ products: [...] }` (keys lowercased by the app) |
| `stt` | `start-dictation` | `{ conversationId, conversationType, messageId, dictationSessionId }` | push `dictation-started` / `dictation-result` `{ sessionId, recognizedText, confidence, isFinal }` / `dictation-error` `{ sessionId, errorCategory }` / `dictation-ended` `{ sessionId, finalText }` |
| `stt` | `end-dictation` | `{ body, sessionId }` | |
| `stt` | `is-dictating` / `get-active-session-id` / `get-microphone-permission-status` / `get-speech-recognition-permission-status` | | `...-response` |
| `stt` | `open-microphone-settings` / `open-speech-recognition-settings` | | opens `ms-settings:privacy-microphone` / `ms-settings:privacy-speech` |
| `tts` | `start-speak` | `{ conversationId, messageId, messageBody, speakingSessionId }` | push `speech-start`, `speech-progress`, `speech-complete`, `speech-error` |
| `tts` | `stop-speak` `{ speakingSessionId }` / `stop-speak-all` / `is-any-speaking` / `is-speaking` | | |

Badge count is a direct broker intent: `{ feature: "application", name: "update-badge-count", payload: { badgeCount } }`.

## Intents routed to the SDK

The broker's SDK intent handler forwards any intent whose `feature` is in `getFeatures()`, except `connect-epic-connect`, `exchange-token`, `launch-external-url`, `new-auth-intent`, `reload-overlay`, `send-presence-update` (handled in-page). `sendIntent` returns `{ id, correlationId, status }`; when `status` is `processing` the app waits for the `intent-status` SDK collection to report `complete` / `error` for that id.

SDK state names consumed through `getNextChanges`: `account-info`, `app-info`, `friends`, `presences`, `pending-game-invites`, `game-info`, `active-lobby`, `lobby-members`, `pending-request-to-join`, `pending-platform-requests`, `update-elements`, `intent-status`, and passthrough `hotkey-info`, `last-error`, `achievements`, `voice-terms-acceptance`, `voice-report`, `request-session-info`, `voice-room`, `input-device`, `output-device`, `bindings`, `voice-settings`. Each change is `{ name, state | add | remove | update, collection, keyName, reason }`.

`account-info` carries `id`, `displayName`, `authToken` (non-elevated EOS token), `elevatedToken` / `accessTokenOverride`, `identities`, `platform`. `getVersion()` (SDK) returns `platform`, `osVersion`, `version`, `productName`, `productVersion`, `productId`, `preferredIntegratedPlatform`, `integratedPlatforms`.

Voice / party specific bridge traffic is covered in the voice docs.
