# Hosts

This are some (not all) Hosts that you can access the EOS Auth Service from

- api.epicgames.dev (`prod`)
- api-gamedev.ol.epicgames.net (`gamedev` / `ci`)

<br/>

Recommended Hosts:

- api.epicgames.dev

eglv2 does not call these endpoints from Rust. It hands an exchange code to the bundled EOS SDK (`EOSSDK-Win64-Shipping.dll`) through `EOS_Auth_Login`, and the SDK talks to this service itself. See [EOS Login](../../Launcher/Auth/EOS.md).

Paths found in the SDK string table:

| Path | SDK label |
|---|---|
| `/epic/oauth/v2/token` | `TokenGrantv2` (Auth interface, Epic account login) |
| `/epic/oauth/v2/tokenInfo` | `TokenInfov2` |
| `/epic/oauth/v2/.well-known/jwks.json` | `FetchPublicKeysv2` |
| `/auth/v1/oauth/token` | `TokenExchange` (Connect interface) |
| `/auth/v2/oauth/token` | Connect token grant |
| `/auth/v1/oauth/jwks` | Connect public keys |
| `/auth/v1/users`, `/auth/v1/accounts/deviceid`, `/auth/v1/accounts/self` | Connect user / device id |

The launcher's own environment table also contains `{epic_dev}/auth/v1/oauth/token` (EndpointUrls +0x228), see [OAuth/Token](OAuth/Token.md). The launcher imports no `EOS_Connect_*` functions, so the Connect paths are not exercised by eglv2 itself.

Epic Connect (`wss://connect.epicgames.dev`) is documented under [ConnectService](../ConnectService/README.md).
