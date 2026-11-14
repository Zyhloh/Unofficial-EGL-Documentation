# Social Overlay - Overview

The friends / chat / party panel in EGL v2 is not part of the launcher frontend. It is Epic's hosted Social Overlay web app (Sentry release `social-overlay@2.9.2`, build `48a8a998c785c6c7358b56ddc82474ca23ae565f`) loaded into a child Tauri webview labelled `social`.

## Loading

1. The shell calls `social_overlay` with `action` `show` / `hide` / `reload` (`socialOverlay` in the frontend bindings). Rust (`social::windows::panel`, `social.panel.open_or_focus`) creates the `social` webview as a child of `main` (`add_child`).
2. The webview loads `https://api.epicgames.dev/overlay-override/v1/launcher-eglv2.html` (gamedev: `https://api-gamedev.ol.epicgames.net`). The SDK appends query parameters. Real URL from the launcher's WebView2 history (0.115):

   ```
   https://api.epicgames.dev/overlay-override/v1/launcher-eglv2.html?product_id=42c61cfdc3d24af5a8333b3284d47240&product_version=0.115.0%2Bgd6d2ef8&deployment_id=83364c64d38841d49c4de2f6f0eb3360&os_name=Windows&os_version=10.0.26300.9974.64bit&integrated_platform_name=egs&sdk_version=1.19.4230.0&sdk_cl_number=57929184&user_id=<accountId>&locale=en
   ```

   `locale` comes last. No `exchange_code` is in the stored URL. The names are confirmed by the live EOS [Product Config](../../EpicGames/EOSSDKConfigService/Config/ProductConfig.md), `client.UIClient.SocialURLQueryParamNames`: `OSName` → `os_name`, `OSVersion` → `os_version`, `ProductId` → `product_id`, `ProductVersion` → `product_version`, `DeploymentId` → `deployment_id`, `SDKVersion` → `sdk_version`, `SDKCLNumber` → `sdk_cl_number`, `IntegratedPlatformName` → `integrated_platform_name`, `UserId` → `user_id`, `ExchangeCode` → `exchange_code`. The exchange code comes from the EOS SDK (`FSocialOverlayJavascript::GenerateSocialUrlInfo: Successfully got exchange code`).
3. The page is a tiny HTML shell that pulls `app-<hash>.js`, `client-<hash>.js`, `network-status-<hash>.js`, `app-eglv2-<hash>.css` and `client-eglv2-<hash>.css` from `https://social-overlay.ol.epicgames.com/<build>-social-web-component/assets/` (build `96211b375055f1df17340f9aa9162510c71d90e3` in November 2026, `48a8a998c785c6c7358b56ddc82474ca23ae565f` in October; the file hashes change with every build), plus `sw-registration-launcher-*.js` which registers the service worker `sw-launcher-eglv2.js` with scope `/overlay-override/v1/`. Manifest: `https://api.epicgames.dev/overlay-override/v1/manifest-eglv2.webmanifest`.
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
| `EPIC_AVATARS_SERVICE_ENDPOINT_URL` | `https://api.epicgames.dev/epic/avatar` (overlay build `96211b37...`; `https://avatars-service-prod.social.live.on.epicgames.com` in `48a8a998...`) |
| `EPIC_AVATARS_FN_DEPLOYMENT_ID` | `9c9906b240c74a92a6b9100d6e4ccbd0` (`62a9473a2dca46b29ccf17577fcf42d7` in build `48a8a998...`) |

Overlay build `48a8a998...` configured an avatars client but sent no request with it; the deployment id only went to Epic Connect (`avatarFnDeploymentId`). Build `96211b37...` uses it: own avatar settings, fallback avatar, and avatar assignments for friends, party members and group chats, see [Avatar Service](../../EpicGames/AvatarService). `e3s-prod.social.live.on.epicgames.com` is not referenced by the overlay.

## HTTP client

Every REST service goes through one wrapper (`ApiClient`, created with `Po(name, init)`, configured at startup with the base URL above):

- URL = base URL + path.
- Headers: `Content-Type: application/json`; `Authorization: Bearer <token>` unless the client is `unauthenticated`; `X-Epic-Agent: epic-social` and `X-EPIC-CORRELATION-ID: <uuid v4>` unless the call passes `includeEpicHeaders: false` (Emerald, moderation and public key calls do).
- Token: `elevated` by default. The elevated token is read from `window.ue.common.getsignedinuser().accesstoken` on every call (the launcher's EG1 account access token, via `bridge_get_signed_in_user`); without that bridge it falls back to `account-info.elevatedToken` / `accessTokenOverride` from the SDK. `nonElevated` is the SDK's `account-info.authToken` and is used only by the achievements client.
- Unused token service: the bundle also has a `token-exchange` client with `POST /exchange` (`{exchangeCode, codeVerifier}`) and `POST /refresh` (`{refreshToken}`), unauthenticated and without Epic headers. Its base URL comes from the build-time `EPIC_TOKEN_EXCHANGE_URL`, which is empty in both captured builds (`48a8a998`, `96211b37`), so in the launcher it never reaches a real host. The launcher's bridge token is used instead.
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
