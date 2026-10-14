## Partner Integration Service - Uplay: Get Account Codes

Reads the Ubisoft Connect code state of an Epic account (titles bought on Epic that activate on Ubisoft Connect). Used by `get_partner_titles`, `redeem_partner_codes` and the partner title state machine (`eglv2_lib::api::partner_integration`, cached by `src\partner\redemption_cache.rs`).

URL: https://partnerintegration-public-service-prod.ol.epicgames.com/partnerintegration/api/uplay/account/:accountId \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`accountId`: The account id

---

The client parses an array of `UplayCode` (log `... (starts as array: ...)`). Recovered fields: `gameId`, `uplayAccountId`, `redeemedOnUplay`; the struct has a fourth field holding the code itself (its Debug output prints `<redacted>`, the JSON name was not recovered).

_Example Response (shape from client)_

```json
[
  {
    "gameId": "94b1569506b04f9f8557af611e8c5e47",
    "uplayAccountId": "94b1569506b04f9f8557af611e8c5e47",
    "redeemedOnUplay": false
  }
]
```

`errors.com.epicgames.partnerintegration.account_not_found` is treated as "no linked Ubisoft account".
