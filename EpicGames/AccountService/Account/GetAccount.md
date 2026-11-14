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

_Example Response (own account)_

```json
{
  "id": "94b1569506b04f9f8557af611e8c5e47",
  "displayName": "Player",
  "name": "First",
  "lastName": "Last",
  "email": "player@example.com",
  "failedLoginAttempts": 0,
  "lastLogin": "2026-11-07T19:41:27.217Z",
  "numberOfDisplayNameChanges": 3,
  "ageGroup": "UNKNOWN",
  "headless": false,
  "country": "US",
  "countryUpdatedTime": "2026-01-01T00:00:00.000Z",
  "preferredLanguage": "en",
  "lastDisplayNameChange": "2026-01-01T00:00:00.000Z",
  "canUpdateDisplayName": false,
  "canUpdateDisplayNameNext": "2026-12-01T00:00:00.000Z",
  "tfaEnabled": true,
  "emailVerified": true,
  "minorVerified": false,
  "minorExpected": false,
  "minorStatus": "NOT_MINOR",
  "siweNotificationEnabled": true,
  "accountLinkingControlsAvailable": true,
  "accountLinkingControlsEnforced": false,
  "accountLinkingControlsSelfApprover": true,
  "cabinedMode": false,
  "hasHashedEmail": false,
  "lastReviewedSecuritySettings": "2026-01-01T00:00:00.000Z",
  "lastDeclinedMFASetup": "2026-01-01T00:00:00.000Z",
  "lastReviewedLinkConsole": "2026-01-01T00:00:00.000Z"
}
```

The launcher's `AccountApiResponse` reads 5 of these: `displayName`, `email`, `emailVerified`, `cabinedMode` and (almost certainly) `country`, which the cached account info stores and the response carries.

| Missing field | Behaviour |
|---|---|
| `displayName` | `Account API response missing display_name field` |
| `email` | Admitted as cabined when `cabinedMode` is true and the email gate is off, denied when the gate is on |
| `cabinedMode` | Treated as cabined (fail-closed), `Auth.AccountInfo.CabinedModeMissing` |

401 during the refresh gate check signs the user out. Malformed body fails closed (`INTERNAL_BETA_RESTRICTED` path). Transport failure keeps the session and re-checks next cycle.
