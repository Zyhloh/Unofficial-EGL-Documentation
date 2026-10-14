## Epic Games Id - Link

Partner account-linking page used by `open_partner_account_link` (`REQ-PARTNER-135`) before an EA app / Ubisoft Connect hand-off. The launcher opens it in the system browser and waits on its own loopback listener for the return.

URL: https://www.epicgames.com/id/link/:provider \
Method: GET (browser navigation) \
Auth Required: No (browser session)

## Path Parameters
`provider`: Partner slug, value not resolved from the binary

## Query Parameters
`redirect_uri`: `http://127.0.0.1:<port>/launcher/account-linked` <br/>
`state`: Optional, appended when the launcher has one for this press <br/>

The URL is built as `{base}/{provider}?redirect_uri={uri}[&state={state}]` (`sub_140E16D80`). That `{base}` is the `/id/link` entry of the environment table is inferred: `/id/link` has no other consumer and the partner module is the only code that builds a `?redirect_uri=` URL of this shape.

On return the launcher emits `PartnerAccountLinkCompletedEvent` (`Library.Partner.AccountLinkCompleted` in the frontend), invalidates the account-links cache and re-reads [ExternalAuths](../../AccountService/Account/ExternalAuths.md). A second press supersedes the first (`Partner.AccountLinkSuperseded`); a timeout logs `Partner.AccountLinkReturnTimedOut`.
