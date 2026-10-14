# v1 Sign-in Carry-over

On first run eglv2 tries to reuse the old Epic Games Launcher's remembered login so the user is not asked to sign in again (`src\v1_migration\signin.rs`, `src\commands\v1_migration.rs`, telemetry `V1Migration.SignInCarryoverFailed`).

## Source

The old launcher's `GameUserSettings.ini`, section `[RememberMe]`, keys `Enable` and `Data` (`RememberMeEnableData`). `Data` is base64 (alphabet table next to the parser) of a JSON `RememberMeRecord` with `Region`, `Token`, `DisplayName`. `Token` is the v1 refresh token issued to `launcherAppClient2`.

## Chain

1. Skip if a session already exists (`alreadySignedIn`) or session restore is still running.
2. `POST /account/api/oauth/token` with `34a02cf8f4414e29b15921876da36f9a`: `grant_type=refresh_token`, `refresh_token=<v1 token>`, `token_type=eg1` (label `refresh_token_v1_carryover`, `Exchanging v1's remembered refresh token to open the carry-over chain`).
3. `GET /account/api/oauth/exchange` with that token (label `v1_carryover_exchange_code`; `v1 carry-over: failed to mint SISU exchange code` on failure), so the code is for the SISU client.
4. `POST /account/api/oauth/token` with `egs-desktop`: `grant_type=exchange_code` (`Exchanging Epic exchange_code for tokens`).
5. The account id from step 2 must match the redeemed one (`v1 carry-over account mismatch: v1 ... vs redeemed ...`).
6. The new session is installed like a normal sign-in.

Outcomes (`V1CarryoverOutcome`): `migrated`, `noRememberedSignIn`, `alreadySignedIn`, `failed`. Telemetry detail: `already_signed_in`, `no_remembered_sign_in`, `unreadable`, `restore_pending`, `exchange_failed`, `finalize_failed`. On failure the user sees the normal sign-in screen (`exchange chain failed, falling back to sign-in`).

The client used in step 4 is inferred from the SISU wording of step 3; the binary does not log it.
