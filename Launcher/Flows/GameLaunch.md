# Game Launch (auth part)

Games never get the launcher's token. `launch_game` mints a one-time exchange code and passes it on the command line, like the old launcher. Code: `sub_140B386E0` (launch), `sub_140F54030` (argument builder), `eglv2_lib::auth::exchange_code_cache` (prefetch).

## Exchange code

1. Frontend calls `prefetch_exchange_code` while the user is about to play (install dialog / play button hooks, throttled to once per 500 ms in JS). The launcher mints a code ahead of time and caches it (`Auth.ExchangeCode.PrefetchFailed` on error).
2. `launch_game` takes the cached code or mints one: [`GET /account/api/oauth/exchange`](../../EpicGames/AccountService/OAuth/Exchange.md) with the EG1 bearer.
3. Failure does not block the launch: `Failed to get exchange code, launching without auth:`; the `-AUTH_*` arguments are then left out.

Cache lifetime and whether a `consumingClientId` is sent for games are not resolved.

## Arguments

Built in this order:

| # | Argument | Condition |
|---|---|---|
| 1 | `-eglv2`, `-eglv2apipath="<install API path>"` | Namespace is not an Unreal Engine one (`ue`, `poodle`, `ecc92c9d225843f5827847052fb9f5f3`); the path only when the local install API is ready (`Install API readiness sender dropped; launching without an install API path`) |
| 2 | `-AUTH_LOGIN=unused` | Exchange code present |
| 3 | `-AUTH_PASSWORD=<exchange code>` | Exchange code present (logged as `<redacted>`) |
| 4 | `-AUTH_TYPE=exchangecode` | Exchange code present |
| 5 | Manifest `LaunchCommand`, catalog additional command line, per-game user args | Sanitised, see below |
| 6 | `-epicapp=<appName>` | Unless step 5 already has `epicapp` |
| 7 | `-epicenv=<env>` | Unless step 5 already has `epicenv`; value `Prod` / `GameDev`, replaced by the `override_epicenv` command-line option when set |
| 8 | `-epicovt=<path>` | Ownership verification token file written (`src\ovt`) |
| 9 | `-epicdeploymentid=<id>` | Deployment id from the artifact sidecar (`Passing the artifact sidecar's deployment id`) |
| 10 | `-EpicPortal` | Always |
| 11 | `-epicusername=<displayName>` | Signed in |
| 12 | `-epicuserid=<accountId>` | Signed in |
| 13 | `-epiclocale=<locale>` | Always |
| 14 | `-named_pipe=<accountId>\<value>` | Catalog namespace is `fn` (Fortnite) and a user id is known |
| 15 | `-src=12` `-pl=01` | Namespace `fn`, when a helper check on the argument list returns false (meaning not resolved) |
| 16 | remaining manifest / user args | |
| 17 | `-epicsandboxid=<namespace>` | Always |

Example (Crosshair V2, captured from the launcher log, `Launch.GameSpawning`, 12 arguments):

```
"C:\Users\<user>\Epic Games\CrosshairV2QGIkt\Crosshair.exe" -eglv2 -eglv2apipath="C:\Users\<user>\AppData\Local\com.epicgames.eglv2\api.json" -AUTH_LOGIN=unused -AUTH_PASSWORD=<exchange code> -AUTH_TYPE=exchangecode -epicapp=8d3fd7a1c6034e799f04a2c8cce520a3 -epicenv=Prod -EpicPortal -epicusername=<displayName> -epicuserid=<accountId> -epiclocale=en -epicsandboxid=4de5e06a60314c12ada34d918e65cfda
```

`-eglv2apipath` points at the [Install API](../InstallApi.md) record. Before spawning, the launcher logs the ownership token gate (`Launch.OwnershipTokenSkipped reason=not_required`), the deployment id (`No artifact sidecar deployment id to pass`), the running-state process rules and a cloud save pull; a launch takes about 8 ms once the exchange code is prefetched.

## Fortnite

Fortnite's `launchExecutable` is `FortniteGame/Binaries/Win64/FortniteBootstrapper.exe` with the manifest launch command `-obfuscationid=<id>`. The bootstrapper starts `FortniteLauncher.exe` with the same arguments, which fetches the anti-cheat deployment (`deployment_id=62a9473a2dca46b29ccf17577fcf42d7 sandbox_id=fn`), writes `EasyAntiCheat/Settings.json`, and starts `FortniteClient-Win64-Shipping_EAC_EOS.exe` with the launcher's arguments plus `-fromfl=eaceos -caldera=<token> -startup=<guid>`. The game then logs in with the exchange code (`FOnlineIdentityMcp::Login Type=exchangecode`, `EOS_Auth_Login succeeded`, `EOS_Connect_Login succeeded`).

A launch built by the [Download Client](../Library/DownloadClient.md) without `-eglv2`, `-named_pipe`, `-src` / `-pl` (auth args, `-obfuscationid`, Epic args, from a copy installed by that client) logged in and played a full match. Within a minute of starting, Fortnite queued a `Repair` of its Battle Royale add-on through the Install API.

## Launcher-reserved arguments

Before merging, user / catalog args whose name matches a launcher-owned argument are dropped (`Launch.LauncherOwnedArgDiscarded`, `sub_14055AD90`): `EpicPortal`, `epiclocale`, `epicsandboxid` always; `AUTH_LOGIN`, `AUTH_PASSWORD`, `AUTH_TYPE` when an exchange code is passed; `epicusername`, `epicuserid`, `named_pipe`, `epicovt`, `epicdeploymentid` when the launcher sets them. Deep-link forwarded args additionally refuse `auth_eglv2`, `epicapp`, `epicenv` and the names above (`DeepLink.ArgNotAllowed`) and must match the catalog's `AllowUriCmdArgsSanitized` regex.

## Cabined accounts

A cabined account must acknowledge the restriction notice first; see [Cabined Mode](../Auth/CabinedMode.md). The refused launch is replayed after `cabined_gate_acknowledge`.

## Ownership token

Titles whose catalog custom attribute `OwnershipToken` is `"true"` (Hogwarts Legacy, Just Cause 4, Football Manager 2020) get a token from [Ownership Token](../../EpicGames/EcommerceIntegrationService/OwnershipToken/Create.md) before the launch. It is written to `<installDir>\.egstore\<accountId>\<namespace><catalogItemId>.ovt` (the three parts are checked to be file-name safe) and passed as `-epicovt=<path>`. Token files are deleted on uninstall.

## Deployment id

`-epicdeploymentid` comes from the artifact sidecar ([Bulk Sidecars](../../EpicGames/LauncherService/Assets/BulkSidecars.md), `config.deploymentId`). Titles without a sidecar launch without it ("launching without -epicdeploymentid").

## Extra launch options

Catalog custom attributes `extraLaunchOption_NNN_Name` / `extraLaunchOption_NNN_Args` (e.g. ARK: `Launch ARK (Extremely Low Memory)`, Rocket League `-noeac`) are offered as alternative launch modes (`get_extra_launch_options`); the chosen option's args are appended. `defaultLaunchOption_Args` is used when none is chosen. Argument sources in precedence order: manifest `LaunchCommand`, catalog `AdditionalCommandLine`, per-game user launch args, catalog extra launch option args; a later duplicate of the same argument wins within a source, a higher-precedence source wins across sources.

## Partner titles

EA app and Ubisoft Connect titles are handed off by URI instead of spawned, with a fresh exchange code per hand-off. See [Third-party Titles](../Library/ThirdPartyTitles.md) for the URIs and checks.
