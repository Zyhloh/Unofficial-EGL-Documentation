## Fab - Artifacts: Get Manifest

Resolves the download manifest of one Fab artifact (`Fab artifact manifest resolved`). Used for Fab installs into projects / engines (`fab::ue_download`) and launcher asset enumeration.

URL: https://www.fab.com/e/artifacts/:artifactId/manifest \
Method: POST \
Auth Required: Yes (Bearer access token)

## Path Parameters
`artifactId`: `projectVersions[].artifactID` from [Get Library](../Library/GetLibrary.md)

The method byte in the request matches the one used by quick purchase (POST); the request body was not recovered.

---

_Example Response (shape from client, `FabManifestResponse` / `FabDownloadInfo` / `FabDistributionPoint`)_

```json
{
  "downloadInfo": [
    {
      "assetFormat": "...",
      "buildVersion": "...",
      "manifestHash": "...",
      "distributionPointBaseUrls": ["https://..."],
      "distributionPoints": [
        {
          "manifestUrl": "https://...",
          "signatureExpiration": "2026-10-14T16:00:00.000Z"
        }
      ]
    }
  ]
}
```

No `downloadInfo` is `Fab manifest response carried no downloadInfo`.
