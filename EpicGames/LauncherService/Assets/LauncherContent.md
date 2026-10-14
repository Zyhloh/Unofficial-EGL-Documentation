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

_Example Response (shape from client)_

Same `AssetsResponse` shape as [Get Asset (v2)](GetAssetV2.md); the client selects the element with `appName` `EpicGamesLauncherContent`.

```json
{
  "elements": [
    {
      "appName": "EpicGamesLauncherContent",
      "labelName": "Live-Krampus",
      "buildVersion": "1.0.0-12345678",
      "hash": "94b1569506b04f9f8557af611e8c5e4794b15695",
      "useSignedUrl": false,
      "manifests": [
        { "uri": "https://<cdn host>/.../content.manifest", "queryParams": [] }
      ]
    }
  ]
}
```
