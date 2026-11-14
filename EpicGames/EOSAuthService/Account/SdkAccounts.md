## EOS Auth Service - Account: Query Accounts

Account lookup used by the EOS SDK's UserInfo client (route `FetchAccountsForSdkv2`; callers are `FUserInfoClient` query tasks such as `QueryUserInfoByDisplayName`). The launcher imports no `EOS_UserInfo_*` function, so it only fires if the SDK's own overlay / party code looks up users (e.g. display names); needs a live capture.

URL: https://api.epicgames.dev/epic/id/v2/sdk/accounts \
Method: GET \
Auth Required: Yes (Bearer EOS token from [Epic Account Token](../OAuth/EpicToken.md); an EG1 account-service token gets 401 `errors.com.epicgames.unauthorized`)

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

_Example Response (own account by `accountId`)_

```json
[
  {
    "accountId": "94b1569506b04f9f8557af611e8c5e47",
    "displayName": "DisplayName",
    "preferredLanguage": "en",
    "linkedAccounts": [
      {
        "identityProviderId": "nintendo",
        "accountId": "0123456789abcdef",
        "externalAuthEnv": "lp1"
      },
      {
        "identityProviderId": "psn",
        "accountId": "0000000000000000000"
      }
    ],
    "country": "US",
    "cabinedMode": false
  }
]
```

An array. For your own account the live response had no `email`, `emailVerified` or `dateOfBirth` (the SDK deserializer knows those fields too). Linked account entries vary by provider: `identityProviderId` always, plus some of `accountId`, `displayName`, `countryCode` and `externalAuthEnv` (`externalAuthEnv` on the Nintendo link; one entry had `displayName` and `countryCode` but no `accountId`).
