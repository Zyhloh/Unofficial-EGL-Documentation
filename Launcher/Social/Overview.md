# Social Overlay - Overview

The friends / chat / party panel in EGL v2 is not part of the launcher frontend. It is Epic's hosted Social Overlay web app (Sentry release `social-overlay@2.9.2`, build `48a8a998c785c6c7358b56ddc82474ca23ae565f`) loaded into a child Tauri webview labelled `social`.

## Loading

1. The shell calls `social_overlay` with `action` `show` / `hide` / `reload` (`socialOverlay` in the frontend bindings). Rust (`social::windows::panel`, `social.panel.open_or_focus`) creates the `social` webview as a child of `main` (`add_child`).
2. The webview loads `https://api.epicgames.dev/overlay-override/v1/launcher-eglv2.html` (gamedev: `https://api-gamedev.ol.epicgames.net`). The launcher appends query parameters; the exe string table holds `product_id`, `product_version` (`0.95.1+ge288862`), `deployment_id`, `os_name` (`Windows`), `os_version`, `integrated_platform_name` (`egs`), `sdk_version`, `sdk_cl_number`, `user_id` (exact ordering/values inferred from the string table).
3. The page is a tiny HTML shell that pulls `app-Z6xvdTog.js`, `client-HGNfKPY5.js`, `network-status-B3JBXhBv.js` and CSS from `https://social-overlay.ol.epicgames.com/48a8a998c785c6c7358b56ddc82474ca23ae565f-social-web-component/assets/`, plus `sw-registration-launcher-*.js` which registers the service worker `sw-launcher-eglv2.js` with scope `/overlay-override/v1/`. Manifest: `https://api.epicgames.dev/overlay-override/v1/manifest-eglv2.webmanifest`.
4. Before any page script runs, the launcher injects initialization scripts (embedded in the exe): a console forwarder (`social_webview_console_log`), a layout self-check, `social-bridge.js` (defines `window.ue.social`, `window.ue.common`, `window.ue.launcher`) and `webview-tab-focus.js`. The EOS SDK overlay bridge script is injected after them and merges its own methods onto `window.ue.social`. See [Bridge](Bridge.md).
5. The app reads from its own URL: `locale`, `sdk_cl_number`, `os_name`, `product_version`, `product_id`, `launcher_product`, `exchange_code`. `platformName` is hardcoded to `egs`, `productName` to `Epic Games Launcher`.
6. Once painted, `social-bridge.js` calls `bridge_notify_content_painted` (`{ label: "social" }`) so the shell fades its loading curtain.

Chat pop-out uses `window.open("windowed-chat.html?...")` from the same host; on Windows it becomes a Tauri window labelled `social-chat` that borrows the broker through `window.opener.window.social.broker`.

## Architecture

The app is a React + Redux store fed by a "broker" (`window.social.broker`). Modules register data providers, intent handlers and effects. Data reaches it from four places:

| Source | What |
| --- | --- |
| Native bridge (`window.ue.*`) | account info, tokens, SDK state (friends from platforms, game invites, lobbies), launcher window/idle/connection state, notifications, badge |
| Epic Connect websocket | realtime friends, presence, chat, party, social ban and parental-control events. See [Connect](Connect.md) |
| REST services | chat, presence, KWS settings, social ban, moderation, Emerald, Compass, public key, SOCS, ITS, party |
| GraphQL | friends list / mutations, account lookup, search. See [GraphQL](GraphQL.md) |

## Service base URLs (hardcoded in `app-Z6xvdTog.js`)

