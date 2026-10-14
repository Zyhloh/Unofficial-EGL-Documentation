## EOS Auth Service - OAuth: Generate Exchange Code (v2)

Called by the EOS SDK (route `GetExchangeCodev2`) from its UI / social overlay code to mint a one-time code for the social overlay web app. The SDK config carries `UIClient.SocialSPAClientId` = `cf27c69fe66441e8a8a4e8faf396ee4c` and `FriendsURLExchangeCodeSuffix` = `` ?exchange_code=`exchange_code ``; the overlay reads `exchange_code` from its URL ([Social Overview](../../../Launcher/Social/Overview.md)). That the code is minted for that client id is inferred from the config, not traced.

URL: https://api.epicgames.dev/epic/oauth/v2/exchange \
Method: GET \
Auth Required: Yes (Bearer Epic account access token, inferred)

## Headers
`X-Epic-Correlation-ID`: random id <br/>
`X-Epic-Login-ID`: SDK login id, when set <br/>

## Query Parameters
`consumingClientId`: Optional. Client id allowed to redeem the code <br/>
`codeChallenge`: Optional. PKCE challenge <br/>
`codeChallengeMethod`: Optional. PKCE challenge method <br/>

---

_Example Response (shape from client)_

```json
{
  "code": "94b1569506b04f9f8557af611e8c5e47",
  "expiresInSeconds": 300,
  "creatingClientId": "34a02cf8f4414e29b15921876da36f9a",
  "consumingClientId": "cf27c69fe66441e8a8a4e8faf396ee4c"
}
```
