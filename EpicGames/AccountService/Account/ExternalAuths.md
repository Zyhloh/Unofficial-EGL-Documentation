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

_Example Response (shortened)_

```json
[
  {
    "accountId": "94b1569506b04f9f8557af611e8c5e47",
    "type": "steam",
    "externalAuthId": "76561190000000000",
    "externalAuthIdType": "steam_id64",
    "authIds": [
      {
        "id": "76561190000000000",
        "type": "steam_id64"
      }
    ],
    "dateAdded": "2026-01-01T00:00:00.000Z"
  }
]
```

One entry per linked account. `type` / `externalAuthIdType` pairs seen live: `xbl` / `xuid`, `psn` / `psn_user_id`, `nintendo` / `nsa_id`, `steam` / `steam_id64`, `google` / `google_user_id`, `github` / `github_login`, `twitch` / `twitch_name`, `disney` / `disney_id`, `lego` / `lego_id`. The launcher reads only `type` and `externalAuthId`. Partner code compares `type` against `epic2ea`, `link2ea` (EA app) and `uplay` (Ubisoft Connect); those three values come from the binary (no such link on the test account). A non-success status leaves the link state `unknown`, which permits the hand-off (`REQ-PARTNER-133`).