| Constant | URL |
| --- | --- |
| `EPIC_CONNECT_URL` | `wss://connect.ol.epicgames.com` |
| `EPIC_SERVICE_GRAPHQL_URL` | `https://api.epicgames.dev/overlay-graphql/v1/graphql` |
| `EPIC_K3S_ENDPOINT_URL` | `https://api.kws.ol.epicgames.com` |
| `EPIC_LAUNCHDARKLY_ENDPOINT` | `https://api.epicgames.dev/overlay-launch-darkly` |
| `EPIC_PARTY_ENDPOINT_URL` | `https://api.epicgames.dev/epic/party` |
| `EPIC_PUBLIC_KEY_SERVICE_URL` | `https://publickey-service-prod.ecbc.live.use1a.on.epicgames.com` |
| `EPIC_REPORTING_ENDPOINT_URL` | `https://compass-service-prod.ecosec.on.epicgames.com/compass` |
| `EPIC_SOCIAL_BAN_SERVICE_ENDPOINT_URL` | `https://social-ban-public-service-prod.social.live.on.epicgames.com/socialban` |
| `EPIC_CHAT_SERVICE_ENDPOINT_URL` | `https://api.epicgames.dev/epic/chat` |
| `EPIC_MODERATION_SERVICE_ENDPOINT_URL` | `https://moderation-ingest-service-prod-external.ecbc.live.use1a.on.epicgames.com` |
| `EPIC_SOCS_ENDPOINT_URL` | `https://api.epicgames.dev/epic/socs` |
| `EPIC_PRESENCE_SERVICE_ENDPOINT_URL` | `https://api.epicgames.dev/epic/presence` |
| `EPIC_ITS_SERVICE_ENDPOINT_URL` | `https://api.epicgames.dev/epic/interactions` |
| `EPIC_EMERALD_SERVICE_ENDPOINT_URL` | `https://emerald-service-live.ecosec.on.epicgames.com` |
| `EPIC_AVATARS_SERVICE_ENDPOINT_URL` | `https://avatars-service-prod.social.live.on.epicgames.com` |
| `EPIC_AVATARS_FN_DEPLOYMENT_ID` | `62a9473a2dca46b29ccf17577fcf42d7` |

The avatars client is configured but this build issues no avatars-service request; the deployment id is only sent to Epic Connect (`avatarFnDeploymentId`). `e3s-prod.social.live.on.epicgames.com` is not referenced by the overlay.

## HTTP client

Every REST service goes through one wrapper (`ApiClient`, created with `Po(name, init)`, configured at startup with the base URL above):

- URL = base URL + path.
- Headers: `Content-Type: application/json`; `Authorization: Bearer <token>` unless the client is `unauthenticated`; `X-Epic-Agent: epic-social` and `X-EPIC-CORRELATION-ID: <uuid v4>` unless the call passes `includeEpicHeaders: false` (Emerald, moderation and public key calls do).
- Token: `elevated` by default. The elevated token is read from `window.ue.common.getsignedinuser().accesstoken` on every call (the launcher's EG1 account access token, via `bridge_get_signed_in_user`); without that bridge it falls back to `account-info.elevatedToken` / `accessTokenOverride` from the SDK. `nonElevated` is the SDK's `account-info.authToken` and is used only by the achievements client.
- `referrerPolicy: no-referrer`. Presence uses `credentials: "omit"`.
- Retry: up to 5 attempts, delay `min(100..600ms * 2^n, 2000ms)`; honours `Retry-After`; retries 5xx and 429 (1s), plus per-call `retriableStatuses` (chat conversation reads add 403). After a network failure while offline it waits up to the offline deadline for `online`.
- Errors: a JSON body carrying `errorCode` is thrown as `UpstreamServiceError` with `responseStatus` and the response `X-EPIC-CORRELATION-ID`.

GraphQL uses urql with `X-Epic-Agent: epic-social`, `Authorization: Bearer <elevated token>`, `credentials: include`.

## Related pages

- [Bridge](Bridge.md) - native bridge API
- [Connect](Connect.md) - realtime websocket
- [GraphQL](GraphQL.md) - friends/account GraphQL operations
- [Signing](Signing.md) - chat message signing and verification
- [Chat](../../EpicGames/ChatService/README.md), [Presence](../../EpicGames/PresenceService/README.md), [Friends](../../EpicGames/FriendsService/README.md), [Social Ban](../../EpicGames/SocialBanService/README.md), [KWS](../../EpicGames/KWS/README.md), [Moderation](../../EpicGames/ModerationService/README.md), [Emerald](../../EpicGames/EmeraldService/README.md), [Compass](../../EpicGames/CompassService/README.md), [Public Key](../../EpicGames/PublicKeyService/README.md)
