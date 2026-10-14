## Artifact Delivery Service - Builds: Chunk

One data chunk of a build. Files are assembled from chunk parts listed in the [Manifest](Manifest.md).

URL: :cdnBaseUrl/:chunkDir/:group/:hash_:guid.chunk \
Method: GET \
Auth Required: No

Template in the binary: `{base}/{chunkDir}/{group:02}/{hash:016X}_{guid}.chunk`.

## Path Parameters
`cdnBaseUrl`: An entry of `cdnBaseUrls` from [Get Asset (v2)](../../LauncherService/Assets/GetAssetV2.md); on HTTP error, transport error or stall the next URL is tried ("Chunk CDN HTTP error, trying next URL", "All CDN URLs failed on attempt") <br/>
`chunkDir`: `Chunks`, `ChunksV2`, `ChunksV3`, `ChunksV4`, `ChunksV5` or `ChunksV5/plain`, from the manifest feature level <br/>
`group`: Chunk data group, 2 digits, zero padded <br/>
`hash`: Chunk rolling hash, 16 upper-case hex digits <br/>
`guid`: Chunk GUID (32 hex characters)

---

Each chunk is decompressed and SHA-1 checked against the manifest ("Chunk decompress/verify failed", "SHA1 mismatch for chunk"). Downloaded chunks are kept in `.egstore/chunk_cache` (spilled to disk when the RAM budget is full) so paused or interrupted installs resume without re-downloading.
