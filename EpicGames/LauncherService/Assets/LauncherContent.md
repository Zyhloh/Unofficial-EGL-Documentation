## Launcher Service - Assets: Launcher Content Build

Build info for the `EpicGamesLauncherContent` app (label `Live-Krampus`). The partner bootstrap (`src\partner\bootstrap.rs`) downloads this build's manifest and pulls the partner client installers out of it (`EA/EAappInstaller.exe`, `UbisoftConnect/UbisoftConnectInstaller.exe`), caching them with a `build-version.txt` marker ("partner content build info", "Downloaded the partner client installer from the launcher content build").

URL: https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/v2/platform/:platform/launcher \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`platform`: `Windows`

## Query Parameters
`label`: `Live-Krampus` <br/>

---

_Example Response (manifest tokens shortened)_

Same `AssetsResponse` shape as [Get Asset (v2)](GetAssetV2.md). It returns two elements, the old launcher (`EpicGamesLauncher`) and the content build; the client selects the element with `appName` `EpicGamesLauncherContent`.

```json
{
  "elements": [
    {
      "appName": "EpicGamesLauncher",
      "buildVersion": "20.3.8-60034553+++UE5+Release-Distro-5.5-Windows",
      "hash": "a251afbffd08511a1d791643ecedddf5f3116db9",
      "isPreloaded": false,
      "labelName": "Live-Krampus-Windows",
      "manifests": [
        {
          "queryParams": [
            { "name": "Expires", "value": "1794626250" },
            { "name": "KeyName", "value": "epic-key-01" },
            { "name": "Signature", "value": "..." }
          ],
          "uri": "https://google.epicgamescdn.com/Builds/UnrealEngineLauncher/CloudDir/0_iQRSxNUEQ8f8fmfkC_nzoIs3XTEw.manifest"
        },
        {
          "queryParams": [ { "name": "cf_token", "value": "1794626250_..." } ],
          "uri": "https://egs-cloudfront-chunks.epicgamescdn.com/Builds/UnrealEngineLauncher/CloudDir/0_iQRSxNUEQ8f8fmfkC_nzoIs3XTEw.manifest"
        }
      ],
      "metadata": { "status": "NOT_DEPRECATED" },
      "useSignedUrl": false
    },
    {
      "appName": "EpicGamesLauncherContent",
      "buildVersion": "++UE5+Dev-Distro-5.5+prod-CL-60376003-Windows",
      "hash": "7152271c2ad5409a6c07f8072de7247245b8db4f",
      "isPreloaded": false,
      "labelName": "Live-Krampus-Windows",
      "manifests": [
        {
          "queryParams": [ { "name": "cf_token", "value": "1794626250_..." } ],
          "uri": "https://egs-cloudfront-chunks.epicgamescdn.com/Builds/UnrealEngineLauncher/CloudDir/Wan8NU8tD0fF3JDUAkiDAwj5K5DHPg.manifest"
        },
        {
          "queryParams": [ { "name": "ak_token", "value": "exp=1794626250~hmac=..." } ],
          "uri": "https://epicgames-download1.akamaized.net/Builds/UnrealEngineLauncher/CloudDir/Wan8NU8tD0fF3JDUAkiDAwj5K5DHPg.manifest"
        },
        {
          "queryParams": [ { "name": "f_token", "value": "1794626250_..." } ],
          "uri": "https://egdownload.fastly-edge.com/Builds/UnrealEngineLauncher/CloudDir/Wan8NU8tD0fF3JDUAkiDAwj5K5DHPg.manifest"
        }
      ],
      "useSignedUrl": false
    }
  ]
}
```

`labelName` comes back as `Live-Krampus-Windows`. The old launcher element has four mirrors (Google, CloudFront, Akamai, Fastly; two shown) and a `metadata.status`. The content element has three mirrors and no `metadata`.
