## Account Service - Account: Get External Auths

`eglv2_lib::api::external_auths`. Fetches the account's linked platforms before a partner (EA app / Ubisoft Connect) hand-off, and for the Store bridge's `externalauthtypes`. Cached in `eglv2_lib::auth::account_links_cache` and invalidated after an account-link return.

URL: https://account-public-service-prod03.ol.epicgames.com/account/api/public/account/:accountId/externalAuths \
Method: GET \
Auth Required: Yes (Bearer access token)

## Headers
`Authorization`: Bearer {access_token} <br/>

## Path Parameters
`accountId`: The account id

---

_Example Response (shape from client; only `type` and `externalAuthId` are read)_

```json
[
  {
    "type": "uplay",
    "externalAuthId": "94b1569506b04f9f8557af611e8c5e47"
  }
]
```

Partner code compares `type` against `epic2ea`, `link2ea` (EA app) and `uplay` (Ubisoft Connect); inferred from the string run next to the provider names. A non-success status leaves the link state `unknown`, which permits the hand-off (`REQ-PARTNER-133`).
