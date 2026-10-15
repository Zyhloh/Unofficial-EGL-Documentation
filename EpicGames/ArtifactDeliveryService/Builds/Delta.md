## Artifact Delivery Service - Builds: Delta Manifest

Optional delta manifest between the installed build and the update target. It lets the client rebuild most changed files from data already on disk, so an update downloads much less. If it is missing, does not parse or does not fit the new build, the client falls back to a full diff of old vs new manifest ("Delta manifest does not merge, falling back to full diff").

URL: :base/Deltas/:newBuildId/:oldBuildId.delta \
Method: GET \
Auth Required: No

## Path Parameters
`base`: The manifest URL of a mirror without its file name (`https://egdownload.fastly-edge.com/Builds/Fortnite/CloudDir`) <br/>
`newBuildId`: `BuildId` from the new build's manifest meta <br/>
`oldBuildId`: `BuildId` from the installed build's manifest meta (`.egstore\<installationId>.manifest`)

## Example Request

```http
GET /Builds/Fortnite/CloudDir/Deltas/Ui2VxPBjUkymuiCJyoZ-FA/vtuT6fElREubMbN1CCx_7g.delta HTTP/1.1
Host: egdownload.fastly-edge.com
```

Works on all three CDNs, with or without the mirror's query token. When no delta exists for the pair, CloudFront answers `403` and Akamai / Fastly `404`.

---

_Format_

Same binary format as the [Manifest](Manifest.md). It is a manifest of the **new** build (same `buildVersion`, `buildId`, launch info) that only lists the files that changed (with the new file hashes), with chunk parts that point mostly at chunks the **old** build already has, plus the chunk list for everything it references.

Fortnite 42.30 -> 42.40, live:

| | Count |
| --- | --- |
| Delta size | 11,050,606 bytes (zlib), 17.3 MB uncompressed |
| Files in the delta | 449 (every file whose hash changed) |
| Chunks in the delta | 149,599 (144,964 of them are old-build chunks, the rest new) |
| Chunks new to the delta | stored in the normal `ChunksV4` folder of the build, not under `Deltas/` |

## Merging

For every file of the new manifest that the delta lists with the same SHA-1, take the delta's chunk parts; add the delta's chunks to the chunk list. Then plan as usual: a chunk part whose chunk exists in an installed file is read from disk, everything else is downloaded.

For the installed Fortnite (694 selected files): 370 files changed, 44 removed, 63,642 chunks needed, 60,234 rebuilt from local files, **3,408 downloaded (3.01 GB)**. Without the delta, the same update needs 13,286 chunks (12.3 GB).

The launcher:

- skips the delta when both builds have the same id or no installed file changed,
- fetches it with a 10 s header timeout and up to 3 retries,
- can fetch it ahead of the click ("update manifest and delta stored ahead of the click", cached as `<x>.update_delta.<y>`),
- logs `Download.DeltaManifestRequested`, `Fetched`, `Merged` (`file_count`, `chunk_count`), `Unavailable`, `TimedOut`, `Rejected`, `CacheHit`, `Skipped`.
