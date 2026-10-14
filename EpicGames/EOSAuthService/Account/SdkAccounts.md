## EOS Auth Service - Account: Query Accounts

Account lookup used by the EOS SDK's UserInfo client (route `FetchAccountsForSdkv2`; callers are `FUserInfoClient` query tasks such as `QueryUserInfoByDisplayName`). The launcher imports no `EOS_UserInfo_*` function, so it only fires if the SDK's own overlay / party code looks up users (e.g. display names); needs a live capture.

URL: https://api.epicgames.dev/epic/id/v2/sdk/accounts \
Method: GET \
Auth Required: Yes (Bearer Epic account access token, inferred)

## Headers
`X-Epic-Correlation-ID`: random id <br/>

## Query Parameters
`accountId`: Repeatable. Epic account id to look up <br/>
`externalAccountId`: Optional. External account id <br/>
`displayName`: Optional. Exact display name <br/>
`identityProviderId`: Optional, with `externalAccountId`. One of the values below <br/>

| `identityProviderId` |
|---|
| `psn` |
| `xbl` |
| `nintendo` |
| `steam` |

---

_Example Response (shape from client; array wrapper inferred)_

```json
[
  {
    "accountId": "94b1569506b04f9f8557af611e8c5e47",
    "displayName": "DisplayName",
    "preferredLanguage": "en",
    "linkedAccounts": [
      {
        "identityProviderId": "steam",
        "accountId": "76561198000000000",
        "displayName": "SteamName"
      }
    ],
    "email": "...",
    "emailVerified": true,
    "country": "US",
    "dateOfBirth": "...",
    "cabinedMode": false
  }
]
```

Field names are from the SDK deserializers; which ones the service fills for a non-self lookup is not known. Linked account entries also have a `countryCode` field.
