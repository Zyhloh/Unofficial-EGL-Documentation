# IPC - Events

Events the Rust backend emits to the frontend. Typed through tauri-specta (`events` in `bindings-*.js`, `listen` / `once` / `emit` proxies). Payload docs come from the doc comments embedded in the exe (`src\types.rs`, `src\events.rs`).

## Typed events

| Event | When |
| --- | --- |
| `access-denied-event` | Backend refused an action for the current account |
| `auth-state-changed-event` | Auth state changed, see [Auth IPC](../Auth/IPC.md) |
| `cabined-launch-blocked-event` | Launch blocked for a cabined account |
| `cabined-mode-changed-event` | Cabined mode toggled |
| `catalog-item-cached-event` | One catalog item refreshed |
| `catalog-updated-event` | Catalog refreshed |
| `checkout-overlay-visibility-event` | `checkout-overlay` shown / hidden |
| `cloud-save-decision-required-event` | Cloud save conflict needs a user choice (answer with `cloud_save_resolve`) |
| `cloud-save-sync-state-event` | Cloud save sync progress |
| `cloud-save-upload-state-event` | Cloud save upload progress |
| `custom-engines-updated-event` | Custom engine list changed |
| `deep-link-install-event` | `com.epicgames.launcher://apps/...?action=install` |
| `deep-link-navigate-event` | Deep link resolved to a frontend route (`{ route, replace }`) |
| `deep-link-uninstall-event` | Uninstall link, opens the confirm dialog |
| `download-progress-event` | Download progress |
| `download-queue-state-event` | Queue changed |
| `engines-updated-event` | Engine list changed |
| `eula-prompt-event` | EULA gate needs an answer: `{ promptId, appId, key, version, title, body, locale, action }` (`action` `install` / `launch`) |
| `eula-prompt-closed-event` | Prompt resolved elsewhere |
| `external-library-updated-event` | Steam / Xbox discovery changed |
| `flag-changed-event` | A LaunchDarkly flag changed |
| `frontend-debug-wanted-changed` | Verbose frontend logging toggled |
| `game-state-changed-event` | Running state of a game |
| `idle-state-changed-event` | User idle / active (social presence) |
| `image-cached-event` | Cover cached: `{ md5, localUrl, url }` (`localUrl` is `http://img.localhost/<md5>`) |
| `install-disk-sizes-updated-event` | Disk sizes re-measured |
| `install-scan-completed-event` | Install scan finished |
| `install-scan-progress-event` | Install scan progress |
| `ld-status-changed-event` | LaunchDarkly client status |
| `library-updated-event` | Library refreshed |
| `open-native-library-event` | Store asked to open the native library |
| `partner-account-link-completed-event` | Partner account link returned (loopback `/launcher/account-linked`) |
| `partner-install-dispatched-event` | Partner hand-off sent, frontend starts the install wait |
| `partner-title-state-changed-event` | Partner title state |
| `partner-titles-stale-event` | Partner titles need a reload |
| `platform-availability-event` | Availability probe results |
| `playtime-published-event` | Playtime sent to the library service |
| `prereq-failed-event` | Prerequisite install failed |
| `product-state-changed-event` | Tile state changed |
| `proton-install-progress-event` | Linux Proton download |
| `proton-runtime-required-event` | Linux: game needs Proton |
| `release-channel-changed-event` | Release channel changed |
| `selective-download-info-updated-event` | Background revalidation of selective download info finished |
| `stable-target-changed-event` | `stable-target.json` answer changed |
| `staff-eligibility-changed-event` | Staff check changed (EG Staff pane) |
| `store-auth-injected-event` | EG1 token injected into the store webview |
| `tools-updated-event` | UE tool list changed |
| `ue-gates-updated-event` | Engine / tool EULA gates changed |
| `ue-projects-measured-event` | Project sizes measured |
| `verify-repair-started-event` | Verify found damage and started repair |
| `window-snap-interaction` | Window snap layout interaction |

## Untyped events

