# Third-party Titles and Apps

Titles that are not a plain "download files, run exe" game. All examples were checked live with [Get Asset (v2)](../../EpicGames/LauncherService/Assets/GetAssetV2.md) and the build [Manifest](../../EpicGames/ArtifactDeliveryService/Builds/Manifest.md). The catalog custom attributes come from [Catalog Bulk Items](../../EpicGames/CatalogService/Catalog/BulkItems.md).

## Ubisoft Connect titles

Catalog attributes (Rayman Legends):

```json
{
  "ThirdPartyManagedProvider": "UbisoftConnect",
  "partnerLinkType": "ubisoft",
  "partnerLinkId": "f667bb94543e43eb87ca008f497df782",
  "GameID": "410",
  "RegistryPath": "SOFTWARE\\WOW6432Node\\Ubisoft\\Launcher\\Installs\\410",
  "RegistryKey": "InstallDir",
  "NeverUpdate": "true",
  "FolderName": "RaymanLegends"
}
```

The Epic build is the full game plus a bundled Ubisoft Connect installer. Manifest meta:

| Field | Value |
| ----- | ----- |
| `launchExe` | `UplayLaunch.exe` |
| `launchCommand` | `-UplayId=410` |
| `prereqIds` | `["uplay"]` |
| `prereqName` | `Uplay` |
| `prereqPath` | `Uplay/UplayInstaller.exe` |
| `prereqArgs` | `/S` |

Seen on Rayman Legends (5.4 GB download), Trackmania (3.0 GB), Watch Dogs (14.7 GB), Watch Dogs 2 (40.5 GB), Assassin's Creed Syndicate (47.9 GB) and Roller Champions (0.5 GB). `NeverUpdate: true` marks the Epic build as never updated (Ubisoft Connect patches the game). `GameID` is the Ubisoft game id. `RegistryPath` / `RegistryKey` (HKLM) is where Ubisoft Connect records the install folder.

