# Architecture

EGL v2 ("eglv2", version `0.95.1+ge288862`, Tauri identifier `com.epicgames.eglv2`, product name `Epic Games Launcher`) is a full rewrite of the UE-based launcher.

| Layer | What |
| --- | --- |
| Backend | Rust crate `eglv2_lib` (+ `eglv2-context`, `eglv2-manifest`, `eglv2_models`, `eglv2_macros`), Tauri 2, tokio, reqwest / hyper, axum (local install API). Built by `egl-runner` CI. Source paths leak as `src\...rs`, modules as `eglv2_lib::...` |
| Frontend | React + Vite SPA embedded in the exe (served from `tauri.localhost`), react-router, TanStack Query, zustand, i18next. Sentry release `epic-games-launcher@0.95.1+ge288862` |
| Web runtime | WebView2 (Windows), shared user data folder `EBWebView`. macOS and Linux builds exist (`macos-aarch64`, Linux `deb` / `appimage`, Proton for Windows games) |
| EOS | `EOSSDK-Win64-Shipping.dll` loaded at startup (DLL verified in an `eossdk-relay` thread), used for EOS auth, the social overlay bindings, voice (RTC) and EOS telemetry. See [EOS](Auth/EOS.md) |
| Remote web apps | Store (`store.epicgames.com`), Fab (`www.fab.com/plugins/egl`), checkout (`launcher.store.epicgames.com/purchase`), Social Overlay (`api.epicgames.dev/overlay-override/v1/launcher-eglv2.html`) |

All service hosts and how to switch them: [Environments](Environments.md). Commands and events between frontend and backend: [IPC](IPC/README.md). Files on disk: [Local Data](LocalData.md).

## Windows and webviews

| Label | Kind | Content |
| --- | --- | --- |
| `main` | Window | Shell window. Hosts the embedded frontend and the child webviews below |
| `shell` | Webview | The React app (`index.html`) |
| `store-webview` | Child webview of `main` | Remote store; store bridge injected ([Purchase](Flows/Purchase.md)) |
| `fab-webview` | Child webview | Remote Fab app; Fab bridge injected |
| `social` | Child webview | Social Overlay web app, see [Social Overview](Social/Overview.md) |
| `social-chat` | Window | Chat pop-out of the overlay |
| `checkout-overlay` | Child webview | Single-instance checkout tab |
| `toast-window` | Window | Non-activating toast popups (`toast_harden_window`, `toast:*` events) |
| `downloads-window` | Window | Detached downloads list |
| `oauth-login` | Webview | Embedded sign-in page, see [Sign In](Flows/SignIn.md) |
| `egs-zero-trust-signin` | Window | Staff only: Cloudflare Access sign-in for the EGS v2 store |
| `perf-monitor` | Window | Developer perf overlay |

Content webviews are created by the frontend (`plugin:webview|create_webview`) or by Rust (`store_create_webview`, `fab_create_webview`, `social_overlay`). Rust tags them for the perf monitor (`register_webview_label`), injects init scripts (bridges, scrollbar normalization, keyboard tab-focus hand-off, console forwarders), applies a WebView2 tracking-prevention level (`EGL_ENABLE_TRACKING_PREVENTION`) and recovers "ghost" webviews (`webview::builder::ghost_recovery`). Remote origins only reach IPC through Tauri capabilities (`social-bridge-remote` for `https://api.epicgames.dev` / `https://api-gamedev.ol.epicgames.net`, and a store bridge capability).

