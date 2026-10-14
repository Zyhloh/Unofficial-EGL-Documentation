# Environments

EGL v2 builds one endpoint table at startup (`eglv2_lib::config::EndpointUrls`, built from `EnvironmentConfig`). There are two compiled host sets: **prod** and **gamedev**. The `ci` environment uses the gamedev host set (the table builder only branches on "prod or not"); the one exception is the feedback ingest stage (`/prod` vs `/ci`).

## Selecting the environment

| Source (`EnvironmentConfig.source`) | How |
| --- | --- |
| `default` | `prod` |
| `persisted` | `set_environment` (`{ env }`) writes `environment` into `settings/app-settings.json`, then the frontend relaunches. Staff-only UI (Settings > EG Staff) |
| `cliOverride` | `-epicenv=<prod\|production\|gamedev\|game-dev\|ci>` on the command line. `set_environment` fails with `Cannot change environment when CLI override is active` |

`get_environment_config` returns `{ "value": "prod", "source": "default" }`. Valid values (frontend list): `prod`, `gamedev`, `ci`.

Switching environment does not sign out: `auth.json` is keyed by environment (`Switching environment (no sign-out, env-keyed auth.json preserves both sessions)`), and the access token is stored per environment (`auth/access-token-prod.dpapi`). Caches also live under `cache/<env>/`.

## Endpoint table

