# Add-ons (DLC and additional content)

How "Manage add-ons" works and how add-ons are installed. Everything below was checked live against Fortnite, Civilization VI, Cyberpunk 2077 and Lego Star Wars.

## Finding a game's add-ons

1. [Catalog Bulk Items](../../EpicGames/CatalogService/Catalog/BulkItems.md) for the base game with `includeDLCDetails=true` returns `dlcItemList[]` (`{ id }` per add-on).
2. Bulk items for those ids gives each add-on's catalog item: `title`, `categories`, `mainGameItem` (the base game), `customAttributes` and `releaseInfo[]`. The add-on's app name is `releaseInfo[].appId` for the platform.
3. [Get Asset (v2)](../../EpicGames/LauncherService/Assets/GetAssetV2.md) for `namespace / addonItemId / appId` returns the build when the account owns it, else `403`:

```json
{
  "errorCode": "errors.com.epicgames.launcher.not_entitled",
  "errorMessage": "missing entitlement.",
  "messageVars": [],
  "numericErrorCode": 30000,
  "originatingService": "launcher-service",
  "intent": "prod"
}
```

A wrong item / app pair (for example the add-on's app id used as the item id) returns `404 errors.com.epicgames.launcher.invalid_catalog_item` (30009) instead.

Owned add-ons also appear in [Library Items](../../EpicGames/LibraryService/Library/Items.md) as their own records (`appName` = the add-on app).

## Categories

| Category | Meaning | Example |
| -------- | ------- | ------- |
| `addons` | Regular add-on | Civilization VI Aztec DLC, Lego Star Wars Classic Obi-Wan |
| `addons/launchable` | Add-on with its own entry and launch button | Fortnite Battle Royale, Fortnite OG, Unreal Editor for Fortnite |
| `digitalextras` | Extra (tools, soundtracks) | Cyberpunk 2077 REDmod |
| `hidden` | Not shown; installed as a dependency of the base game | Fortnite Save the World Content, LEGO Fortnite Content |

The "Manage add-ons" dialog lists the add-ons the account owns that are not `hidden`. For Fortnite on an account that owns BR, OG and UEFN, those three are listed; Festival, Rocket Racing, Ballistic, Reload, LEGO Odyssey / Brick Life and Save the World return `not_entitled`.

## Installing

An add-on installs into its base game's folder: its manifest paths are relative to the base game's root (REDmod writes `mods/...` and `tools/redmod/...` into the Cyberpunk 2077 folder). The install record has `parentInstallationId` set to the base game's `installationId`, and its manifest is saved next to the base game's in `.egstore/<installationId>.manifest`.

Add-on builds seen:

| Add-on | Files | Install size | Content |
| ------ | ----- | ------------ | ------- |
| Fortnite Battle Royale | 1 | 26 B | `dlc/zero.ini` |
| Fortnite OG | 1 | 20 B | `zbbrtest.txt` |
| Civilization VI Aztec DLC | 1 | | A `.modinfo` file |
| LEGO Fortnite Content (`hidden`) | 7 | 9.45 GB | `GFP_JunoRoot` pak files |
| Save the World Content (`hidden`) | 101 | 5.0 GB | `GFP_SaveTheWorldRoot` pak files |
| Unreal Editor for Fortnite | 11805 | 24.1 GB | `FortniteGame/Binaries/Win64/UnrealEditorFortnite-Win64-Shipping.exe` and its content |
| Cyberpunk 2077 REDmod | 4781 | 97 MB | Mod tools |

Many add-ons are entitlement markers: a tiny file whose presence the game checks. The large Fortnite content add-ons are exact subsets of the Fortnite manifest: every file in the LEGO / Save the World Content manifests is also in the base game's manifest with the same hash, under one install tag. When removing files on uninstall or when changing components, a file that another installation in the same folder also lists must be kept.

## Dependencies

Some builds have an [Artifact Dependency Config](../../EpicGames/LauncherService/ArtifactDependencies/GetConfig.md) (Get Asset v2 `metadata.hasDependencyConfig: true`). Fortnite's maps aliases to add-on apps and lists what each depends on:

```json
{
  "revision": 1,
  "aliases": {
    "Fortnite": "Fortnite",
    "FortniteJunoContent": "94bc5ec13f8f438c97fdbef3e9019e27",
    "FortniteStWContent": "aa31f9e94e844b299ca757d1d0b97a09"
  },
  "entries": {
    "Fortnite": { "namespace": "fn", "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5", "dependencies": [] },
    "94bc5ec13f8f438c97fdbef3e9019e27": { "namespace": "fn", "catalogItemId": "b619cf61a4144d67bd753dc990637e7c", "dependencies": ["Fortnite"] },
    "aa31f9e94e844b299ca757d1d0b97a09": { "namespace": "fn", "catalogItemId": "0b41f0192f7f4f2691684581aedc0778", "dependencies": ["Fortnite"] }
  }
}
```

The config is stored on the base game's install record (`dependencyConfig`). Hidden content add-ons can have their own [`.sdmeta`](../../EpicGames/ArtifactDeliveryService/Builds/SdMeta.md): Save the World Content has one required component, "Fortnite Save the World" (`Tags: ["GFP_SaveTheWorldRoot"]`).

## Add-on toggles

The dialog's switches are saved in `settings/game-settings.json` under `addons`, keyed by `<namespace>:<itemId>:<appName>` of the base game and then of the add-on:

```json
{
  "games": {},
  "addons": {
    "fn:4fe75bbc5a674f4f9b356b5c90567da5:Fortnite": {
      "fn:1e8bda5cfbb641b9a9aea8bd62285f73:Fortnite_Studio": false,
      "fn:4e7f14219eff40ffb21d0bcf1d68182a:6c914d2868bc4595a470c0edf7544c84": true,
      "fn:d75daf91c89b49ecb110b69a7bd68996:afdb5a85efcc45d8ae8e406e2121d81c": true
    }
  },
  "cloudSaves": {}
}
```

Applying the dialog calls the IPC command `set_app_configuration { parentAppId, configs: [{ appId, shouldBeInstalled }], allowUninstall }`. Seen live on Fortnite:

- **Turning an add-on off** saves `false` in the map and uninstalls it right away (not through the download queue): its manifest is loaded from `.egstore`, its files are deleted from the parent folder (`zbbrtest.txt` for Fortnite OG), and a tombstone `{"installationId":"5AF4B638FAEB9CF47D46642B635F017C","deleted":true}` is appended to `installations.jsonl`.
- **Turning add-ons on** saves `true` and queues one install per add-on, linked to the parent's installation id. A re-enabled add-on gets a new installation id (OG came back as `BFD921F1FA9DDF221DC144E43D5D0E17`). The queue runs one operation at a time, so OG waited behind the 20 GB UEFN download.

## Unreal Editor for Fortnite

UEFN (`Fortnite_Studio`, categories `addons/launchable`, `software`) is a Fortnite add-on with the same `buildVersion` as Fortnite, Get Asset v2 `metadata.installationPoolId: "FortniteInstallationPool"`, and custom attributes `AdditionalCommandLine: -epicapp=Fortnite`, `IgnoreMainGameGateKeeper: true`, `DlcProcessNames: UnrealEditorFortnite-Win64-Shipping.exe,CrashReportClientEditor.exe,urc.exe`. Its launch executable is `FortniteGame/Binaries/Win64/UnrealEditorFortnite-Win64-Shipping.exe` inside the Fortnite folder.