User-Agents per webview: [Environments](Environments.md#http-client).

CSP of the shell: `script-src 'self' https://api.epicgames.dev https://*.epicgames.dev https://api-gamedev.ol.epicgames.net`; `connect-src` allows `ipc:`, `http://ipc.localhost`, `media-cdn.epicgames.com`, Mixpanel, LaunchDarkly, `github.ol.epicgames.net`, both `content-download-egs` hosts, `*.ingest.us.sentry.io`, EOS (`api.epicgames.dev`, `connect.epicgames.dev`), `notifications-service-prod06/gamedev` websockets, `friends-public-service-prod06/gamedev`, `presence-public-service-prod/gamedev`; `frame-src https://www.youtube-nocookie.com`. Images come through the custom `img:` protocol (`http://img.localhost/<md5>`) backed by the image cache.

## Startup

Named phases in the log (`run:*`, `setup:*`): context, single instance, roaming migration (`%APPDATA%` -> `%LOCALAPPDATA%`), log init (`logs\EpicGamesLauncher_<date>.log`, older segments pruned), install source, sysinfo, tracing, Sentry, bootstrap auth, DPoP signer ([DPoP](Auth/DPoP.md)), settings, telemetry, EOS relay / DLL verify, window. The self-update boot gate runs before the instance is claimed ([Self Update](SelfUpdate.md)). The frontend reports its own phases through `record_frontend_startup_phase`.

Single instance: tauri `single-instance` plugin (`single_instance::windows_impl`). A second process forwards its arguments (e.g. a deep link) to the running one, which focuses its window (`Deep-link focus: main window could not be resolved` when it cannot). `--self-update-dev` skips the plugin. Start minimized from autostart keeps the window in the tray (`--autostart`).

Tray: recent games and auth state (`update_tray_menu`), actions as `tray://` events. Taskbar badge / overlay icon for voice party and downloads (`social::voice_party::windows::taskbar_badge`).

## Local install API

`eglv2_lib::install_api` runs an HTTP server (axum) on loopback for games and Epic tools (e.g. `epiconlineservicesinstallhelper.exe`): non-loopback peers are dropped, every request needs the `x-epic-machine-secret` header (`InstallApi.MachineSecretRejected`), the port + secret are advertised in an `api.json` record (`ApiFile { ..., machineSecret, version }`) that is removed on shutdown. Routes seen: `/api/v1/installation`, `/json/api/v1/installation`, `.../operations/<id>`. Request bodies (`InstallRequest`: `type`, `dir`, `platform`, `sandboxId`, `itemId`, `artifactId`, `tags`, `actions`, `downloadRateLimitBps`; `ManifestInfoRequest`: `tagSets`, `installationId`, `apps`) let a caller install / query a title through the launcher. Launch flags passed through it are filtered (`InstallApi.ReservedLaunchFlagDropped`, `SmuggledLaunchFlagDropped`). Record location and full route list were not resolved; `EGL_INSTALL_API_INSECURE` relaxes the secret check (inferred from the name).

## Telemetry

Events go through one dispatcher (`telemetry::dispatcher`) to several sinks, each with a sample-rate flag. Session log line: `telemetry pipeline initialized machine_bucket=0.79 mixpanel_enabled=true datarouter_enabled=true eos_datarouter_enabled=true`.

| Sink | Endpoint |
| --- | --- |
| Data Router | [Send Data](../EpicGames/DataRouterService/DataRouter/SendData.md), `AppID=LauncherV2` |
| EOS Data Router | [Telemetry Send Events](../EpicGames/DataRouterService/Telemetry/SendEvents.md) |
| Mixpanel | `POST https://api.mixpanel.com/track?ip=0`, form body `data=<base64 JSON>`, project token `5c241d3ffdc4cb50a9d52f92c885b12f`, props `distinct_id`, `$device_id`, `$insert_id`, `$user_id`, `time`, `mp_lib=rust-backend` |
| Sentry | [Sentry](../ThirdParty/Sentry/Envelope/Send.md) |

Events are spooled to `telemetry\spool\*.jsonl` first. `-disable-telemetry`, `EGL_DISABLE_TELEMETRY` turn egress off.

## Feedback

`submit_feedback` collects logs (`feedback::collect`), requests a slot from the `feedback_ingest` host ([Request Slot](../EpicGames/FeedbackService/Reports/RequestSlot.md)) and uploads `logs.zip` to the returned presigned S3 POST ([Upload Report](../EpicGames/FeedbackService/Reports/UploadReport.md)). Enabled by the `feedback-enabled` flag; `feedback-ingest-url` overrides the host. History in `feedback\history-<env>.json`.

## Feature flags

LaunchDarkly Rust client (`launchdarkly::actor`, SDK `3.11.1` per the live log `LaunchDarkly client started (non-blocking) sdk_version=3.11.1 env=Prod`), mobile endpoints ([Stream](../ThirdParty/LaunchDarkly/Mobile/StreamEval.md), [Poll](../ThirdParty/LaunchDarkly/Mobile/PollEval.md), [Events](../ThirdParty/LaunchDarkly/Events/Send.md)). Three mobile keys are compiled in (one per environment, mapping not resolved). Contexts: a `machine` context with `releaseChannel`, plus the user ([context shape](../ThirdParty/LaunchDarkly/Mobile/StreamEval.md#context)). Values are persisted to `cache\<env>\launchdarkly\flags.json`; `ld-overrides.json(c)` (`-ld-overrides`, `EGL_LD_OVERRIDES`) overrides locally, release builds refuse some keys. `-disable-ld` / `EGL_DISABLE_LD` serve registry defaults. IPC: `get_feature_flags`, `get_flag_overrides`, `flag-changed-event`, `ld-status-changed-event`.

The social overlay evaluates its own flags server-side: [Overlay Feature Flags](../EpicGames/OverlayFeatureFlagsService/Features/GetFeatures.md).

Flag registry (frontend `SettingsModal`, defaults are what the client uses before LaunchDarkly answers):

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `developer-mode` | boolean | `false` | Unlocks the developer settings section and the build/channel/environment pills. Internal (non-release) builds always qualify regardless, and a release build ignores this override. |
| `login-email-gate-enabled` | boolean | `true` | Master switch for the email allow-list gate at sign-in. Set false to open the gate to everyone. A release build ignores this override. |
| `login-email-gate-allowed` | boolean | `false` | Whether the current user is in the allowed segment for the email gate. Set true to let yourself through the gate. A release build ignores this override. |
| `whats-new-modal-enabled` | boolean | `false` | Kill-switch for the What's New modal at startup. |
| `feedback-enabled` | boolean | `false` | Kill-switch for the in-app log-sharing flow. When on, a "Send feedback" item appears in the shell menu, letting a player upload PII-scrubbed launcher logs to Epic and get a reference code for support. |
| `feedback-ingest-url` | string | `""` | Prod-only override for the feedback ingest slot-request URL (the full URL, path included, used verbatim), so the edge can move without a client release. Empty uses the built-in per-environment endpoint. Must be https on an Epic or AWS host. |
| `presence-mode` | string | `"social-overlay"` | Which sink publishes the user's idle presence. One of 'epic-connect' (launcher-owned Epic Connect transport) or 'social-overlay' (default; the launcher self-publishes nothing and the social overlay app owns the publish). Unknown values coerce to the default. |
| `social-panel` | boolean | `true` | Master gate for the docked social panel feature. Default on. Set false to disable it: the native panel never opens (Windows/macOS/Linux). Distinct from the per-session -disable-social-panel CLI/env kill switch. |
| `game-invites-party-ping` | boolean | `true` | Gate for the party-ping game-invite transport (party.v0.PING). Checked per inbound message; flip live without a restart. |
| `game-invites-legacy` | boolean | `true` | Gate for the legacy matchmaking game-invite transport (Borderlands 3 era). Checked per inbound message. |
| `game-invites-weblink` | boolean | `false` | Gate for the URI/weblink (Sony weblinks) game-invite transport. Checked at deep-link processing time. |
| `self-update-mode` | string | `"disabled"` | Self-update behavior for the launcher itself: 'encouraged' (bottom-bar update and restart button), 'forced' (required update), or 'disabled'. Any other value counts as 'disabled'. |
| `self-update-target-version` | string | `""` | The version the launcher updates to, including the +g hash; it must differ from the running version exactly. Older versions roll back. Empty string means no update. |
| `self-update-cdn-base-urls` | json | `[]` | Array of CDN base URLs the self-update download tries, in order. Empty array means no update, unless the stable-target emergency override is on, which supplies its own CDN. |
| `self-update-forced-hold-minutes` | number | `15` | How long a client already running may wait before starting a forced update download. Each client picks a random point in 0 to this many minutes, so a flag flip does not make the whole install base download at once. Set to 0 for an emergency deprecation that has to move now. |
| `self-update-lazy-hold-minutes` | number | `60` | How long a client may wait before starting a lazy (encouraged) update download. Each client picks a random point in 0 to this many minutes. Wider than the forced window because nothing is on screen during the wait. Set to 0 to start every client at once. |
| `game-update-check-interval` | number | `20` | Minutes between automatic game update checks. |
| `game-update-check-jitter` | number | `1.5` | Randomization multiplier applied to the update-check interval so machines don't all poll at once. |
| `dev-build-polling-tiers` | json | `null` | Developer-only override of the build-polling tier timings. null means use the built-in tiers. |
| `flag-poll-interval-minutes` | number | `15` | How often the launcher polls the flag relay, in minutes. Clamped to 1 minute to 6 hours; a broken value falls back to 15. |
| `telemetry-datarouter-sample-rate` | number | `1` | Share of machines, 0 to 1, that send analytics events and logs to Data Router at all. 0 sends from none, 1 from every machine. |
| `telemetry-datarouter-log-levels` | json | `["event","info","warn","error","fatal"]` | Array of log levels that may reach Data Router as Launcher.Log rows. A level left out stops sending from every machine; "debug" never sends. Named analytics events, Mixpanel and Sentry are not affected ("event" gates only the Launcher.Log row that mirrors an event). An empty array sends no log rows; a value that is not an array reads as every level. |
| `telemetry-mixpanel-sample-rate` | number | `1` | Share of machines, 0 to 1, that send analytics events to Mixpanel at all. |
| `telemetry-eos-datarouter-sample-rate` | number | `1` | Share of machines, 0 to 1, that send the v1-parity eos.social.* stream to the EOS Data Router, whole sessions at a time. |
| `telemetry-sentry-sample-rate` | number | `1` | Share of machines, 0 to 1, that send crash reports and errors to Sentry at all, frontend included. Not closed by consent or -disable-telemetry. |
| `telemetry-heartbeat-interval-secs` | number | `60` | Seconds between App.Heartbeat events. Used only within 15 to 3600; anything else falls back to 60. A change re-arms the heartbeat timer without a relaunch. |
| `develop-news-enabled` | boolean | `false` | Whether Develop's News section is offered on a release build. Default off: the live Unreal Engine feed is unreachable until Web Framework supplies the Cloudflare auth-token header (#3027), so a release build has no content source for it. Internal (non-release) builds always show the section regardless. When off, the section tab, its route and its top-bar entry are all withheld; a stored top-bar layout keeps the entry and it returns when this flips. |
| `cloud-saves-enabled` | boolean | `false` | Launcher-managed cloud saves: pull a game's saves before it launches and after it installs. Default off; on in dev and QA through LaunchDarkly targeting. |
| `partner-ea-uri-scheme` | string | `"auto"` | Selects the URI scheme used to hand off to the EA app. One of 'auto' (default; prefers epic2ea when its handler is registered, else link2ea), 'link2ea' or 'epic2ea' (states a preference that falls back to the other scheme when only that one is registered). Any other value behaves as 'auto'. REQ-PARTNER-164, #4227. |
| `dpop-nonce-enabled` | boolean | `true` | Fleet rollback for DPoP nonce handling and the ens proof claim (ADR-0066). Default on. Set false to turn both off on every launcher; proof of possession itself stays on. Takes effect from the next token request. Never delete the flag in LaunchDarkly: an absent flag reads on. Distinct from the per-machine -disable-dpop-nonce CLI/env switch, which forces it off even when this is true. |

## Services by feature

| Feature | Docs |
| --- | --- |
| Sign-in, tokens, EOS auth | [Sign In](Flows/SignIn.md), [Account Service](../EpicGames/AccountService), [EOS Auth](../EpicGames/EOSAuthService), [Web Id](../EpicGames/Web/Id), [Auth](Auth/Clients.md) |
| Library, catalog, collections, playtime | [Library](Flows/Library.md), [Library Service](../EpicGames/LibraryService), [Catalog Service](../EpicGames/CatalogService), [Caching](Library/Caching.md), [Artwork](Library/Artwork.md), [External Sources](Library/ExternalSources.md) |
| Install, update, downloads | [Install And Update](Flows/InstallAndUpdate.md), [Launcher Service](../EpicGames/LauncherService), [Artifact Delivery](../EpicGames/ArtifactDeliveryService), [Entitlement Service](../EpicGames/EntitlementService) |
| Launch | [Game Launch](Flows/GameLaunch.md), [Ownership Token](../EpicGames/EcommerceIntegrationService/OwnershipToken/Create.md) |
| EULA | [EULA Tracking](../EpicGames/EulaTrackingService) |
| Store, purchase | [Purchase](Flows/Purchase.md), [Order Processor](../EpicGames/OrderProcessorService), [Store Content](../EpicGames/StoreContentService), [Store web](../EpicGamesStore) |
| Fab | [Fab](../EpicGames/Web/Fab) |
| Partner titles | [Partner Integration](../EpicGames/PartnerIntegrationService), [Deep Links](DeepLinks.md#partner-hand-off-uris-outbound) |
| Cloud saves | [Cloud Saves](Flows/CloudSaves.md), [Data Storage](../EpicGames/DataStorageService) |
| Fortnite deployment info | [Fortnite App Service](../EpicGames/FortniteAppService) |
| External game metadata | [IGDB](../ThirdParty/IGDB) |
| Social, presence, chat, party | [Social Overview](Social/Overview.md), [Bridge](Social/Bridge.md), [Connect](Social/Connect.md), [GraphQL](Social/GraphQL.md), [Friends](../EpicGames/FriendsService), [Presence](../EpicGames/PresenceService), [Party](../EpicGames/PartyService), [Interactions](../EpicGames/InteractionsService) |
| Voice | [Voice Chat](Flows/VoiceChat.md), [RTC Service](../EpicGames/RTCService) |
| Self update, what's new, v1 migration | [Self Update](SelfUpdate.md) |
| Telemetry, crash reports | [Data Router](../EpicGames/DataRouterService), [Sentry](../ThirdParty/Sentry) |

## Module map

Top-level `eglv2_lib` modules seen in strings: `api` (`artifact_dependency`, `assets`, `catalog`, `client`, `collections`, `eula`, `external_auths`, `fab`, `fn_deployment`, `igdb`, `library`, `partner_integration`, `purchase`, `store_content`, `store_tags`, `e3s`, `ownership_token`), `auth`, `cache`, `child_launch`, `cloud_saves`, `command_line`, `commands`, `compat` (Proton), `config`, `deep_link`, `device_id`, `device_profile`, `download`, `engines`, `entitlement`, `eos`, `epic_connect`, `eula_gate`, `external_library` (`steam`, `xbox`), `fab`, `fab_import`, `feedback`, `hero_cache`, `image_cache`, `import_scan`, `install_api`, `install_state`, `installations_migration`, `launchdarkly`, `ld_overrides`, `mock`, `ovt`, `partner`, `pending_uninstall`, `platform_availability`, `playtime`, `presence_mode_flag`, `product_state`, `recently_played`, `refresh`, `running_apps`, `self_update_boot_gate`, `settings`, `single_instance`, `social`, `stable_target`, `taskbar`, `telemetry`, `thread_priority`, `tray`, `update_check_config`, `uri_activation`, `v1_migration`, `webview`, `window_snap`.
