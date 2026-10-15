## EOS Auth Service - OAuth: Revoke Token (v2)

Ends an EOS Epic account session. The EOS SDK calls it when the session is dropped, e.g. `EOS_Auth_Logout` during launcher sign-out (see [EOS Login](../../../Launcher/Auth/EOS.md#sign-out)); log line `RevokeToken RevokeReason=%s Token=%s`.

URL: https://api.epicgames.dev/epic/oauth/v2/revoke \
Method: POST \
Auth Required: Yes (Basic Authentication where the username is the Client Id and the password is the Client Secret)

## Headers
`Content-Type`: application/x-www-form-urlencoded <br/>

## Body

`token`: The access token to revoke

---

_Example Response_

`204 No Content`. [Token Info](TokenInfo.md) for the same token then returns `{"active": false}`.
