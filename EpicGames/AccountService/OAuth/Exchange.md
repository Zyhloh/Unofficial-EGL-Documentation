## Account Service - OAuth: Generate Exchange Code

Mints a one-time exchange code from the caller's access token. eglv2 calls it from six places:

| Caller | `consumingClientId` | Purpose |
|---|---|---|
| Browser sign-in (`eas_for_eg1`) | set | Trade the EAS token for an EG1 token |
| EOS login (`eos_login_exchange_code`) | EOS client id (`34a02cf8f4414e29b15921876da36f9a`) | `EOS_Auth_Login` with `EOS_LCT_ExchangeCode` |
| Game launch / `prefetch_exchange_code` (`src\auth\exchange_code_cache.rs`) | not determined | `-AUTH_PASSWORD=` of the game, see [Game Launch](../../../Launcher/Flows/GameLaunch.md) |
| Parental consent (`auth_open_parental_consent`) | not determined | [/id/exchange](../../Web/Id/Exchange.md) web SSO |
| Partner hand-off (EA app / Ubisoft Connect) | not determined | Passed to the partner client |
| v1 carry-over (`v1_carryover_exchange_code`) | set | Move the old launcher's session to the SISU client |

When `consumingClientId` is requested and the response omits it or returns a different value, the launcher logs `Exchange code consumingClientId mismatch` / `cannot verify pin` and rejects the code.

URL: https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange \
Method: GET \
Auth Required: Yes (Bearer access token)

## Headers
`Authorization`: Bearer {access_token} <br/>

## Query Parameters
`consumingClientId`: Optional. Client id that is allowed to redeem the code <br/>

---

_Example Response_

```json
{
  "expiresInSeconds": 299,
  "code": "94b1569506b04f9f8557af611e8c5e47",
  "creatingClientId": "34a02cf8f4414e29b15921876da36f9a"
}
```

_Example Response (with `consumingClientId`)_

```json
{
  "expiresInSeconds": 299,
  "code": "94b1569506b04f9f8557af611e8c5e47",
  "creatingClientId": "34a02cf8f4414e29b15921876da36f9a",
  "consumingClientId": "34a02cf8f4414e29b15921876da36f9a"
}
```

The code is valid for 5 minutes and single use. `POST` answers 405 `errors.com.epicgames.common.method_not_allowed`. The launcher deserializes only `code` and `consumingClientId`; 429 is logged as `Exchange code request rate-limited (429)`, an unparseable body maps to `EXCHANGE_CODE_RESPONSE_UNPARSEABLE`.
