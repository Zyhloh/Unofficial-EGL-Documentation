## Launcher Service - Assets: Get Asset (v2)

Build info for one app on one platform / label: build version, manifest URLs, manifest SHA-1, selective-download metadata URL and CDN base URLs. First step of every install, update, verify, repair, DLC size lookup and selective-download lookup ("Fetching manifest metadata"). Also used for UE engine enumeration (`Enumerating launcher assets label=`).

URL: https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/v2/platform/:platform/namespace/:namespace/catalogItem/:catalogItemId/app/:appName/label/:label \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`platform`: Host platform name, e.g. `Windows` <br/>
`namespace`: Catalog namespace <br/>
`catalogItemId`: Catalog item id <br/>
`appName`: App / artifact id <br/>
`label`: Build label, e.g. `Live` <br/>

The client picks the element whose `appName` and `labelName` match the request ("No build for this platform (no element matched appName and labelName)").

---

_Example Response_

Fortnite, `platform` `Windows`, `label` `Live`. Signed query values replaced with `<signature>`.

```json
{
  "elements": [
    {
      "appName": "Fortnite",
      "labelName": "Live-Windows",
      "buildVersion": "++Fortnite+Release-42.30-CL-58813929-Windows",
      "hash": "597958ab2642d50255c6633cdb98a035a3aeb902",
      "useSignedUrl": false,
      "metadata": {
        "installationPoolId": "FortniteInstallationPool",
        "hasDependencyConfig": true
      },
      "manifests": [
        {
          "uri": "https://egdownload.fastly-edge.com/Builds/Fortnite/CloudDir/VPUT6zt1kxXQ4D5n70-gFCFrnLTzQQ.manifest",
          "queryParams": [
            { "name": "f_token", "value": "<signature>" }
          ]
        },
        {
          "uri": "https://epicgames-download1.akamaized.net/Builds/Fortnite/CloudDir/VPUT6zt1kxXQ4D5n70-gFCFrnLTzQQ.manifest",
          "queryParams": [
            { "name": "ak_token", "value": "<signature>" }
          ]
        },
        {
          "uri": "https://egs-cloudfront-chunks.epicgamescdn.com/Builds/Fortnite/CloudDir/VPUT6zt1kxXQ4D5n70-gFCFrnLTzQQ.manifest",
          "queryParams": [
            { "name": "cf_token", "value": "<signature>" }
          ]
        }
      ],
      "selectiveDownload": [
        {
          "uri": "https://selective-download-egs.distro.on.epicgames.com/Org/o-aa83a0a9bc45e98c80c1b1c9d92e9e/Product/prod-fn/30/303f2a60c3a82195d7ea10e87979707d26974fe937323ad0076f888fe44fd1b2.sdmeta",
          "queryParams": [
            { "name": "cf_token", "value": "<signature>" }
          ]
        }
      ],
      "sdMetaHash": "303f2a60c3a82195d7ea10e87979707d26974fe937323ad0076f888fe44fd1b2",
      "isPreloaded": false
    }
  ]
}
```

A small game without selective download or dependency config (`Grunt`, namespace `5b325322a4c04b9e9e780b9a1e9b2d70`), shortened to one of its three mirrors:

```json
{
  "elements": [
    {
      "appName": "Grunt",
      "labelName": "Live-Windows",
      "buildVersion": "1.2-aeeb6200374fc01a6a51c3006846a350febeb243.21-Win",
      "hash": "b419a862de2fdeffbe546111a860835f3cc93c2c",
      "useSignedUrl": false,
      "manifests": [
        {
          "uri": "https://egs-cloudfront-chunks.epicgamescdn.com/Builds/Org/o-ndzqj36dmhqmfklcq44yywpgfnbmbd/ca72a212479d4f658b053d06fa37330e/default/WykQ0eCx5T2cA283kUmygzrGPAOENw.manifest",
          "queryParams": [
            { "name": "cf_token", "value": "<signature>" }
          ]
        }
      ],
      "isPreloaded": false
    }
  ]
}
```

The client deserializes `AssetsResponse` (`elements`), `AssetElement` (11 fields: `appName`, `labelName`, `buildVersion`, `hash`, `useSignedUrl`, `metadata`, `manifests`, `selectiveDownload`, `sdMetaHash`, `cdnBaseUrls`, `sidecar`), `ManifestUrl` (`uri`, `queryParams`), `ManifestQueryParam` (`name`, `value`), `SelectiveDownloadUrl` (`uri`, `queryParams`, `headers`), `AssetSidecar` (`config`, `rvn`) and `AssetElementMetadata`. `isPreloaded` is not read by the client; `cdnBaseUrls` and `sidecar` were absent in the captures.

- `labelName` is `<label>-<platform>` (`Live-Windows` for a `Live` request).
- `hash` is the manifest SHA-1. Every manifest copy is SHA-1-checked against it; a mismatch rejects that mirror ("Manifest SHA-1 did not match build info, rejecting this copy and trying next"). If `hash` is missing the first copy that parses is accepted.
- Each `manifests[]` entry is a CDN mirror (Fastly `f_token`, Akamai `ak_token`, CloudFront `cf_token`; order varies). The download URL is `uri` with every `queryParams` pair appended as a query string.
- `selectiveDownload` is an array of `.sdmeta` URLs; `metadata` is omitted when the build has none.
- `sdMetaHash` + `buildVersion` are the revalidation key for the cached selective-download info (`sd-cache.json`).
- `metadata.hasDependencyConfig: true` means an [Artifact Dependency Config](../ArtifactDependencies/GetConfig.md) exists for this build; without it that endpoint returns 404.

See [Install and Update](../../../Launcher/Flows/InstallAndUpdate.md).