Keys are the names accepted by `-baseurl.<key>=<url>` (see [Overrides](#overrides)).

| Key | Prod | Gamedev / CI | Used for |
| --- | --- | --- | --- |
| `library_service` | https://library-service.live.use1a.on.epicgames.com | https://library-service-gamedev.aeee.dev.use1a.on.epicgames.com | [Library Service](../EpicGames/LibraryService): items, collections, tags, playtime, state token |
| `catalog_service` | https://catalog-public-service-prod06.ol.epicgames.com | https://catalogv2-public-service-gamedev.ol.epicgames.net | [Catalog Service](../EpicGames/CatalogService) |
| `account_service` | https://account-public-service-prod03.ol.epicgames.com | https://account-public-service-common-gamedev.ol.epicgames.net | [Account Service](../EpicGames/AccountService): OAuth, account info |
| `website` | https://www.epicgames.com | https://epicgames-gamedev.ol.epicgames.net | `/id/authorize`, `/id/register`, `/id/exchange`, `/id/link`, `/store`, `/account/parental-controls` ([Sign In](Flows/SignIn.md)) |
| `launcher_service` | https://launcher-public-service-prod06.ol.epicgames.com | https://launcher-public-service-gamedev.aeee.dev.use1a.on.epicgames.com | [Launcher Service](../EpicGames/LauncherService): `/launcher/api/public/assets/v2` |
| `store` | https://store.epicgames.com | https://store.epicgames-gamedev.ol.epicgames.net | `store-webview` content |
| `checkout` | https://launcher.store.epicgames.com/purchase | https://launcher.store.epicgames-gamedev.ol.epicgames.net/purchase | `checkout-overlay` ([Purchase](Flows/Purchase.md)) |
| `fab` | https://www.fab.com | https://www.fab-public.cceb.dev.use1a.on.epicgames.com | `fab-webview` content (`/plugins/egl`) |
| `fab_api` | https://www.fab.com | https://fab.cceb.dev.use1a.on.epicgames.com | [Fab](../EpicGames/Web/Fab) library + artifact manifests |
| `order_processor` | https://orderprocessor-public-service-ecomprod01.ol.epicgames.com | https://orderprocessor-public-service-gamedev.ol.epicgames.net | [Order Processor](../EpicGames/OrderProcessorService): quick purchase |
| `entitlement` | https://entitlement-public-service-prod08.ol.epicgames.com | https://entitlement-public-service-gamedev.ol.epicgames.net | [Entitlement Service](../EpicGames/EntitlementService) |
| `eula_tracking` | https://eulatracking-public-service-prod06.ol.epicgames.com | https://eulatracking-public-service-gamedev.ol.epicgames.net | [EULA Tracking](../EpicGames/EulaTrackingService) |
| `epic_dev` | https://api.epicgames.dev | https://api-gamedev.ol.epicgames.net | [EOS auth](../EpicGames/EOSAuthService) `/auth/v1/oauth/token`, [telemetry](../EpicGames/DataRouterService/Telemetry/SendEvents.md) `/telemetry/data`, social overlay `/overlay-override/v1/launcher-eglv2.html` |
| `connect_ws` | wss://connect.epicgames.dev | wss://connect-gamedev.ol.epicgames.net | [Epic Connect](Social/Connect.md) websocket |
| `presence_service` | https://presence-public-service-prod.ol.epicgames.com | https://presence-public-service-gamedev.ol.epicgames.net | [Presence Service](../EpicGames/PresenceService) |
| `feedback_ingest` | https://77m13yhhad.execute-api.us-east-1.amazonaws.com/prod | https://qv4w0ux1dl.execute-api.us-east-1.amazonaws.com/ci | Feedback reports, `POST /api/v2/reports` (`submit_feedback`). Also overridable by `EGL_FEEDBACK_INGEST_HOST` and the `feedback-ingest-url` flag |
| `e3s_service` | https://e3s-prod.social.live.on.epicgames.com | https://e3s-gamedev.social.dev.on.epicgames.com | `/api/v1/coordinates` (game-invite weblink coordinates, `src\api\e3s.rs`) |
| `data_storage` | https://datastorage-public-service-liveegs.live.use1a.on.epicgames.com | https://datastorage-public-service-gamedev.ol.epicgames.net | [Data Storage](../EpicGames/DataStorageService): cloud saves |
| `partner_integration` | https://partnerintegration-public-service-prod.ol.epicgames.com | https://partnerintegration-public-service-gamedev.ol.epicgames.net | [Partner Integration](../EpicGames/PartnerIntegrationService) (base path `/partnerintegration`) |
| `ecommerce_integration` | https://ecommerceintegration-public-service-ecomprod02.ol.epicgames.com | https://ecommerceintegration-public-service-gamedev.ol.epicgames.net | [Ecommerce Integration](../EpicGames/EcommerceIntegrationService) (base path `/ecommerceintegration`) |
| (fixed) | https://datarouter.ol.epicgames.com | same | [Data Router](../EpicGames/DataRouterService) `/datarouter/api/v1/public/data`. Not overridable, no gamedev variant |

`fab` cannot be overridden with `-baseurl` (it is missing from the override key list).

## Hosts outside the table

Hardcoded in the exe, same in every environment:

| Host | Used for |
| --- | --- |
| https://content-download-egs.distro.on.epicgames.com/Builds/EGLv2 | [Self Update](SelfUpdate.md): `stable-target.json`, `<version>/<platform>/buildinfo.json`, `patch-notes/<locale>.json`, partner client installers |
| https://content-download-egs-gamedev.aeee.dev.use1a.on.epicgames.com | Gamedev counterpart (CSP allow-list) |
| https://fortnite-app-service.eeef.live.use1a.on.epicgames.com | [Fortnite App Service](../EpicGames/FortniteAppService): `/api/v1/apps` |
| https://store-content.ak.epicgames.com | [Store Content](../EpicGames/StoreContentService): product pages + product mapping |
| https://store.epicgames.com/graphql | [Store GraphQL](../EpicGamesStore/GraphQL/GetMediaRef.md) (trailer media refs) |
| https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/linux-manifest.txt | Linux installer manifest |
| https://api.igdb.com/v4/games, https://id.twitch.tv/oauth2/token | [IGDB](../ThirdParty/IGDB) metadata for external (Steam / Xbox) games |
| https://quixel-megascans-static.s3.us-west-2.amazonaws.com/fab/manifest/prod/plugins_v1.json | Fab DCC plugin manifest |
| https://o10593.ingest.us.sentry.io | [Sentry](../ThirdParty/Sentry) |
| https://api.mixpanel.com | Mixpanel `/track?ip=0` (`telemetry::sinks::mixpanel`) |
| https://clientsdk.launchdarkly.com, https://clientstream.launchdarkly.com, https://events.launchdarkly.com | LaunchDarkly mobile SDK (feature flags, see [Architecture](Architecture.md#feature-flags)) |
| https://epicgamesinc.cloudflareaccess.com | Staff only: "EGS Zero Trust" store sign-in (`egs_zero_trust`) |
| https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton10-34/GE-Proton10-34.tar.gz | Linux: Proton runtime (`install_proton_runtime`) |
| https://media-cdn.epicgames.com | CSP `connect-src` only (store media) |

The social overlay web app has its own host list, see [Social Overview](Social/Overview.md).

## HTTP client

| Client | User-Agent |
| --- | --- |
| Rust API client (`eglv2_lib::api::client`, also FN deployment, launcher services) | `EpicGamesLauncherV2/0.95.1+ge288862 (windows)` |
| Store GraphQL / store content | `EpicGamesLauncher/2 (+https://store.epicgames.com)` |
| `social` webview | `EpicGamesLauncher/0.95.1+ge288862 (windows)` |
| Other webviews (`store-webview`, `fab-webview`, `checkout-overlay`, ...) | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/<N>.0.0.0 Safari/537.36 Edg/<N>.0.0.0 EpicGamesLauncher/0.95.1+ge288862` where `<N>` is the WebView2 major version (fallback `130` when unknown or below 67) |
| Data Router sink | `<AppID>/<AppVersion> <...>` (template `{}/{} {}`, third value not resolved) |

The `EpicGamesLauncher/<ver>` token is how Store / Fab pages detect "launcher mode". The store bridge advertises `clientversion` `19.0.0` to the store (`bridge_get_client_version`), not the real version.

Common headers sent by the API client:

| Header | Value |
| --- | --- |
| `Authorization` | `Bearer <EG1 access token>` (see [Token Storage](Auth/TokenStorage.md)) |
| `DPoP` | DPoP proof when enabled, see [DPoP](Auth/DPoP.md) |
| `X-Epic-Correlation-ID` | Per-request correlation id (logged as `correlation_id`) |
| `Accept-Language` | UI locale (store content, Fab library) |

Retry policy (`src\api\client.rs`): 5xx retried with backoff except on non-idempotent requests, 401 triggers one token refresh then retry, 429 honours `retry-after`, transport errors retried while attempts remain.

## Overrides

| Mechanism | Effect |
| --- | --- |
| `-debugtools` / `-debugtoolsaccess` | Arms the overrides below and webview devtools |
| `-baseurl.<key>=<url>` | Replaces one table entry. Needs `-debugtools`. URL must be https/wss (http/ws only to loopback), no credentials, query or fragment |
| `-social-overlay-url=<url>` | Replaces the overlay page. Needs `-debugtools`; must be an absolute https URL on `*.epicgames.dev` / `*.ol.epicgames.net` or loopback. Same rule for the `socialOverlayUrl` setting |
| `-overrideepicapp=`, `-overrideepicenv=` | Passed through to games (`OverrideEpicApp` / `OverrideEpicEnv`), alphanumeric, `-`, `_` only |
| `EGL_MOCK_SERVICES_URL`, `-mock-services` | Mock backend, only in builds compiled with the feature |

Environment variables read by the exe: `EGL_SENTRY_DSN`, `EGL_EOS_CLIENT_ID`, `EGL_EOS_CLIENT_SECRET`, `EGL_EOS_ENCRYPTION_KEY`, `EGL_EOS_PRODUCT_ID`, `EGL_EOS_SANDBOX_ID`, `EGL_EOS_DEPLOYMENT_ID`, `EGL_EOS_BACKEND_ENVIRONMENT`, `EGL_IGDB_CLIENT_ID`, `EGL_IGDB_CLIENT_SECRET`, `EGL_SISU_CLIENT_ID`, `EGL_SISU_CLIENT_SECRET`, `EGL_SISU_SCOPES`, `EGL_SISU_REDIRECT_HOST`, `EGL_SISU_REDIRECT_PORT`, `EGL_SISU_REDIRECT_PATH`, `EGL_SISU_BROWSER_SINK`, `EGL_LD_OVERRIDES`, `EGL_DEBUG_TOOLS`, `EGL_SIMULATE_CABINED`, `EGL_MOCK_SERVICES_URL`, `EGL_DESTRUCTIVE_UPDATES`, `EGL_UPDATE_STREAM_THRESHOLD`, `EGL_PROTON_PIN`, `EGL_FEEDBACK_INGEST_HOST`, `EGL_DISABLE_DPOP`, `EGL_DISABLE_DPOP_NONCE`, `EGL_DISABLE_LD`, `EGL_DISABLE_SENTRY`, `EGL_DISABLE_SELF_UPDATE`, `EGL_DISABLE_SOCIAL_PANEL`, `EGL_SOCIAL_OVERLAY_URL`, `EGL_DISABLE_TELEMETRY`, `EGL_DISABLE_PLAYTIME_REPORTING`, `EGL_DISABLE_STORE_PREWARM`, `EGL_ENABLE_TRACKING_PREVENTION`, `EGL_IMAGE_FETCH_CONNECTIONS`, `EGL_IMAGE_CDN_RESIZE`, `EGL_STORAGE_PROBE_PATHS`, `EGL_TEST_HARNESS_PORT`, `EGL_WEBVIEW2_REMOTE_DEBUGGING_PORT`, `EGL_FORCE_NAV_PROBE`, `EGL_OVERLAY_ADAPTER`, `EGL_OVERLAY_SWAP`, `EGL_GDK_BACKEND`, `EGL_STARTUP_BENCH_OUT`, `EGL_STARTUP_BENCH_UNTIL`, `EGL_STARTUP_BENCH_TIMEOUT_MS`, `EGL_INSTALL_API_INSECURE`, `EGL_V1_DISPOSAL`, `EGL_V1_UNINSTALL_FOR_REAL`, `EGL_URL_PROTOCOL_RECLAIM`, `EGLV2_FORCE_KEYRING`, `EGLV2_LOCALE`, `RUST_LOG`. Several of the `EGL_EOS_*` / `EGL_IGDB_*` / `EGL_SISU_*` names look like build-time inputs (inferred from their grouping with `EGL_SENTRY_DSN`).

Command-line flags (parsed in `eglv2_lib::command_line`): `-debugtools`, `-debuglogging`, `-epicenv=`, `-applabel=`, `-baseurl.<key>=`, `-social-overlay-url=`, `-overrideepicapp=`, `-overrideepicenv=`, `-disable-dpop`, `-disable-dpop-nonce`, `-dpop-iat-offset-seconds=`, `-dpop-suppress-nonce-harvest`, `-dpop-seed-bad-nonce`, `-disable-ld`, `-ld-overrides`, `-disable-telemetry`, `-disable-social-panel`, `-disable-self-update`, `-self-update-dev`, `-patch-to-version=`, `-patch-lazy`, `-simulate-cabined`, `-sentry-test=<panic|js-error|unhandled-rejection|ipc-error>`, `-eosverbose`, `-installer-session-id=<uuid v4>`, `-mock-services`. Both `-x` and `--x` spellings are accepted.

## What changed from the UE-based launcher

| Area | v1 (UE launcher) | v2 |
| --- | --- | --- |
| Library | `/library/api/public/items` | `/library/api/public/v2/items`, collections, tags and `stateToken` on `library-service.live.use1a.on.epicgames.com`, see [Library](Flows/Library.md) |
| Catalog gamedev | `catalog-public-service-gamedev` | `catalogv2-public-service-gamedev.ol.epicgames.net` |
| New `*.on.epicgames.com` hosts | - | `datastorage-public-service-liveegs.live.use1a`, `fortnite-app-service.eeef.live.use1a`, `e3s-prod.social.live`, `content-download-egs.distro`, `selective-download-egs.distro`, `library-service-gamedev.aeee.dev.use1a`, `launcher-public-service-gamedev.aeee.dev.use1a`, `www.fab-public.cceb.dev.use1a` |
| EOS | Launcher was not an EOS client | Full EOS SDK client (`api.epicgames.dev` token, `wss://connect.epicgames.dev`, EOS overlay for social) |
| Self update | BuildPatch from launcher assets | Tauri updater: `buildinfo.json` + signed NSIS setup on `content-download-egs.distro.on.epicgames.com/Builds/EGLv2`, gated by LaunchDarkly |
| Telemetry | Data Router | Data Router (`AppID=LauncherV2`), EOS telemetry (`api.epicgames.dev/telemetry/data`), Mixpanel, Sentry |
| Feedback | - | AWS API Gateway `/api/v2/reports` |
