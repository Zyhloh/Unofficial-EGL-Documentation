## KWS - Settings: Update User

Reports the account's time zone. Launcher 0.115 sends it at every sign-in and session restore with the OS time zone (`Account.TimezoneReportStarted` / `Account.TimezoneReported`). If the account is not known to K3S yet (`account_not_found`) it retries later; a time zone that is not an IANA name is not sent.

URL: https://api.kws.ol.epicgames.com/v1/epic-settings/public/users/:accountId \
Method: PATCH \
Auth Required: Yes (Bearer EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Correlation-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: Your account id

## Body
```json
{
  "clientTimeZone": "America/New_York"
}
```

`clientTimeZone`: IANA time zone name

---

_Example Response_

```json
{
  "response": {
    "userId": "94b1569506b04f9f8557af611e8c5e47",
    "clientTimeZone": "America/New_York"
  },
  "meta": {
    "requestId": "8283e81f-6175-4706-aa82-d6c93ee79a7c",
    "timestamp": "2026-11-14T03:01:00.268Z"
  }
}
```

Gamedev host: `epic-settings-gamedev-api.kws.ol.epicgames.com`.
