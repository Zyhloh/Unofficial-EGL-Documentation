## Artifact Delivery Service - Builds: Manifest

The build manifest (file list, chunk list, install tags, launch info) for one build. Downloaded after [Get Asset (v2)](../../LauncherService/Assets/GetAssetV2.md) for install, update, verify, repair, DLC uninstall (when no local copy exists in `.egstore`) and size lookups. Parsed manifests are cached in memory with an idle TTL ("Parsed manifest cache hit/miss").

URL: `manifests[].uri` from Get Asset (v2), with that entry's `queryParams` appended \
Method: GET \
Auth Required: No (the query token is the authorization)

## Mirrors

Each `manifests[]` entry is the same file on a different CDN, each with its own signed query parameter:

| Host | Query parameter |
| ---- | --------------- |
| `egdownload.fastly-edge.com` | `f_token` |
| `epicgames-download1.akamaized.net` | `ak_token` |
| `egs-cloudfront-chunks.epicgamescdn.com` | `cf_token` |

The order of the entries differs between responses. A token is `<unix expiry>_<hex signature>` and expires about 5 minutes after the Get Asset call, so fetch the asset right before downloading. Expired tokens fail per CDN: CloudFront `403` with body `expired token`, Akamai `403` HTML error page, Fastly `410 Gone`.

The client tries the mirrors in order and rejects a copy that fails to download, fails to parse, or whose SHA-1 does not equal the element `hash` ("Every manifest mirror was rejected on the SHA-1").

## Example Request

```http
GET /Builds/Fortnite/CloudDir/VPUT6zt1kxXQ4D5n70-gFCFrnLTzQQ.manifest?f_token=1792033224_e219c1ebbc0528f463daeb1cfe92883380dfcd32 HTTP/1.1
Host: egdownload.fastly-edge.com
```

---

_Format_

All integers are little endian. Strings (`FString`) are an `int32` length followed by the characters: a positive length is that many bytes of UTF-8 / ASCII including the trailing NUL, a negative length is `-length` UTF-16LE characters including the trailing NUL, `0` is an empty string. Arrays (`TArray`) are a `uint32` count followed by the elements.

### Header (41 bytes)

| Offset | Type | Field |
| ------ | ---- | ----- |
| 0 | uint32 | Magic `0x44BEC00C` |
| 4 | uint32 | Header size (`41`) |
| 8 | uint32 | Body size, uncompressed |
| 12 | uint32 | Body size, as stored |
| 16 | byte[20] | SHA-1 of the uncompressed body |
| 36 | uint8 | Stored as: bit 0 = zlib compressed, bit 1 = encrypted |
| 37 | uint32 | Manifest version (feature level) |

The body follows the header. Inflate it with zlib when bit 0 is set and check its SHA-1. Encrypted manifests are rejected by the launcher ("Manifest is encrypted; encrypted builds are not supported").

Seen live: version `17` on most games, `13` on older builds (Football Manager 2020), `21` on Fortnite, Unreal Engine 5.x, Discord, Crosshair V2 and other current builds.

### Body

The body has four sections in this order. Each starts with a `uint32` section size (including itself) and a `uint8` data version; a reader should seek to `start + size` after reading the fields it knows, so newer versions stay readable.

**1. Meta**

| Type | Field | Since data version |
| ---- | ----- | ------------------ |
| uint32 | Section size | |
| uint8 | Data version | |
| uint32 | Feature level | 0 |
| uint8 | Is file data (`1` = old non-chunked build) | 0 |
| uint32 | App id | 0 |
| FString | App name | 0 |
| FString | Build version | 0 |
| FString | Launch executable (relative path) | 0 |
| FString | Launch command (extra arguments) | 0 |
| TArray&lt;FString&gt; | Prerequisite ids | 0 |
| FString | Prerequisite name | 0 |
| FString | Prerequisite path (relative) | 0 |
| FString | Prerequisite arguments | 0 |
| FString | Build id | 1 |
| FString | Uninstall action path | 2 |
| FString | Uninstall action arguments | 2 |

