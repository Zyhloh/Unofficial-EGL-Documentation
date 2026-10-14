## EULA Tracking Service - Agreements: Accept Agreement

Records acceptance of one agreement version. Sent by `accept_eula` (`{ promptId }`) after the user agrees in the EULA modal, and by `acquire_engine_entitlement` / `acquire_tool_entitlement` (log `Accepting engine EULA agreement agreement_key=... version=...`).

URL: https://eulatracking-public-service-prod06.ol.epicgames.com/eulatracking/api/public/agreements/:key/version/:version/account/:accountId/accept \
Method: POST \
Auth Required: Yes (Bearer access token)

## Path Parameters
`key`: Agreement key from [Get Agreement](GetAgreement.md) <br/>
`version`: Agreement version from [Get Agreement](GetAgreement.md) <br/>
`accountId`: The account id

## Query Parameters
`locale`: Locale of the accepted text, e.g. `en` <br/>

The method is inferred (same path shape as the UE launcher's accept call); the binary only shows the path segments and the `locale` pair.
