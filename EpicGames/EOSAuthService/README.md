# Hosts

This are some (not all) Hosts that you can access the EOS Auth Service from

- api.epicgames.dev (`prod`)
- api-gamedev.ol.epicgames.net (`gamedev` / `ci`)

<br/>

Recommended Hosts:

- api.epicgames.dev

eglv2 does not call these endpoints from Rust. It hands an exchange code to the bundled EOS SDK (`EOSSDK-Win64-Shipping.dll`, `1.19.4230.0-57929184@LauncherV2`) through `EOS_Auth_Login`, and the SDK talks to this service itself. See [EOS Login](../../Launcher/Auth/EOS.md).

## How the SDK picks the host

Only the SDK config service URL is compiled in: an XOR-obfuscated ini inside the DLL holds `[SDKConfig] BaseUrl="https://api.epicgames.dev/sdk"` (`[SDKConfig GameDev]` = `https://api-gamedev.ol.epicgames.net/sdk`). Every other base URL comes from the `services` map of [Platform Config](../EOSSDKConfigService/Config/PlatformConfig.md), keyed by the route's service name plus `Service`:

| SDK route service | Config key | BaseUrl (prod, live `services` map) | Paths |
|---|---|---|---|
| `OAuth` (Epic account client, config name `AccountsEpicId`) | `AccountsEpicIdService` | `https://api.epicgames.dev` | `/epic/oauth/v2/*`, `/epic/id/v2/*` |
| `EOSAuth` (Connect client) | `EOSAuthService` | `https://api.epicgames.dev` | `/auth/v1/*`, `/auth/v2/*` |

Common SDK headers: `X-Epic-Correlation-ID` on every route, `X-Epic-Login-ID` and `DPoP` (once `EOS_Auth_ConfigureDpop` ran, retried with `DPoP-Nonce`) on Epic account auth tasks. Client authentication is `Basic base64(client_id:client_secret)`.

## Endpoints used by eglv2 (through the SDK)

- [OAuth/EpicToken](OAuth/EpicToken.md) - `POST /epic/oauth/v2/token` (login, refresh)
- [OAuth/TokenInfo](OAuth/TokenInfo.md) - `POST /epic/oauth/v2/tokenInfo` (periodic verify)
- [OAuth/Revoke](OAuth/Revoke.md) - `POST /epic/oauth/v2/revoke` (logout)
- [OAuth/Exchange](OAuth/Exchange.md) - `GET /epic/oauth/v2/exchange` (social overlay exchange code)
- [OAuth/PublicKeys](OAuth/PublicKeys.md) - `GET /epic/oauth/v2/.well-known/jwks.json`
- [Account/SdkAccounts](Account/SdkAccounts.md) - `GET /epic/id/v2/sdk/accounts` (UserInfo lookups, use by eglv2 not confirmed)

## In the SDK, not reachable from eglv2

| Path | SDK route | Why unused |
|---|---|---|
| `POST /epic/oauth/v2/deviceAuthorization` | `InitiateDeviceFlowv2` | Device code login, eglv2 logs in with `EOS_LCT_ExchangeCode` only |
| `POST /epic/id/v2/externalAuths` | `ExternalAuthLinkingv2` | `EOS_Auth_LinkAccount`, not imported |
| `POST /auth/v1/oauth/token` | `TokenGrant` | Connect / client credentials, see [OAuth/Token](OAuth/Token.md) |
| `POST /auth/v2/oauth/token` | `TokenExchange` | Connect token exchange (`urn:ietf:params:oauth:grant-type:token-exchange`) |
| `GET /auth/v1/oauth/jwks` | `FetchPublicKeys` | Connect public keys |
| `/auth/v1/users`, `/auth/v1/accounts/deviceid`, `/auth/v1/accounts/self`, `/auth/v1/accounts`, `/auth/v1/account-transfers` | Connect `Link`, `Create`, `Unlink`, `AccountTransfer` | Connect user / device id |

The launcher imports no `EOS_Connect_*` function. The SDK can still request a client token on its own (`Unable to get the client auth token`), which would go to `/auth/v1/oauth/token`; not confirmed.

The launcher's own environment table also contains `{epic_dev}/auth/v1/oauth/token` (EndpointUrls +0x228), see [OAuth/Token](OAuth/Token.md).

Epic Connect (`wss://connect.epicgames.dev`) is documented under [ConnectService](../ConnectService/README.md).
