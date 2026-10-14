## EOS Auth Service - OAuth: Revoke Token (v2)

Called by the EOS SDK (`RevokeTokenTask`, route `TokenRevokev2`) when it drops an Epic account session, e.g. on `EOS_Auth_Logout` during launcher sign-out (`overlay_and_sdk` drain stage, see [EOS Login](../../../Launcher/Auth/EOS.md#sign-out)). Log: `RevokeToken RevokeReason=%s Token=%s`. A revoke behavior can suppress it (`RevokeToken requested but disabled by behavior`).

URL: https://api.epicgames.dev/epic/oauth/v2/revoke \
Method: POST \
Auth Required: Yes (set by the SDK task; type not resolved statically)

## Headers
`Content-Type`: application/x-www-form-urlencoded <br/>
`X-Epic-Correlation-ID`: random id <br/>
`X-Epic-Login-ID`: SDK login id, when set <br/>

## Query Parameters
`intent`: Revoke intent, mapped from the SDK revoke reason <br/>

| `intent` |
|---|
| `LOG_OUT_SINGLE` |
| `LOG_OUT_BATCH` |
| `LOG_OUT_CREDENTIALS_CHANGE` |
| `LOG_OUT_INACTIVE` |
| `LOG_OUT_ON_SHUTDOWN` |
| `LOG_OUT_ON_ERROR` |
| `LOG_OUT_ILLEGAL_STATE` |
| `SINGLE_SESSION_ENFORCEMENT` |
| `LOG_OUT_CONFIRM_IDENTITY` |
| `REFRESH_SESSION_LIMIT_ENFORCEMENT` |
| `DATA_CONSENT_REVOKED` |
| `LOG_OUT_POLICY_ENFORCEMENT` |
| `LOG_OUT_POLICY_CHANGE` |
| `LOG_OUT_POLICY_DATA_CHANGE` |
| `LOG_OUT_TIME_CONTROL_POLICY` |
| `ADMIN_REMOVED_SINGLE` |
| `ADMIN_REMOVED_BATCH` |
| `ADMIN_REMOVED_CLIENT_SESSIONS` |
| `LOG_OUT_FOR_DATA_COLLECTION` |
| `NOT_SET` |

SDK revoke reasons: `Logout`, `DeletePersistentAuth`, `LoginFailed`, `Shutdown`, `RefreshFailed`, `Expired`, `VerifyFailed`, `OldReplacedWithNew`, `OperationFailed`. A reason without a mapping falls back to unknown (`ToRevokeIntent failed because the revoke reason is not mapped to a revoke intent`). Which intent `Logout` maps to needs a live capture.

## Body

| Field | Value |
|---|---|
| `token` | The token to revoke |
| `token_type_hint` | Token type hint |

---

No response fields are deserialized.
