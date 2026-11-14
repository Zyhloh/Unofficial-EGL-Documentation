## Artifact Delivery Service - Delivery: Download URLs

Turns chunk paths into download URLs for a signed ticket. Used since launcher 0.115 for builds whose [Get Asset (v2)](../../LauncherService/Assets/GetAssetV2.md) element has `useSignedUrl: true`: the launcher signs chunks ahead in batches ("Signed chunk URLs for the download in N batches") and falls back to signing on demand.

URL: https://artifact-delivery-service-public-prod.ol.epicgames.com/artifact-delivery/api/public/v1/delivery/account/:accountId/downloadurls \
Method: POST \
Auth Required: Yes (Bearer access token; the ticket goes in the body)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Correlation-ID`: random UUID <br/>

## Path Parameters
`accountId`: Your account id

## Body
```json
{
  "signedTicket": "eyJzaGFyZElkIjoiZWdzIiwi...",
  "chunkIds": [
    "ChunksV4/76/32BBCF7BA2967AE3_1FF228864B57C5A9D0328B9D25E346B3.chunk",
    "ChunksV4/48/A4BD8349A55FDAD6_E0750C1846B5239C1A446E93B8CC8D42.chunk"
  ],
  "deltaId": null,
  "clientMetrics": {}
}
```

`signedTicket`: From [Create Download Ticket](../../LauncherService/Assets/CreateTicket.md), required <br/>
`chunkIds`: Chunk paths relative to the build folder, exactly as in [Chunk](../Builds/Chunk.md) (`ChunksV4/<group>/<hash>_<guid>.chunk`). Just `<hash>_<guid>`, the GUID or the file name are refused <br/>
`deltaId`, `clientMetrics`: Sent by the launcher; optional

---

_Example Response_

```json
{
  "ChunksV4/76/32BBCF7BA2967AE3_1FF228864B57C5A9D0328B9D25E346B3.chunk": "https://egs-cloudfront-chunks.epicgamescdn.com/Builds/Fortnite/CloudDir/ChunksV4/76/32BBCF7BA2967AE3_1FF228864B57C5A9D0328B9D25E346B3.chunk",
  "ChunksV4/48/A4BD8349A55FDAD6_E0750C1846B5239C1A446E93B8CC8D42.chunk": "https://egs-cloudfront-chunks.epicgamescdn.com/Builds/Fortnite/CloudDir/ChunksV4/48/A4BD8349A55FDAD6_E0750C1846B5239C1A446E93B8CC8D42.chunk"
}
```

The server picks the CDN per request (one call answered with Fastly URLs, the next with CloudFront). For Fortnite, whose build does not ask for signed URLs, the URLs carry no signature; for signed builds the launcher uses whatever query string comes back without parsing it.

_Example Response (chunk id not in path form)_

```json
{
  "errorCode": "errors.com.epicgames.artifactdelivery.unauthorized",
  "errorMessage": "Invalid chunkId found.",
  "intent": "prod",
  "messageVars": [],
  "numericErrorCode": 1002,
  "originatingService": "artifact-delivery-service-springboot"
}
```

Other errors: `signedTicket cannot be null.` / `Invalid signedTicket.` (400 `errors.com.epicgames.artifactdelivery.bad_request`, 1001); the ticket as Bearer instead of the access token gives 401 `errors.com.epicgames.common.authentication.token_verification_failed`. Error codes in the launcher: `signed_ticket_expired`, `artifactdelivery.forbidden`, `distribution_point_not_found`, `no_distribution_point_found`.
