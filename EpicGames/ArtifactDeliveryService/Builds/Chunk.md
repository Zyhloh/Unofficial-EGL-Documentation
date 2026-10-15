## Artifact Delivery Service - Builds: Chunk

One data chunk of a build. Files are assembled from chunk parts listed in the [Manifest](Manifest.md).

URL: :base/:chunkDir/:group/:hash_:guid.chunk \
Method: GET \
Auth Required: No

Template in the binary: `{base}/{chunkDir}/{group:02}/{hash:016X}_{guid}.chunk`.

## Path Parameters
`base`: The manifest URL of a mirror without its file name (`https://egdownload.fastly-edge.com/Builds/Fortnite/CloudDir` for `.../CloudDir/VPUT6zt1kxXQ4D5n70-gFCFrnLTzQQ.manifest`), or an entry of `cdnBaseUrls` when [Get Asset (v2)](../../LauncherService/Assets/GetAssetV2.md) returns one. On HTTP error, transport error or stall the next base is tried ("Chunk CDN HTTP error, trying next URL", "All CDN URLs failed on attempt") <br/>
`chunkDir`: From the manifest feature level: below 3 `Chunks`, below 6 `ChunksV2`, below 15 `ChunksV3`, otherwise `ChunksV4` (`ChunksV5` and `ChunksV5/plain` exist in the client for newer levels). Live: level 13 uses `ChunksV3`; 17 and 21 use `ChunksV4` <br/>
`group`: Chunk data group from the manifest, 2 decimal digits, zero padded <br/>
`hash`: Chunk rolling hash from the manifest, 16 upper-case hex digits <br/>
`guid`: Chunk GUID, 32 upper-case hex digits

## Query Parameters

The mirror's signed token (`f_token`, `ak_token`, `cf_token`) may be appended. Every chunk tested downloaded with and without it on all three CDNs, for builds with `useSignedUrl: false`.

## Example Request

```http
GET /Builds/Org/o-uy755p5tdy7u56vrmmry4drhhcrhar/836002e0e7e54201b3d4b68a84c3ee4c/default/ChunksV4/89/C9696E33277B9DC3_ACBE9DB02D394A01A1001B4832998900.chunk HTTP/1.1
Host: egdownload.fastly-edge.com
```

_Example header (decoded)_

```json
{
  "magic": "0xB1FE3AA2",
  "version": 3,
  "headerSize": 66,
  "dataSizeCompressed": 426727,
  "guid": "ACBE9DB02D394A01A1001B4832998900",
  "rollingHash": "0xC9696E33277B9DC3",
  "storedAs": 1,
  "sha1": "49d9af4fbed8670e1e54a2574be340973a65338b",
  "hashType": 3,
  "dataSizeUncompressed": 1048576
}
```

## CDN selection

There is no setting, environment variable or flag to pick a CDN, and the launcher never calls a distribution points endpoint. Per download operation:

- Every mirror starts with a failure count of 0. Before each chunk request the bases are sorted by `(failure count, position in the server's list)`, so the server's first mirror is used until it fails.
- An HTTP error, transport error, stall or bad chunk adds 1 to that host's failure count (never reset during the operation) and the next base in the sorted list is tried ("Switched preferred CDN", `Download.CdnFailover`).
- Up to 4 attempts per chunk, each trying every base. Before attempt `n` (from 1) the client waits `(1000 << (n - 1)) + random(0..500)` ms (about 1 s, 2 s, 4 s).
- Stall timeout for the request and the body read: `max(20 s, mean + 4 * stddev)` of the last 100 chunk download times, capped at 60 s.
- 24 to 64 chunk requests run in parallel: the client starts at 24 and adds or removes slots based on latency / throughput.

---

_Format_

Little endian. Header, then the payload.

| Offset | Type | Field | Since version |
| ------ | ---- | ----- | ------------- |
| 0 | uint32 | Magic `0xB1FE3AA2` | 1 |
| 4 | uint32 | Header version | 1 |
| 8 | uint32 | Header size (`41` for v1, `62` for v2, `66` for v3) | 1 |
| 12 | uint32 | Payload size, as stored | 1 |
| 16 | byte[16] | GUID | 1 |
| 32 | uint64 | Rolling hash | 1 |
| 40 | uint8 | Stored as: bit 0 = zlib compressed, bit 1 = encrypted | 1 |
| 41 | byte[20] | SHA-1 of the uncompressed data | 2 |
| 61 | uint8 | Hash type: `1` rolling hash, `2` SHA-1, `3` both | 2 |
| 62 | uint32 | Uncompressed size (`1048576`) | 3 |

Live: version 3 on featureLevel 17 and 21 builds, version 2 on a featureLevel 13 build. The payload starts at the header size; inflate it with zlib when bit 0 is set. Its SHA-1 must equal the chunk's SHA-1 in the manifest.

The launcher decompresses and SHA-1 checks every chunk ("Chunk decompress/verify failed", "SHA1 mismatch for chunk"). Downloaded chunks are kept in `.egstore/chunk_cache` (spilled to disk when the RAM budget is full), so paused or interrupted installs resume without downloading them again.
