## EOS SDK Config Service - Config: Product Config

Per-product SDK configuration: the same `client` / `services` / `watermark` document as the public [Platform Config](PlatformConfig.md), with the product's overrides applied. Fetched by the EOS SDK after the platform is created.

URL: https://api.epicgames.dev/sdk/v1/product/:productId \
Method: GET \
Auth Required: Yes (EOS client token from [Token (v1)](../../EOSAuthService/OAuth/Token.md) `client_credentials`)

## Path Parameters
`productId`: EOS product id, `42c61cfdc3d24af5a8333b3284d47240` for the launcher

## Query Parameters
`platformId`: SDK platform, e.g. `WIN` (optional; the same document came back without it) <br/>
`deploymentId`: EOS deployment, `83364c64d38841d49c4de2f6f0eb3360` for the launcher (optional)

## Headers
`X-Epic-Correlation-ID`: random id (sent by the SDK) <br/>
`If-None-Match`: sent by the SDK when it has a previous copy; no `ETag` was returned live

---

_Example Response (launcher product, shortened)_

```json
{
  "client": {
    "BaseService": { "HttpRetryLimit": 4, "HttpRetryResponseCodes": [429, 503, 504] },
    "Messaging.EpicConnect": {
      "bDisableWebSocket": true,
      "EpicGlobalSubscriptionCoordinates": ["ec-coord-temporary-subscription=parties-internal"],
      "FailedConnectionDelayMultiplier": 2.5,
      "RetryBackoffMaxSeconds": 180
    },
    "Messaging.Stomp": {
      "bDisableWebSocket": true,
      "Url": "wss://api.epicgames.dev/notifications/v1/`deploymentid`/connect",
      "ClientHeartbeatIntervalMs": 30000,
      "BlocklistMessageTypeFilters": ["lobbyinvite", "matchmakinginvite"]
    },
    "MetricsClient.Heartbeat": { "RecordRate": 0 },
    "SDKAnalytics.Heartbeat": { "RecordRate": 300 },
    "RateLimiter.PresenceClient.Operations": { "MessageCount": 3, "TimeIntervalInSeconds": 20.0, "Operation": ["SendUpdate", "SetPresence"] },
    "UIClient.SocialURLQueryParamNames": {
      "OSName": "os_name",
      "ProductId": "product_id",
      "DeploymentId": "deployment_id",
      "ExchangeCode": "exchange_code"
    }
  },
  "services": {
    "AccountsService": { "BaseUrl": "https://egp-idsoc-proxy-prod.ol.epicgames.com/account", "RedirectUrl": "accounts.epicgames.com" },
    "PartiesInternalService": { "BaseUrl": "https://api.epicgames.dev/epic/party/internal" },
    "PresenceService": { "BaseUrl": "https://api.epicgames.dev/epic/presence" },
    "ReportsService": { "BaseUrl": "https://api.epicgames.dev/player-reports" },
    "RTCService": { "BaseUrl": "https://api.epicgames.dev/rtc" },
    "DataStorageService": { "BaseUrl": "https://api.epicgames.dev/datastorage" }
  },
  "watermark": 794601937
}
```

The launcher product's config has the same 39 services and the same URLs as the platform config. The only differences are 4 client overrides:

| Key | Override |
| --- | -------- |
| `Messaging.EpicConnect` | `bDisableWebSocket: true` |
| `Messaging.Stomp` | `bDisableWebSocket: true` |
| `MetricsClient.Heartbeat` | `RecordRate: 0` |
| `SDKAnalytics.Heartbeat` | `RecordRate: 300` |

So the SDK inside the launcher opens no Connect / notifications websocket of its own (the launcher runs [Epic Connect](../../../Launcher/Social/Connect.md) itself) and sends no metrics heartbeat. There is no `EmeraldService` entry.

_Example Response (Epic account token from [Epic Account Token](../../EOSAuthService/OAuth/EpicToken.md))_

```json
{
  "errorCode": "errors.com.epicgames.common.oauth.invalid_token",
  "errorMessage": "Jwks doesn't have key to match kid or alg from Jwt",
  "messageVars": [],
  "numericErrorCode": 1014,
  "originatingService": "eos-gateway",
  "intent": "prod"
}
```
