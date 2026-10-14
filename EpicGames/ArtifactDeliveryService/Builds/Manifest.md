## Artifact Delivery Service - Builds: Manifest

The build manifest (file list, chunk list, install tags) for one build. Downloaded after [Get Asset (v2)](../../LauncherService/Assets/GetAssetV2.md) for install, update, verify, repair, DLC uninstall (when no local copy exists in `.egstore`) and size lookups. Parsed manifests are cached in memory with an idle TTL ("Parsed manifest cache hit/miss").

URL: `manifests[].uri` from Get Asset (v2), with that entry's `queryParams` appended \
Method: GET \
Auth Required: No (signed URL when `useSignedUrl` is true)

Each `manifests[]` entry is a mirror. The client tries them in order and rejects a copy that fails to download, fails to parse, or whose SHA-1 does not equal the element `hash` ("Every manifest mirror was rejected on the SHA-1").

---

_Format_

Epic chunked build manifest (`.manifest`), parsed by the launcher's `eglv2-manifest` crate:

- Binary form: header magic, zlib-compressed body, sections `ManifestMeta` (`AppID`, `AppName`, `BuildVersion`, `LaunchExe`, `LaunchCommand`, `PrereqIds`, `PrereqName`, `PrereqPath`, `PrereqArgs`, `BuildId`), chunk data list (GUID, hash, SHA-1, group, file size), file manifest list (`Filename`, `FileHash`, `FileChunkParts` with `Guid`/`Offset`/`Size`, `InstallTags`, `bIsUnixExecutable`) and custom fields.
- JSON form is also accepted ("Detected JSON manifest format": `ManifestFileVersion`, `AppNameString`, `BuildVersionString`, `LaunchExeString`, `ChunkHashList`, `ChunkShaList`, `ChunkFilesizeList`, `DataGroupList`, `FileManifestList`, `CustomFields`, ...).
- Encrypted manifests are rejected ("Manifest is encrypted; encrypted builds are not supported").
- The manifest's feature level picks the chunk directory: `Chunks`, `ChunksV2`, `ChunksV3`, `ChunksV4`, `ChunksV5`, `ChunksV5/plain` ("Derived chunk subdirectory from feature level"). See [Chunk](Chunk.md).

The installed copy is stored in the install's `.egstore` folder as `<id>.manifest` and is used as the old side of update diffs.
