## EOS Auth Service - OAuth: Epic Account Token (v2)

Called by the EOS SDK, not by eglv2's Rust code, when the launcher runs `EOS_Auth_Login` with `EOS_LCT_ExchangeCode` after sign-in (`eos:auth_login_dispatch`, `credential=exchange_code`). The exchange code is minted with `consumingClientId` = the EOS client id `34a02cf8f4414e29b15921876da36f9a`, see [OAuth/Exchange](../../AccountService/OAuth/Exchange.md). The SDK is configured with a DPoP signer first (`EOS_Auth_ConfigureDpop`, ES256), so requests may carry a `DPoP` proof.

URL: https://api.epicgames.dev/epic/oauth/v2/token \
Method: POST \
Auth Required: Yes (Basic Authentication where the username is the Client Id and the password is the Client Secret)

## Headers
`Content-Type`: application/x-www-form-urlencoded <br/>
`DPoP`: ES256 proof, when configured <br/>

## Body

Inferred from the SDK string table (`epicgames_exchange_code`, `GrantType`, `code_verifier`), not from a trace:

| Field | Value |
|---|---|
| `grant_type` | `exchange_code` |
| `exchange_code` | Minted exchange code |
| `deployment_id` | `83364c64d38841d49c4de2f6f0eb3360` (prod) |

Client id / deployment come from [Clients](../../../Launcher/Auth/Clients.md). Needs a live capture.

Related SDK calls on the same session: [TokenInfo](TokenInfo.md), [Revoke](Revoke.md), [Exchange](Exchange.md), [PublicKeys](PublicKeys.md).
