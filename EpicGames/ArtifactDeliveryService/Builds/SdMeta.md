## Artifact Delivery Service - Builds: Selective Download Metadata

The `.sdmeta` file: the optional components of a build and the install tags each one maps to. Backs `get_selective_download_info` and the component list of the install dialog. Cached in `sd-cache.json` keyed by namespace, item, app, platform, locale, `buildVersion` and `sdMetaHash`; a cache hit is served immediately and revalidated in the background (`selective-download-info-updated-event`).

URL: `selectiveDownload[].uri` from [Get Asset (v2)](../../LauncherService/Assets/GetAssetV2.md), with its `queryParams` \
Method: GET \
Auth Required: No (the query token is the authorization)

Only builds that have optional components return `selectiveDownload` (Fortnite). The file name is the `sdMetaHash` of the element (SHA-256). The client tries the URLs in turn ("`.sdmeta` URL failed, trying next", "All .sdmeta CDN URLs failed"). Without a `.sdmeta`, components are derived from the manifest install tags ("Derived SD components from manifest install tags").

## Example Request

```http
GET /Org/o-aa83a0a9bc45e98c80c1b1c9d92e9e/Product/prod-fn/30/303f2a60c3a82195d7ea10e87979707d26974fe937323ad0076f888fe44fd1b2.sdmeta?cf_token=1792033224_e2f9107c0c1f4c0f2452409b9cd8a31ba5225cfe HTTP/1.1
Host: selective-download-egs.distro.on.epicgames.com
```

---

_Example Response (Fortnite, shortened)_

```json
{
  "DataType": "SelDlMeta",
  "Data": [
    {
      "Title": "Fortnite Core and Battle Royale",
      "Title_translate": "true",
      "UniqueId": "A17316661F902216B15E8DAB34ECCD71",
      "IsRequired": "true",
      "Tags": ["Startup", "FrontEnd", "Encrypted", "Globals", "DefaultGameplayChunk", "FortniteBR", "FNOne", "Langde", "Langfr", "Langpl", "Langru", ""]
    },
    {
      "Title": "Epic Quality Assets (Streamed by default)",
      "Title_translate": "true",
      "Description": "Epic quality textures are streamed on demand by default. To reduce downloads during gameplay, they can optionally be installed.",
      "Description_translate": "true",
      "UniqueId": "BC27D46CFC5347479B3F118F9A31EA06",
      "IsRequired": "false",
      "IsDefaultSelected": "false",
      "Tags": ["StartupOptional", "FrontEndOptional", "EncryptedOptional", "FortniteBREpicOptionalInstall"],
      "Title_fr": "Ressources de qualité Epic (diffusées en continu par défaut)",
      "Description_fr": "Par défaut, les textures de qualité Epic sont diffusées en continu à la demande. ..."
    }
  ]
}
```

`DataType`: Always `SelDlMeta` <br/>
`Data[].Title`, `Description`: English text; `Title_<locale>` / `Description_<locale>` hold translations (`fr`, `it`, `de`, `es`, `es-MX`, `ru`, ...) when `*_translate` is `"true"` <br/>
`Data[].UniqueId`: Component id, stored in the install record (`componentSelection.selected`) <br/>
`Data[].IsRequired`, `IsDefaultSelected`: Booleans written as the strings `"true"` / `"false"`; either key can be missing (treat as false) <br/>
`Data[].Tags`: Manifest install tags the component installs. `""` stands for the untagged files <br/>
Also read by the client when present: `Invisible`, `TotalInstallSize`, `TotalDownloadSize`; missing sizes are computed from the manifest.

A component is installed when it is required or selected. The selected tag set is the union of the `Tags` of those components, and a file is installed when it has no tags or any of its tags is in the set. For the Fortnite build above: required only = 611 files / 37.6 GB, with Epic Quality Assets = 694 files / 66.3 GB, whole manifest = 891 files / 159.4 GB (the rest belongs to add-ons, see [Add-ons](../../../Launcher/Library/Addons.md)).

The IPC result (`SelectiveDownloadInfo`) is `{ components: SdComponent[], baseDownloadSize, baseInstallSize }`, where `SdComponent` has `title`, `titleTranslate`, `description`, `isRequired`, `uniqueId`, `isDefaultSelected`, `tags`, `requires`, `invisible`, `downloadSize` and one more field that was not separated from neighbouring strings.
