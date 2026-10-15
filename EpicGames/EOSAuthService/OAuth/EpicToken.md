## EOS Auth Service - OAuth: Epic Account Token (v2)

Signs an Epic account in to EOS. The launcher's EOS SDK calls it after sign-in (`EOS_Auth_Login` with an exchange code minted for the EOS client), see [OAuth/Exchange](../../AccountService/OAuth/Exchange.md). The SDK may add a `DPoP` proof (it is configured with an ES256 signer).

URL: https://api.epicgames.dev/epic/oauth/v2/token \
Method: POST \
Auth Required: Yes (Basic Authentication where the username is the Client Id and the password is the Client Secret)

## Headers
`Content-Type`: application/x-www-form-urlencoded <br/>

## Body

`grant_type`: `exchange_code` (also `refresh_token`) <br/>
`exchange_code`: Exchange code from an Epic account session <br/>
`deployment_id`: EOS deployment, `83364c64d38841d49c4de2f6f0eb3360` for the launcher <br/>
`scope`: Space separated scopes, e.g. `basic_profile friends_list presence`

Client: the launcher's `34a02cf8f4414e29b15921876da36f9a` / `daafbccc737745039dffe53d94fc76cf` (see [Clients](../../../Launcher/Auth/Clients.md)).

---

_Example Response_

```json
{
  "scope": "basic_profile friends_list country presence",
  "token_type": "bearer",
  "access_token": "eyJ0IjoiZXBpY19pZCIs...",
  "refresh_token": "eyJ0IjoiZXBpY19pZF9y...",
  "expires_in": 129600,
  "expires_at": "2026-10-17T00:33:23.211Z",
  "refresh_expires_in": 31540000,
  "refresh_expires_at": "2027-10-15T13:40:03.212Z",
  "account_id": "94b1569506b04f9f8557af611e8c5e47",
  "client_id": "34a02cf8f4414e29b15921876da36f9a",
  "application_id": "fghi4567KEIkE93BQjKGjnyql0oI6X1a",
  "merged_accounts": [],
  "acr": "AAL1",
  "auth_time": "2026-10-15T12:33:23.205Z"
}
```

The access token is a JWT valid for 36 hours, the refresh token for a year. `country` is granted without being requested. This user token is accepted by the `api.epicgames.dev/epic/...` services (party, presence, chat); the [Product Config](../../EOSSDKConfigService/Config/ProductConfig.md) refuses it.

Related: [Token Info](TokenInfo.md), [Revoke](Revoke.md), client token [Token (v1)](Token.md).
