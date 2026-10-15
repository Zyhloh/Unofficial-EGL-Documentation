## Fab - Artifacts: Get Manifest

Resolves the download manifest of one Fab artifact (`Fab artifact manifest resolved`). Used for Fab installs into projects / engines (`fab::ue_download`) and launcher asset enumeration.

URL: https://www.fab.com/e/artifacts/:artifactId/manifest \
Method: POST \
Auth Required: Yes (Bearer access token)

## Path Parameters
`artifactId`: `projectVersions[].artifactID` from [Get Library](../Library/GetLibrary.md)

## Headers
`Content-Type`: application/json <br/>

## Body
```json
{
  "itemId": "26757664d35f47088139090bd7f73a81",
  "namespace": "89efe5924d3d467c839449ab6ab52e7f",
  "platform": "Windows"
}
```

`itemId`: `assetId` from [Get Library](../Library/GetLibrary.md) (the `legacyItemId` gives a 500) <br/>
`namespace`: `assetNamespace` from the library <br/>
`platform`: `Windows` / `Mac`

---

_Example Response_

```json
{
  "downloadInfo": [
    {
      "type": "manifest",
      "assetFormat": "asset-format/game-engine/unreal-engine",
      "artifactId": "MilitaryWeapDark",
      "buildVersion": "4.21.0-6954822+++depot+UE4-UserContent-Windows",
      "manifestHash": "08eca889a2fe9222766de7449e8725c29af3b92c",
      "metadata": {},
      "distributionPoints": [
        {
          "manifestUrl": "https://egdownload.fastly-edge.com/Builds/Rocket/Automated/MilitaryWeapDark/CloudDir/MilitaryWeapDark4.21.0-6954822%2B%2B%2Bdepot%2BUE4-UserContent-Windows.manifest?f_token=1792068127_e2a8e9673f789d3961c02c13d54f60b78b1a850e",
          "signatureExpiration": "2026-10-15T12:42:07.906Z"
        },
        {
          "manifestUrl": "https://epicgames-download1.akamaized.net/Builds/Rocket/Automated/MilitaryWeapDark/CloudDir/MilitaryWeapDark4.21.0-6954822%2B%2B%2Bdepot%2BUE4-UserContent-Windows.manifest?ak_token=exp=1792068127~hmac=0bcd6048631d0a5de7b3bacd26de7bf857d10b738046aa0f4f76476ad55426dc",
          "signatureExpiration": "2026-10-15T12:42:07.906Z"
        },
        {
          "manifestUrl": "https://egs-cloudfront-chunks.epicgamescdn.com/Builds/Rocket/Automated/MilitaryWeapDark/CloudDir/MilitaryWeapDark4.21.0-6954822%2B%2B%2Bdepot%2BUE4-UserContent-Windows.manifest?cf_token=1792068127_890d5b4a882cb2e1411fb726d275be435d66fd83",
          "signatureExpiration": "2026-10-15T12:42:07.906Z"
        }
      ],
      "distributionPointBaseUrls": [
        "https://egs-cloudfront-chunks.epicgamescdn.com/Builds/Rocket/Automated/MilitaryWeapDark/CloudDir",
        "https://epicgames-download1.akamaized.net/Builds/Rocket/Automated/MilitaryWeapDark/CloudDir",
        "https://egdownload.fastly-edge.com/Builds/Rocket/Automated/MilitaryWeapDark/CloudDir"
      ]
    }
  ]
}
```

The manifest and its chunks are the same [Manifest](../../../ArtifactDeliveryService/Builds/Manifest.md) / [Chunk](../../../ArtifactDeliveryService/Builds/Chunk.md) format as game builds; `distributionPointBaseUrls` are the chunk bases. `manifestHash` is the SHA-1 of the manifest file. The signed URLs expire after about 5 minutes (`signatureExpiration`). The Akamai token here is `exp=<unix>~hmac=<hex>`.

_Example Response (missing body fields)_

```json
{
  "detail": {
    "namespace": ["This field is required."],
    "itemId": ["This field is required."],
    "platform": ["This field is required."]
  }
}
```
