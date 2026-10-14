## Account Service - Account: Get Account

Reads the signed-in account after every token grant (sign-in, restore, refresh gate check) and on `auth_recheck_cabined_mode`. The result feeds the email gate and [Cabined Mode](../../../Launcher/Auth/CabinedMode.md).

URL: https://account-public-service-prod03.ol.epicgames.com/account/api/public/account/:accountId \
Method: GET \
Auth Required: Yes (Bearer access token)

## Headers
`Authorization`: Bearer {access_token} <br/>

## Path Parameters
`accountId`: The account id

---

_Example Response (shape from client, `struct AccountApiResponse with 5 elements`)_

```json
{
  "displayName": "Player",
  "email": "player@example.com",
  "emailVerified": true,
  "cabinedMode": false
}
```

`displayName`, `email`, `cabinedMode` and `emailVerified` are read. The struct has a fifth field whose name is shared with another struct in the string table and is not resolved (the cached account info stores `country`, so it is probably `country`).

| Missing field | Behaviour |
|---|---|
| `displayName` | `Account API response missing display_name field` |
| `email` | Admitted as cabined when `cabinedMode` is true and the email gate is off, denied when the gate is on |
| `cabinedMode` | Treated as cabined (fail-closed), `Auth.AccountInfo.CabinedModeMissing` |

401 during the refresh gate check signs the user out. Malformed body fails closed (`INTERNAL_BETA_RESTRICTED` path). Transport failure keeps the session and re-checks next cycle.
