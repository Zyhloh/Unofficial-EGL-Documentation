## Epic Games Id - Register

Account creation entry of the same PKCE flow. Opened when the login screen calls `auth_sign_in_browser` with `createAccount: true` (`create-account` button). Same query string as [Authorize](Authorize.md) without `prompt`; the code still returns to the loopback listener and is redeemed the same way.

URL: https://www.epicgames.com/id/register \
Method: GET (browser navigation) \
Auth Required: No

## Query Parameters
`client_id`: `c85f4c6238b04d3399bc0080e83b83fc` <br/>
`response_type`: `code` <br/>
`redirect_uri`: `http://127.0.0.1:<port>/launcher/authorized` <br/>
`scope`: `basic_profile friends_list country presence` <br/>
`code_challenge`: PKCE S256 challenge <br/>
`code_challenge_method`: `S256` <br/>
`state`: Per-attempt value <br/>
`lang`: UI language <br/>

The choice between `/id/authorize` + `prompt=select_account` and `/id/register` is a single branch on the `createAccount` flag in the sign-in task (`sub_1400DC690`); the register mapping is inferred from the endpoint struct layout (`authorize` at +0xA8, `register` at +0xC0).
