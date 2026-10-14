# Deep Links

Scheme: `com.epicgames.launcher://` (Tauri `deep-link` plugin, `desktop.schemes`). The same scheme the UE launcher used; on start EGL v2 takes the registration back if another launcher owns it (`Took the com.epicgames.launcher:// registration back from ...`, `EGL_URL_PROTOCOL_RECLAIM`), unless it is not the installed copy (debug builds leave it alone).

## Delivery

1. A second launcher process receives the URI and hands it to the running instance through the single-instance plugin (`single_instance::windows_impl`), or the first instance reads it from its own command line.
2. `deep_link::transport` sanitizes it (`too_long`, `bad_scheme`, `embedded_scheme`, `malformed` are rejected) and buffers it until the session is ready (`Draining buffered deep-link activation on session-ready`).
3. `deep_link::parser` turns it into an intent; `deep_link::dispatch` acts on it. Navigation intents become `deep-link-navigate-event` (or wait in an inbox until the UI asks with `deeplink_take_pending`); uninstall intents become `deep-link-uninstall-event` (`deeplink_take_pending_uninstall`).

## Routes

The first path element (host) is matched case-insensitively.

| URI | Result |
| --- | --- |
| `com.epicgames.launcher://apps/<appRef>` | Launch (default action). `<appRef>` is the URL-encoded app id; the launcher itself builds `apps/<namespace>:<catalogItemId>:<appName>` (`com.epicgames.launcher://apps/` + `:` separators) and also accepts a bare app name (`DeepLink.AppNameUnresolved` when it cannot be resolved) |
| `...apps/<appRef>?action=launch` | Launch. Not installed -> deferred install (`DeepLink.LaunchDeferredInstall`); update pending -> deferred update; already running -> focus it; partner-managed -> partner hand-off |
| `...apps/<appRef>?action=install` (also `installer`, `update`) | `deep-link-install-event`; resumes a paused download, no-op if already installed |
| `...apps/<appRef>?action=verify` | Verify files |
| `...apps/<appRef>?action=uninstall` | Opens the uninstall confirmation (`DeepLink.UninstallDialogOpened`) |
| `...apps/<appRef>?action=updatecheck` | Update check for the app (`DeepLink.UpdateCheckRequested`) |
| `com.epicgames.launcher://store` / `store/<path>` | Store webview at `/store/<path>` |
| `com.epicgames.launcher://library` | `/library` |
| `com.epicgames.launcher://library?...` | Library with `collectionId`, `/library?acquired=1`, `/library?open=<catalogItemId>` variants |
| `com.epicgames.launcher://ue` / `unreal-engine[/...]` | `/engines` or `/engines/<sub>` (e.g. `engines/unreal-engine`) |
| `com.epicgames.launcher://fab` | `/fab` |
| `com.epicgames.launcher://coderedemption` | Code redemption |
| `com.epicgames.launcher://settings` | Settings |
| `com.epicgames.launcher://social/friends/add` | Social panel: add friend |
| `com.epicgames.launcher://social/notification/<rest>` | Social panel: notification target |
| `com.epicgames.launcher://social/<rest>` | Social panel |
| `com.epicgames.launcher://invite?payload=<payload>` | Game invite (`social::game_invite::deeplink`, inbox with TTL; only `/invite` is handled on that path) |
| `com.epicgames.launcher://epics/<rest>` | Parsed and ignored (`DeepLink.EpicsInert`) |
| anything else | `/library` |

Launch query keys recognized by the parser (names from the binary, semantics inferred): `action`, `silent` (launch without surfacing the launcher, `DeepLink.LaunchSilentWhileRunning`), `arg` (extra launch argument), `env`, `tag`, `install`, `running`, `app`, `timeout`.

Game invite weblinks resolve their target through `e3s_service` `/api/v1/coordinates` (`game-invite: weblink dropped (coordinates resolve failed)`), gated by the `game-invites-weblink` flag.

## Partner hand-off URIs (outbound)

For titles managed by the EA app or Ubisoft Connect the launcher does not start the game itself; it opens the partner client (`eglv2_lib::partner::handoff`, `src\partner\handoff.rs`):

```
<scheme>://launchgame/<artifactId>?auth_password=<exchangeCode>&auth_type=exchangecode&epicusername=<displayName>&epicuserid=<accountId>&epiclocale=<locale>
```

| Provider | Scheme |
| --- | --- |
| `ea_app` | `link2ea` or `epic2ea` (flag `partner-ea-uri-scheme`: `auto`, `epic2ea`, `link2ea`) |
| `ubisoft_connect` | `uplay` |

Key order and the upper-case variants `AUTH_PASSWORD` / `AUTH_TYPE` (also in the binary) are not resolved. The hand-off is refused when the scheme does not belong to the provider (REQ-PARTNER-042), the exchange code is empty (REQ-PARTNER-046) or the artifact id fails validation (REQ-PARTNER-043). Missing partner clients are downloaded from the launcher content build (`EpicGamesLauncherContentWindowsLive-Krampus`, `EA/EAappInstaller.exe`, `UbisoftConnect/UbisoftConnectInstaller.exe`) by `begin_partner_client_acquisition`. Code redemption: [Partner Integration](../EpicGames/PartnerIntegrationService).

Account linking returns on a loopback listener at `/launcher/account-linked` and emits `partner-account-link-completed-event`.

## External pages

Opened in the system browser (`open_account_link`, `open_url`, shell menu):

| Key / caller | URL |
| --- | --- |
| `account_settings` | `https://www.epicgames.com/account/personal?lang=<lang>` |
| `epic_rewards` | `https://www.epicgames.com/account/rewards?lang=<lang>` |
| `account_balance` | `https://www.epicgames.com/account/payments?lang=<lang>` |
| `coupons` | `https://store.epicgames.com/inventory/coupons?lang=<lang>` |
| redeem | `https://www.epicgames.com/redeem?lang=<lang>&source=egs-launcher` |
| `terms_of_service` | `https://www.epicgames.com/site/<lang>/tos` |
| `privacy_policy` | `https://www.epicgames.com/site/<lang>/privacypolicy` |
| `store_refund_policy` | `https://www.epicgames.com/site/<lang>/store-refund-policy` |
| `publisher_index` | `https://store.epicgames.com/<lang>/publisher-index` |
| parental consent | `https://www.epicgames.com/account/parental-controls` (see [Cabined Mode](Auth/CabinedMode.md)) |

The key-to-URL pairing follows the order of the strings and the menu labels; the redeem entry's caller was not resolved.
