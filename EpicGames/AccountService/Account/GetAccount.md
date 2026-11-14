## Account Service - Account: Get Account

Reads the signed-in account after every token grant (sign-in, restore, refresh gate check) and on `auth_recheck_cabined_mode`. The result feeds [Cabined Mode](../../../Launcher/Auth/CabinedMode.md) and [Quiet Hours](../../../Launcher/Auth/QuietHours.md) (and, up to 0.95, the email gate).

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

The launcher's `AccountApiResponse` (0.115) reads 7 of these: `displayName`, `email`, `country`, `cabinedMode`, `emailVerified`, `age` and `minorStatus`. 0.95 read 5 (no `age` / `minorStatus`). `age` is not in the live response for an adult account; `minorStatus` decides then.

| Missing field | Behaviour |
|---|---|
| `displayName` | `Account API response missing display_name field` |
| `email` | `Account API response missing email field` (0.95: admitted as cabined when `cabinedMode` was true and the email gate off) |
| `cabinedMode` | Treated as cabined (fail-closed), `Auth.AccountInfo.CabinedModeMissing` |
| `age` and `minorStatus` | No usable `age` and `minorStatus` other than `NOT_MINOR`: quiet hours apply (fail-closed), see [Quiet Hours](../../../Launcher/Auth/QuietHours.md) |

401 during the refresh gate check signs the user out. Malformed body fails closed (`Failed to parse account API response`; 0.95 used the `INTERNAL_BETA_RESTRICTED` path). Transport failure keeps the session and re-checks next cycle.
