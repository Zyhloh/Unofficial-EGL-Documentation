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

Example (placeholders; Fortnite-only `-named_pipe` / `-src` / `-pl` left out):

```
FortniteLauncher.exe -eglv2 -eglv2apipath="<path>" -AUTH_LOGIN=unused -AUTH_PASSWORD=94b1569506b04f9f8557af611e8c5e47 -AUTH_TYPE=exchangecode -epicapp=Fortnite -epicenv=Prod -EpicPortal -epicusername=Player -epicuserid=94b1569506b04f9f8557af611e8c5e47 -epiclocale=en -epicsandboxid=fn
```

## Launcher-reserved arguments

Before merging, user / catalog args whose name matches a launcher-owned argument are dropped (`Launch.LauncherOwnedArgDiscarded`, `sub_14055AD90`): `EpicPortal`, `epiclocale`, `epicsandboxid` always; `AUTH_LOGIN`, `AUTH_PASSWORD`, `AUTH_TYPE` when an exchange code is passed; `epicusername`, `epicuserid`, `named_pipe`, `epicovt`, `epicdeploymentid` when the launcher sets them. Deep-link forwarded args additionally refuse `auth_eglv2`, `epicapp`, `epicenv` and the names above (`DeepLink.ArgNotAllowed`) and must match the catalog's `AllowUriCmdArgsSanitized` regex.

## Cabined accounts

A cabined account must acknowledge the restriction notice first; see [Cabined Mode](../Auth/CabinedMode.md). The refused launch is replayed after `cabined_gate_acknowledge`.

## Partner titles

EA app / Ubisoft Connect titles are handed off instead of spawned. The launcher mints an exchange code the same way and passes `AUTH_PASSWORD`, `AUTH_TYPE=exchangecode`, `epicusername`, `epicuserid`, `epiclocale` to the partner client through its `://launchgame/` URI (EA: `exchangecode`, `source`, `epicuid` keys). Refused when the account is not linked (`REQ-PARTNER-130`, `REQ-PARTNER-133`). Partner details belong to the partner docs.
