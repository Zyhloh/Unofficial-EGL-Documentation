## Epic Games Id - Exchange (web SSO)

Signs the system browser in with an exchange code, then redirects. eglv2 uses it for `auth_open_parental_consent` so the parental controls page opens already signed in (`SSO exchange URL is unparseable` / `Parental-consent URL is unparseable` on failure).

URL: https://www.epicgames.com/id/exchange \
Method: GET (browser navigation) \
Auth Required: No (the exchange code is the credential)

## Query Parameters
`exchangeCode`: Code from [OAuth/Exchange](../../AccountService/OAuth/Exchange.md) <br/>
`redirectUrl`: Target page, for parental consent `https://www.epicgames.com/account/parental-controls?lang=<lang>` <br/>

```
https://www.epicgames.com/id/exchange?exchangeCode=<code>&redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Faccount%2Fparental-controls%3Flang%3Den
```

If there is no access token or minting fails (`Auth.ParentalConsentNoToken`, `Auth.ParentalConsentCodeFailed`) the launcher opens `https://www.epicgames.com/account/parental-controls?lang=<lang>` directly, signed out. The final URL must pass a safety check before it is opened (`Parental-consent URL failed safety check`).
