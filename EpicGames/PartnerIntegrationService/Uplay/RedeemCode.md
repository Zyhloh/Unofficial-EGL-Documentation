## Partner Integration Service - Uplay: Redeem Code

Redeems the Ubisoft code of one game on the linked Ubisoft account. `redeem` step of `redeem_partner_codes` (`{ appId }`).

URL: https://partnerintegration-public-service-prod.ol.epicgames.com/partnerintegration/api/uplay/account/:accountId \
Method: POST \
Auth Required: Yes (Bearer access token)

## Path Parameters
`accountId`: The account id

## Query Parameters
`uplayAccountId`: Linked Ubisoft account id <br/>
`gameId`: Game id from [Get Account Codes](GetAccountCodes.md) <br/>

The method is inferred; the request builder only shows path and query.