The manifest app name is not always the catalog app name (`AnchovyStaging` for `Anchovy`, `FortniteReleaseBuilds_Studio` for `Fortnite_Studio`, a GUID for many newer titles).

**2. Chunk data list**

`uint32` size, `uint8` version, `uint32` count `N`, then six arrays of `N` entries each (struct of arrays):

| Array | Element |
| ----- | ------- |
| GUIDs | 4 x uint32 (printed as 32 upper-case hex digits, each uint32 as 8 digits) |
| Rolling hashes | uint64 |
| SHA-1 hashes | byte[20], SHA-1 of the uncompressed chunk data |
| Data groups | uint8 |
| Window sizes | uint32, uncompressed size (always `1048576` seen) |
| File sizes | int64, size of the `.chunk` file to download |

**3. File list**

`uint32` size, `uint8` version, `uint32` count `N`, then:

| Array | Element | Since data version |
| ----- | ------- | ------------------ |
| File names | FString (relative path, `/` separators) | 0 |
| Symlink targets | FString | 0 |
| File hashes | byte[20], SHA-1 of the whole file | 0 |
| Flags | uint8: `1` read only, `2` compressed, `4` unix executable | 0 |
| Install tags | TArray&lt;FString&gt; | 0 |
| Chunk parts | `uint32` count, then per part: `uint32` part struct size (`28`), GUID (16 bytes), `uint32` offset in chunk, `uint32` size | 0 |
| MD5 | per file `uint32` has-MD5, then 16 bytes when non-zero | 1 |
| MIME types | FString | 1 |
| SHA-256 | byte[32] per file | 2 |

A file's content is its chunk parts concatenated in order: `chunk[offset : offset + size]` for each part. The file size is the sum of its part sizes.

**4. Custom fields**

`uint32` size, `uint8` version, `uint32` count `N`, `N` FString keys, `N` FString values. Empty on every build checked.

### Install tags

Files without install tags are always installed. Files with tags are installed when at least one of their tags is selected. The selectable tag groups come from [Selective Download Metadata](SdMeta.md) when the build has one (Fortnite), otherwise straight from the tags (Unreal Engine: `editor_symbols`, `engine_source`, `metahuman_content`, `platform_Android`, `platform_IOS`, `platform_Linux`, `platform_TVOS`, `platform_VOS`, `platform_WinARM64`, `templates`).

### JSON form

The launcher also accepts JSON manifests ("Detected JSON manifest format"). None of the builds checked was served as JSON; the field list is from the client strings and the legacy format: `ManifestFileVersion`, `AppNameString`, `BuildVersionString`, `LaunchExeString`, `LaunchCommand`, `PrereqIds`, `PrereqName`, `PrereqPath`, `PrereqArgs`, `FileManifestList[]` (`Filename`, `FileHash`, `FileChunkParts[]` with `Guid` / `Offset` / `Size`, `InstallTags`), `ChunkHashList`, `ChunkShaList`, `DataGroupList`, `ChunkFilesizeList`, `CustomFields`. Numbers in the JSON form are "blobs": each byte of the little-endian value written as 3 decimal digits (`"017000000"` = 17).

_Example (decoded meta, Rocket League)_

```json
{
  "featureLevel": 21,
  "appName": "SugarStaging",
  "buildVersion": "++Prime+Update60-CL-529371",
  "launchExe": "Binaries/Win64/Launcher.exe",
  "launchCommand": "",
  "prereqIds": ["EAC_Service"],
  "prereqPath": "Binaries/Win64/EasyAntiCheat/EasyAntiCheat_EOS_Setup.exe",
  "prereqArgs": "install e6bcca5b37d0457ca881aec508205542",
  "buildId": "efHIGRjCoUi2B4e0YPrMYQ",
  "uninstallActionPath": "Binaries/Win64/EasyAntiCheat/EasyAntiCheat_EOS_Setup.exe",
  "uninstallActionArgs": "uninstall e6bcca5b37d0457ca881aec508205542"
}
```

The installed copy is stored in the install folder as `.egstore/<installationId>.manifest` and is used as the old side of update diffs. Chunk URLs are built from the manifest's mirror; see [Chunk](Chunk.md).
