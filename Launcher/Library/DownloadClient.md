# Download Client

Standalone install / update / launch client in [`Examples/DownloadClient`](../../Examples/DownloadClient). Python + [httpx](https://www.python-httpx.org/), no launcher needed. It follows the [Install and Update flow](../Flows/InstallAndUpdate.md) and [Game Launch](../Flows/GameLaunch.md), and was tested live on games (Drawful 2, Crosshair V2), software (Discord through AppProxy), engine plugins (Quixel Bridge 5.7 -> 5.8 update), Fortnite (components, add-ons) and partner titles (EA / Ubisoft hand-off).

## What it does

- Lists the library with catalog data and a kind per title: `game`, `app`, `addon`, `engine`, `plugin`, `thirdparty:<provider>`, `external:<app>`
- Installs any owned build: fetches build info and manifest, picks components (`.sdmeta` or install tags), downloads chunks with EGL's CDN failover / retry / stall rules, assembles and SHA-1 checks every file
- Installs add-ons into the base game's folder and keeps files shared with other installations in that folder
- Updates in place: fetches the [delta manifest](../../EpicGames/ArtifactDeliveryService/Builds/Delta.md) when one exists, keeps unchanged files, rebuilds changed ones from local data, downloads the rest, deletes removed files after the swap. Fortnite 42.30 -> 42.40 downloaded 3.01 GB (same 3,408 chunks as the launcher) and the result was byte-identical to the launcher's update
- Checks for updates with batched app info, like the launcher's background check
- Verifies and repairs (only the chunks of bad files are downloaded)
- Uninstalls (add-ons first, shared files kept)
- Imports existing launcher installs from `installations.jsonl`
- Launches with the exact launcher arguments, ownership token (`.ovt`) and sidecar deployment id, or hands EA / Ubisoft titles to their client by URI
- Prints a title's art (catalog key images + store hero art)

## Files

| File | Contents |
| --- | --- |
| `config.json` | Settings (no environment variables) |
| `auth.py` | Authorization code / refresh token grant, token cache |
| `epic.py` | Library, catalog, assets, app info, sidecars, dependency config, exchange code, ownership token, store content |
| `manifest.py` | Manifest (binary + JSON) and chunk parser |
| `engine.py` | Download planner, CDN selector, chunk store, assembly, verify |
| `client.py` | Install records, install / update / repair / uninstall / launch, add-ons, art |
| `main.py` | Command line |

## Config

`installRoot`: Where games go (`<installRoot>\<FolderName>`) <br/>
`stateFile`: Install records of this client <br/>
`tokenFile`: Token cache, outside the repository by default <br/>
`platform`, `label`: Build platform and label (`Windows`, `Live`) <br/>
`workers`: Parallel chunk downloads (the launcher uses 24 to 64) <br/>
`retries`: Attempts per chunk, each over every CDN (launcher: 4) <br/>
`memoryLimitMB`: Chunk RAM budget before spilling to `.egstore\chunkcache` <br/>
`speedLimitBytesPerSecond`: 0 = unlimited <br/>
`updateCheck`: `size` (trust unchanged files by size) or `hash` (rehash them) when updating <br/>
`runPrereqs`: Run prerequisites (elevated) after install <br/>
`locale`: For `-epiclocale`, the EA hand-off and store content <br/>
`client`: OAuth client used for the token grant

## Usage

```
pip install -r requirements.txt
python main.py library
python main.py info "Crosshair V2"
python main.py install "Crosshair V2"
python main.py install Fortnite --components A17316661F902216B15E8DAB34ECCD71 --dry-run
python main.py install UE_5.8 --tags templates,engine_source
python main.py addons Fortnite
python main.py check
python main.py verify "Crosshair V2"
python main.py repair "Crosshair V2"
python main.py launch "Crosshair V2"
python main.py launch "Battlefield 6" --dry-run
python main.py import
python main.py art Fortnite
python main.py uninstall "Crosshair V2"
```

`install` on an installed title updates it (or does nothing when it is current). `--dry-run` prints the plan: files kept / written / removed, download size, data reused from disk.
