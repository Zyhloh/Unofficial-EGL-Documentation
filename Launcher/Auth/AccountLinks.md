# Account Links

`open_account_link { link }` opens a fixed web page in the system browser. No exchange code / SSO is attached, the browser's own session applies. The URL must pass a safety check (`Account link URL failed safety check`). `lang` is the launcher UI language.

| `link` | URL |
|---|---|
| `account_settings` | `https://www.epicgames.com/account/personal?lang=<lang>` |
| `epic_rewards` | `https://www.epicgames.com/account/rewards?lang=<lang>` |
| `account_balance` | `https://www.epicgames.com/account/payments?lang=<lang>` |
| `fortnite_gift_card` | `https://www.epicgames.com/redeem?lang=<lang>` |
| `coupons` | `https://store.epicgames.com/inventory/coupons?lang=<lang>` |
| `terms_of_service` | `https://www.epicgames.com/site/<lang>/tos` |
| `privacy_policy` | `https://www.epicgames.com/site/<lang>/privacypolicy` |
| `store_refund_policy` | `https://www.epicgames.com/site/<lang>/store-refund-policy` |
| `publisher_index` | `https://store.epicgames.com/<lang>/publisher-index` |

Mapping is the enum order (`account_settings`, `epic_rewards`, `account_balance`, `fortnite_gift_card`, `coupons`, `terms_of_service`, `privacy_policy`, `store_refund_policy`, `publisher_index`) against the URL table in `sub_140E0B4C0`.

Partner (EA app / Ubisoft Connect) linking is separate: `open_partner_account_link`, see [Id/Link](../../EpicGames/Web/Id/Link.md).
