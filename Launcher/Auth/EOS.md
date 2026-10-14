# EOS Login

The launcher runs the EOS SDK (`EOSSDK-Win64-Shipping.dll`) on a dedicated `eos-worker` thread (`eglv2_lib::eos::manager`, `eglv2_lib::eos::auth_listener`) for the social overlay, party and voice. It signs the SDK in with the same Epic account after every launcher sign-in.

## Platform

`EOS_Platform_Create` with the values in [Clients](Clients.md#eos-platform-config) (`Creating EOS platform step=3/4 product_id= sandbox_id= deployment_id= flags= rtc_enabled=`). `-disable-social-panel` adds `EOS_PF_DISABLE_OVERLAY`.

## Login sequence

1. Launcher session is installed (`AuthEvent::LoggedIn`). An empty access token aborts (`cannot run EOS_Auth_Login`).
2. DPoP: `EOS_Auth_ConfigureDpop` once per session, `algorithm=ES256`, sign callback backed by the launcher key ([DPoP](DPoP.md)).
3. Mint an exchange code with the launcher's EG1 token: `GET /account/api/oauth/exchange?consumingClientId=34a02cf8f4414e29b15921876da36f9a` ([OAuth/Exchange](../../EpicGames/AccountService/OAuth/Exchange.md)). Log: `Minting SISU exchange code for EOS_Auth_Login account_id=... credential=exchange_code consuming_client_id=...`.
4. `EOS_Auth_Login` with `EOS_LCT_ExchangeCode`, the code as `Token`, plus scope flags (`EosManager::auth_login dispatching ... credential=exchange_code exchange_code_len= scopes=`). The SDK redeems it itself, see [EOS Epic Token](../../EpicGames/EOSAuthService/OAuth/EpicToken.md).
5. A `Continuance` result is treated as an error (`UnexpectedContinuance`).
6. Session starters run after login: `sdk_token`, `analytics_bearer`, `connectivity`, `voice_party`, `overlay_registration`, `idle_detector`, `party_leave_analytics` (`src\auth\session_lifetime.rs`).

Network failures are retried with backoff; opening the social panel can nudge a retry (rate limited).

## Token override

The SDK can ask for a fresher token: `EOS_Auth_AddNotifyAccessTokenOverrideRequested`. The launcher answers with `EOS_Auth_SetAccessTokenOverride` using its current EG1 access token (`Re-pushing EG1 access token to SDK (override-requested)`, `EosClient.TokenPush.*`). Both functions are not part of the public EOS SDK headers.

## Sign-out

`EOS_Auth_Logout`, `EOS_Auth_UnconfigureDpop`, notifications cleared (`ClearAuthNotifications`). Stage `overlay_and_sdk` of the sign-out drain.

## Not used

No `EOS_Connect_*` import. The Connect token endpoints in [EOSAuthService](../../EpicGames/EOSAuthService/README.md) are SDK-internal. Epic Connect (the `wss://connect.epicgames.dev` socket) is a separate client started at sign-in (`Epic Connect shared client connect() requested (eager, at sign-in)`), see [Connect](../Social/Connect.md).
