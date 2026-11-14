## Launcher Service - Assets: Create Download Ticket

Issues a signed ticket for one build. The ticket is the input of [Download URLs](../../ArtifactDeliveryService/Delivery/DownloadUrls.md), which signs chunk URLs. Since 0.115 the launcher does this when [Get Asset (v2)](GetAssetV2.md) says `useSignedUrl: true` ("Build info asks for signed chunk URLs; signing every chunk"); 0.95 ignored `useSignedUrl`.

URL: https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/v2/ticket \
Method: POST \
Auth Required: Yes (Bearer access token)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Correlation-ID`: random UUID <br/>

## Body
```json
{
  "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
  "buildVersion": "++Fortnite+Release-43.10-CL-60118918-Windows",
  "appName": "Fortnite",
  "namespace": "fn",
  "label": "Live",
  "platform": "Windows"
}
```

`buildVersion`: `buildVersion` of the Get Asset (v2) element

---

_Example Response_

```json
{
  "createdAt": "2026-11-14T02:59:34.107401420Z",
  "expiresAt": "2026-11-14T03:04:34.000Z",
  "signedTicket": "eyJzaGFyZElkIjoiZWdzIiwiYXJ0aWZhY3RJZCI6IkZvcnRuaXRlIiwi...=.YjcwY2RmOTJjY2E2NWI4OTdlYmRl...=="
}
```

The ticket is valid for 5 minutes. `signedTicket` is `<base64 JSON>.<base64 signature>`; the JSON part decodes to:

```json
{
  "shardId": "egs",
  "artifactId": "Fortnite",
  "grantAccessToDependencies": false,
  "expiresAt": "2026-11-14T03:04:34Z",
  "accountId": "94b1569506b04f9f8557af611e8c5e47",
  "binaryVersion": "++Fortnite+Release-43.10-CL-60118918-Windows"
}
```

A ticket was issued for Fortnite even though its build does not ask for signed URLs. The launcher logs `Download.SignedTicketFetched` ("Fetched a signed download ticket valid for Ns") and gives up after the ticket is refused as expired twice.
