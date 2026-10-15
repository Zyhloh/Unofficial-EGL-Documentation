## Partner Integration Service - Uplay: Get Account Codes

Reads the Ubisoft Connect code state of an Epic account (titles bought on Epic that activate on Ubisoft Connect). Used by `get_partner_titles`, `redeem_partner_codes` and the partner title state machine (`eglv2_lib::api::partner_integration`, cached by `src\partner\redemption_cache.rs`).

URL: https://partnerintegration-public-service-prod.ol.epicgames.com/partnerintegration/api/uplay/account/:accountId \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`accountId`: The account id

---

_Example Response (shortened, 1 of 8 entries)_

```json
[
  {
    "created": "2019-11-08T17:51:40.085Z",
    "updated": "2019-12-25T16:41:56.007Z",
    "rvn": 3,
    "epicEntitlement": {
      "catalogItemId": "6f6332902ef14c0b81fe96c480b4bd5a",
      "entitlementId": "514a6fbf237c4f0185c7890b64968f2d"
    },
    "gameId": "f667bb94543e43eb87ca008f497df782",
    "epicAccountId": "94b1569506b04f9f8557af611e8c5e47",
    "uplayAccountId": "00000000-0000-0000-0000-000000000000",
    "redeemedOnUplay": true,
    "redemptionTimestamp": "2019-12-25T16:41:56.007Z",
    "assignmentTimestamp": "2019-12-25T16:41:54.559Z",
    "regionCode": "WW",
    "refunded": false,
    "id": "18868e0d78bb4af5a2ebf9a0f9dcb882"
  }
]
```

One entry per Ubisoft title bought on Epic. `gameId` is the catalog `partnerLinkId` of the title (Rayman Legends `f667bb94543e43eb87ca008f497df782`), `uplayAccountId` the linked Ubisoft account. The activation key itself is not in this list.

`errors.com.epicgames.partnerintegration.account_not_found` is treated as "no linked Ubisoft account".
