## Artifact Delivery Service - Builds: Delta Manifest

Optional delta manifest between the installed build and the update target, used to shrink update downloads. If it is missing, does not parse or does not fit the new build, the client falls back to a full diff of old vs new manifest ("Delta manifest does not merge, falling back to full diff").

URL: :base/Deltas/:a/:b.delta \
Method: GET \
Auth Required: No

Template in the binary: `Deltas/{}/{}.delta`, relative to the manifest's folder (the `CloudDir` the manifest URL points into).

## Path Parameters
`base`: The manifest URL of a mirror without its file name <br/>
`a`, `b`: Build ids of the two builds (manifest meta `BuildId`, or one computed for older manifests: "Using backwards-compatible computed BuildId"). The code does not show which goes first; Epic's legacy layout is `Deltas/<new build id>/<old build id>.delta`.

---

Same binary format as the [Manifest](Manifest.md). The client:

- skips the delta when both builds have the same id or no installed file changed,
- fetches it with a 10 s header timeout and up to 3 retries,
- merges it into the new manifest ("update manifest and delta stored ahead of the click" when prefetched; cached as `<x>.update_delta.<y>`),
- uses a full old vs new diff when it is unavailable or does not merge.

Events: `Download.DeltaManifestRequested`, `Fetched`, `Unavailable`, `TimedOut`, `Merged`, `Rejected`, `CacheHit`, `Skipped`.
