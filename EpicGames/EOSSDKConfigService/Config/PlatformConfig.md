## EOS SDK Config Service - Config: Platform Config

Default config for every EOS title on a platform. Fetched by the EOS SDK (`FSDKConfigPlatformUpdateTask`, route `GetPlatformConfigRoute`) when the launcher creates its EOS platform. Holds client settings (rate limits, timeouts, overlay URLs) and the `services` map with every service base URL.

URL: https://api.epicgames.dev/sdk/v1/default \
Method: GET \
Auth Required: No (the SDK may attach a token; the endpoint answers without one)

## Headers
`X-Epic-Correlation-ID`: random id <br/>

## Query Parameters
`platformId`: SDK platform id, `WIN` on Windows (value inferred from the SDK platform string table) <br/>

---

_Example Response (live, trimmed)_

```json
{
  "client": {
    "AuthClient": {
      "VerifyTokenInterval": 60.0,
      "RefreshTokenThreshold": 100.0,
      "IdTokenCacheMinExpirySeconds": 300
    },
    "UIClient": {
      "FriendsURL": "https://api.epicgames.dev/overlay-override/v1/",
      "SocialSPAClientId": "cf27c69fe66441e8a8a4e8faf396ee4c",
      "FriendsURLExchangeCodeSuffix": "?exchange_code=`exchange_code"
    },
    "Messaging.EpicConnect": {
      "Urlv2": "wss://connect.epicgames.dev/v2"
    },
    "SDKAnalytics": {
      "BaseUrl": "https://api.epicgames.dev/telemetry/data/",
      "UploadType": "sdkevents"
    }
  },
  "services": {
    "AccountsEpicIdService": { "BaseUrl": "https://api.epicgames.dev" },
    "EOSAuthService": { "BaseUrl": "https://api.epicgames.dev" },
    "EULATrackingService": { "BaseUrl": "https://eulatracking-public-service-prod06.ol.epicgames.com/eulatracking" },
    "MetricsService": { "BaseUrl": "https://api.epicgames.dev/datarouter" },
    "PartiesService": { "BaseUrl": "https://api.epicgames.dev/epic/party" },
    "PresenceService": { "BaseUrl": "https://api.epicgames.dev/epic/presence" },
    "RTCService": { "BaseUrl": "https://api.epicgames.dev/rtc" },
    "ReportsService": { "BaseUrl": "https://api.epicgames.dev/player-reports" },
    "SanctionsService": { "BaseUrl": "https://api.epicgames.dev/sanctions" }
  },
  "watermark": 794601937
}
```

The live `services` map (`platformId=WIN`) has 40 entries; there is no `EmeraldService` entry, so the Emerald host must come from [Product Config](ProductConfig.md).