| Event | Direction | Notes |
| --- | --- | --- |
| `perf-snapshot-event` | backend -> frontend | Perf overlay samples |
| `tray://open`, `tray://quit`, `tray://sign-out`, `tray://navigate`, `tray://launch` | tray -> frontend | Tray menu actions |
| `menu://settings`, `menu://navigate` | menu -> frontend | App menu (macOS) |
| `taskbar://restore` | backend -> frontend | Restore from taskbar |
| `window://hidden` | backend -> frontend | Main window hidden to tray |
| `webview-focus://returned` | backend -> frontend | Keyboard focus came back from a content webview |
| `social://resize-panel`, `social://open-friend-linking`, `social://notify`, `social://badge-count-updated`, `social://conversation-read` | social -> shell | Social panel |
| `social://game-invite-received`, `social://game-invite-accepted`, `social://game-invite-dismissed`, `social://game-invite-store` | backend -> shell | Game invite toasts |
| `toast:ready`, `toast:render`, `toast:click`, `toast:action`, `toast:secondary-action`, `toast:dismiss`, `toast:hover` | shell <-> `toast-window` | Toast window protocol |
| `store://change` | plugin | tauri-plugin-store change notification |

## Tauri plugins used by the frontend

`app`, `dialog` (`open`), `event`, `image`, `os` (`hostname`, `locale`), `path`, `process` (`exit`), `resources`, `sentry` (`breadcrumb`, `envelope`), `store` (key / value files), `webview` (child webviews: create, reparent, bounds, zoom, focus, `clear_all_browsing_data`), `window`. Backend-only plugins seen in the exe: `single-instance`, `deep-link`, `updater` (pubkey minisign `C39BFB6A058EE12B`, `installMode: quiet`), tray icon.

## Bridge objects in content webviews

Scripts embedded in the exe and injected as Tauri initialization scripts. Remote origins get access through capabilities (`social-bridge-remote`, a store bridge capability for `store-webview`).

| Webview | Global | Methods / members |
| --- | --- | --- |
| `store-webview` | `window.ue.launcher` | `getaccesstoken`, `getversion`, `getapiversion`, `apiversions { purchase, signin, layout }`, `featurelevel`, `cabinedmode`, `offlinemode`, `getinstalledapps`, `getexpandedinstalledapps`, `getrecentlyplayed`, `getexpandedrecentlyplayed`, `getqueuedapps`, `getapp`, `openwindow`, `isssoenabled`, `requestsignin`, `onwebloaded`, `trackperformance`, `isbridgestatisticsenabled`, `reportbridgestatistics`, `setversionstrings`, `refetchuserbuilds`, `register*callback` (active / failed / history / scheduled queue, app manage info, install item action, overwrite files modal, response) |
| `store-webview` | `window.ue.common` | `getsignedinuser`, `launchexternalurl` |
| `store-webview` | `window.ue.webmarketplace` / `WebMarketplace` | `requestpurchase`, `requestpurchasecart`, `requestpurchasev2` (all casings) -> `bridge_request_purchase*` |
| `store-webview` | `window.ue.history` | `pushurlhistory`, `replaceurlhistory` -> `store_nav` |
| `store-webview` | `window.ue.social` | `showsocial`, `hidesocial`, `issocialvisible`, `getonlinestatus`, `getbadgecounter` |
| `checkout-overlay` | `window.ue.purchaseflow` / `PurchaseFlow` | `requestclose` / `RequestClose` (`WasSuccessful`, `UserCanceled`, `PurchaseFailed`, `LoadFailure`) -> `bridge_checkout_complete` |
| `fab-webview` | `window.ue.fab` | `getapiversion`, `getsettings`, `savesettings`, `getlistings`, `getlocallistings`, `getprojectlistings`, `searchlocallistings`, `removelocallisting`, `verifylocallistings`, `showlistingondisk`, `download`, `downloadondemand`, `downloadbulk`, `downloadunreallistings`, `downloadplugin`, `installplugin`, `removeplugin`, `openpluginlocation`, `openpluginsettings`, `exportasset`, `exportlisting`, `exportlistingbulk`, `exportquixellisting`, `exportmetahumanlisting`, `addtoproject`, `focusincontentbrowser`, `dragstart`, `choosevaultcachelocation`, `getfolder`, `copytoclipboard`, `openurlinbrowser`, `showalert`, `showmodal`, `showlogs`, `logevent`, `geturlhistory`, `pushfaburlhistory`, `getauthtoken`, `getrefreshtoken`, `login`, `logout`, `isenterprisemodeenabled`, `registercallbacks` |
| `fab-webview` | `window.ue.fab.nativeCallbacks` | Pushed by native: `settingsupdated`, `locallistingsupdated`, `locallistingsremoved`, `setdownloadprogressforlisting`, `setdownloadprogressplugin`, `setinstallprogressplugin`, `ondraginfosuccess`, `ondraginfofailure`, `onLoginSuccessful`, `onLoginFailed`, `pluginopened` |
| `social` | `window.ue.social`, `window.ue.common`, `window.ue.launcher` | See [Social Bridge](../Social/Bridge.md) |