The new launcher does not use this build: it never references `UplayLaunch.exe` or `NeverUpdate`, and hands install and launch to Ubisoft Connect (see [Partner hand-off](#partner-hand-off)). The build is what the old launcher installed; it still downloads and works (install it, run the `uplay` prerequisite, start `UplayLaunch.exe` with the launch command).

## EA app titles

Catalog attributes (Battlefield 6):

```json
{
  "ThirdPartyManagedApp": "the EA app",
  "RegistryPath": "SOFTWARE\\WOW6432Node\\EA Games\\Battlefield 6",
  "RegistryKey": "Install Dir",
  "AdditionalCommandline": "&platform=epic",
  "AllowUriCmdArgs": "true",
  "AllowedUriEnvVars": "params",
  "ProcessNames": "bf6.exe,EAAntiCheat.GameServiceLauncher.exe,EAAntiCheat.Installer.exe",
  "MainWindowProcessName": "bf6.exe",
  "FolderName": "Battlefield6"
}
```

There is no Epic build: Get Asset (v2) returns

```json
{
  "errorCode": "errors.com.epicgames.launcher.download_info_not_found",
  "errorMessage": "Could not find download info",
  "messageVars": [],
  "numericErrorCode": 30006,
  "originatingService": "launcher-service",
  "intent": "prod"
}
```

The game is installed and updated by the EA app. `RegistryPath` / `RegistryKey` tell the launcher where the EA app recorded the install.

## Partner hand-off

The launcher supports exactly two partners: the EA app (`ThirdPartyManagedApp: "the EA app"`, `Origin` is treated as an alias) and Ubisoft Connect (`ThirdPartyManagedProvider: "UbisoftConnect"`). Other values (Rockstar, ...) are not handled.

1. **Install state** of the title: HKLM `RegistryPath`, value `RegistryKey`. Without both the state is "undeterminable" and nothing is handed off. Ubisoft titles also need `GameID`.
2. **Partner client present**: its URI scheme is registered (`HKCR\<scheme>` with `URL Protocol` and a `shell\open\command` whose exe exists), plus `HKLM\SOFTWARE\WOW6432Node\Electronic Arts\EA Desktop` `InstallSuccessful` for EA and `HKLM\SOFTWARE\WOW6432Node\Ubisoft\Launcher` `InstallDir` (with `UbisoftConnect.exe` in it) for Ubisoft. A missing client is installed, elevated, from the launcher's own content build (`EA/EAappInstaller.exe` with `EAX_LAUNCH_CLIENT=0 IGNORE_INSTALLED=1`, `UbisoftConnect/UbisoftConnectInstaller.exe`).
3. **Account link**: [External Auths](../../EpicGames/AccountService/Account/ExternalAuths.md). When not linked, the partner's link page opens in the browser and the launcher waits for the return on a loopback port. If the read fails the hand-off is still allowed. For Ubisoft the title's Uplay activation code (partner integration `uplaycode`: `{gameId, uplayAccountId, redeemedOnUplay}`) must be redeemed first.
4. **Hand-off**: a fresh [exchange code](../../EpicGames/AccountService/OAuth/Exchange.md) is minted and the URI is opened, both for install (Get Asset v2's 404 is ignored) and for launch. After an install hand-off the launcher waits for the registry install state to appear.

EA (`epic2ea` or `link2ea`, chosen by the LaunchDarkly flag `partner-ea-uri-scheme`, default `auto`):

```
link2ea://launchgame/<appName>?AUTH_PASSWORD=<exchange code>&AUTH_TYPE=exchangecode&epicusername=<displayName>&epicuserid=<accountId>&epiclocale=<locale><AdditionalCommandline>
```

`AdditionalCommandline` is appended as is (Battlefield 6: `&platform=epic`) and may not redeclare the five parameters.

Ubisoft:

```
uplay://launch/<GameID>/<launch option>?exchangecode=<exchange code>&epicuid=<accountId>&source=epic
```

URI schemes the launcher opens at all: `steam://`, `epic2ea://`, `link2ea://`, `uplay://`, `shell:AppsFolder\`.

## Apps through AppProxy

Some software is shipped as a tiny build that wraps the vendor's own installer. Discord's build is 6 files:

```
AppProxy.exe
AppProxy.ico
AppProxy.ini
DiscordSetup.exe
msvcp140.dll
vcruntime140.dll
```

`launchExe` is `AppProxy.exe`. AppProxy reads `AppProxy.ini` next to it: if the app is already installed it launches it, otherwise it runs the setup first. The launcher only installs the build and runs `AppProxy.exe`. Discord's `AppProxy.ini` (comments removed):

```ini
[KnownInstallLocation]
Location=%LOCALAPPDATA%\Discord
FileToCheck=installer.db

[Setup]
Name=DiscordSetup.exe
Arguments=-s --silent

[Launch]
Command=%LOCALAPPDATA%\Discord\Update.exe
Arguments=--processStart Discord.exe --process-start-args --campaign-id=epic-games-store

[ForwardCommandLineOnLaunch]
Enabled=False

[ForwardCommandLineOnSetup]
Enabled=False

[Logging]
Enabled=False
```

| Section | Keys |
| ------- | ---- |
| `KnownInstallLocation` (repeatable) | `Location` (environment variables allowed), `FileToCheck`. If the file exists, the app counts as installed |
| `Setup` (repeatable) | `Name` (default `Setup.exe`, next to AppProxy.exe), `Arguments` |
| `Launch` (repeatable) | `URI`, `BundleId` (Mac), `Command`, `Arguments`, or a registry lookup with `HKey`, `Path`, `Value`, `IsURI` |
| `ForwardCommandLineOnLaunch`, `ForwardCommandLineOnSetup` | `Enabled` (default true): pass the launcher's arguments through |
| `Logging` | `Enabled`: write `AppProxy.log` next to AppProxy.exe |

The first section that finds, installs or launches the app wins.

Other software is a normal build (Crosshair V2: 626 files, `launchExe` `Crosshair.exe`).

## Prerequisites seen

| Title | `prereqIds` | `prereqPath` | `prereqArgs` |
| ----- | ----------- | ------------ | ------------ |
| Ubisoft titles | `uplay` | `Uplay/UplayInstaller.exe` | `/S` |
| Rocket League | `EAC_Service` | `Binaries/Win64/EasyAntiCheat/EasyAntiCheat_EOS_Setup.exe` | `install <productId>` |
| Unreal Engine 5.8 | `25BDAA9B0A339099E10CF9C26E8ABDCD67A9E583` | `Engine/Extras/Redist/en-us/vc_redist.x64.exe` | `/quiet /norestart` |
| Cyberpunk 2077 | `VCRedist1519` | `vc/vc_redist.x64.exe` | `/install /passive /norestart` |

The launcher runs the prerequisite after the files are in place: `ShellExecuteExW` with the `runas` verb (elevated, UAC prompt), hidden window, waiting for the exit code. The path must resolve inside the install folder. An abnormal exit is retried once; a failure raises `prereq-failed-event` but Play stays enabled. Whether it already ran is tracked on the install record (`prereqSha1Hash` vs `lastPrereqSucceededSha1Hash`), not by checking the system.

Rocket League also has an uninstall action (`uninstallActionPath` = the EAC setup, `uninstallActionArgs` = `uninstall <productId>`). The new launcher does not run uninstall actions.

## Ownership tokens

Titles with the custom attribute `OwnershipToken: "true"` (Just Cause 4, Football Manager 2020, Hogwarts Legacy) need an ownership token at launch; see [Game Launch](../Flows/GameLaunch.md).
