## Launcher Service - Assets: Get Asset (v2)

Build info for one app on one platform / label: build version, manifest URLs, manifest SHA-1, selective-download metadata URL and CDN base URLs. First step of every install, update, verify, repair, DLC size lookup and selective-download lookup ("Fetching manifest metadata"). Also used for UE engine enumeration (`Enumerating launcher assets label=`).

URL: https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/v2/platform/:platform/namespace/:namespace/catalogItem/:catalogItemId/app/:appName/label/:label \
Method: GET \
Auth Required: Yes (Bearer access token)

GET is inferred: the request has no body type in the client and only the URL is built (`assets_v2_element_url`).

## Path Parameters
`platform`: Host platform name, e.g. `Windows` <br/>
`namespace`: Catalog namespace <br/>
`catalogItemId`: Catalog item id <br/>
`appName`: App / artifact id <br/>
`label`: Build label, e.g. `Live` <br/>

The client picks the element whose `appName` and `labelName` match the request ("No build for this platform (no element matched appName and labelName)").

---

_Example Response (shape from client)_

```json
{
  "elements": [
    {
      "appName": "Fortnite",
      "labelName": "Live",
      "buildVersion": "++Fortnite+Release-32.00-CL-12345678-Windows",
      "hash": "94b1569506b04f9f8557af611e8c5e4794b15695",
      "useSignedUrl": true,
      "metadata": {
        "hasDependencyConfig": false
      },
      "manifests": [
        {
          "uri": "https://<cdn host>/Builds/Org/o-xxxx/94b1569506b04f9f8557af611e8c5e47/default/abcdef.manifest",
          "queryParams": [
            { "name": "f_token", "value": "..." }
          ]
        }
      ],
      "selectiveDownload": {
        "uri": "https://<cdn host>/.../abcdef.sdmeta",
        "queryParams": [],
        "headers": []
      },
      "sdMetaHash": "94b1569506b04f9f8557af611e8c5e4794b15695",
      "cdnBaseUrls": [
        "https://<cdn host>/Builds/Org/o-xxxx/94b1569506b04f9f8557af611e8c5e47/default"
      ],
      "sidecar": {
        "config": "{}",
        "rvn": 1
      }
    }
  ]
}
```

Field names from `AssetsResponse` (`elements`), `AssetElement` (11 fields: `appName`, `labelName`, `buildVersion`, `hash`, `useSignedUrl`, `metadata`, `manifests`, `selectiveDownload`, `sdMetaHash`, `cdnBaseUrls`, `sidecar`), `ManifestUrl` (`uri`, `queryParams`), `ManifestQueryParam` (`name`, `value`), `SelectiveDownloadUrl` (`uri`, `queryParams`, `headers`), `AssetSidecar` (`config`, `rvn`) and `AssetElementMetadata` (`hasDependencyConfig` is the only key found next to it, so its placement here is inferred; other metadata keys not recovered). URIs, query parameter names and values are placeholders.

- `hash` is the manifest SHA-1. Every manifest copy is SHA-1-checked against it; a mismatch rejects that mirror ("Manifest SHA-1 did not match build info, rejecting this copy and trying next"). If `hash` is missing the first copy that parses is accepted.
- Each `manifests[]` entry is a mirror. The download URL is `uri` with every `queryParams` pair appended as a query string (inferred from the struct; the signing parameters are not visible statically).
- `sdMetaHash` + `buildVersion` are the revalidation key for the cached selective-download info (`sd-cache.json`).
- `metadata.hasDependencyConfig` presumably gates [Artifact Dependency Config](../ArtifactDependencies/GetConfig.md) (inferred from the name).

See [Install and Update](../../../Launcher/Flows/InstallAndUpdate.md).
