## IGDB - Auth: Token

Twitch app token for IGDB (`eglv2_lib::api::igdb::auth`, `ExternalLibrary.IgdbTokenMinted`). Client id / secret come from `EGL_IGDB_CLIENT_ID` / `EGL_IGDB_CLIENT_SECRET`.

URL: https://id.twitch.tv/oauth2/token \
Method: POST \
Auth Required: No

## Body
`client_id`: Twitch client id <br/>
`client_secret`: Twitch client secret <br/>
`grant_type`: `client_credentials` <br/>

---

_Example Response (shape from client, `TokenResponse`)_

```json
{
  "access_token": "...",
  "expires_in": 5184000
}
```
