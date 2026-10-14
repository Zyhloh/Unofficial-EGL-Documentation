## Artifact Delivery Service - Builds: Delta Manifest

Optional delta manifest between the installed build and the update target, used to shrink update downloads. If it is missing, does not parse or does not fit the new build, the client falls back to a full diff of old vs new manifest ("Delta manifest does not merge, falling back to full diff").

URL: :cdnBaseUrl/Deltas/:a/:b.delta \
Method: GET \
Auth Required: No

Template in the binary: `Deltas/{}/{}.delta`, relative to a CDN base URL.

## Path Parameters
`cdnBaseUrl`: An entry of `cdnBaseUrls` <br/>
`a`, `b`: Build ids of the two builds. The binary only shows the template; that `a` is the new build and `b` the installed build is inferred from Epic's legacy layout. Build ids come from the manifest meta (`BuildId`) or are computed for older manifests ("Using backwards-compatible computed BuildId").

---

Same chunked manifest format as [Manifest](Manifest.md).
