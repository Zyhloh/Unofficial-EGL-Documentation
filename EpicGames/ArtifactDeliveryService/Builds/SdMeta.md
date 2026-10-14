## Artifact Delivery Service - Builds: Selective Download Metadata

The `.sdmeta` file: the optional components (language packs, HD textures, ...) of a build and the install tags each one maps to. Backs `get_selective_download_info` and the install dialog component list. Cached in `sd-cache.json` keyed by app, platform, locale, `buildVersion` and `sdMetaHash`; a cache hit is served immediately and revalidated in the background (`selective-download-info-updated-event`).

URL: `selectiveDownload.uri` from [Get Asset (v2)](../../LauncherService/Assets/GetAssetV2.md), with its `queryParams` and `headers` \
Method: GET \
Auth Required: No

The client tries the URL(s) in turn ("`.sdmeta` URL failed, trying next", "All .sdmeta CDN URLs failed"). If the build has no `.sdmeta`, components are derived from the manifest's install tags instead ("No .sdmeta and not a UE tab product", "Derived SD components from manifest install tags").

---

_Example Response (shape from client)_

```json
{
  "components": [
    {
      "Title": "High Resolution Textures",
      "Title_translate": false,
      "Description": "4K texture pack",
      "IsRequired": false,
      "UniqueId": "94b1569506b04f9f8557af611e8c5e47",
      "IsDefaultSelected": false,
      "Tags": ["highres"],
      "Invisible": false,
      "TotalInstallSize": 0,
      "TotalDownloadSize": 0
    }
  ]
}
```

Per-component keys from the binary (`Title`, `Title_translate`, `Description`, `IsRequired`, `UniqueId`, `IsDefaultSelected`, `Tags`, `Invisible`, `TotalInstallSize`, `TotalDownloadSize`). The top-level layout of the file was not recovered; the `components` wrapper above is a placeholder. Missing sizes are recomputed from the manifest.

The IPC result (`SelectiveDownloadInfo`) is `{ components: SdComponent[], baseDownloadSize, baseInstallSize }`, where `SdComponent` has `title`, `titleTranslate`, `description`, `isRequired`, `uniqueId`, `isDefaultSelected`, `tags`, `requires`, `invisible`, `downloadSize` and one more field that was not separated from neighbouring strings (11 in total).
