# Voice - Native Bridge

How voice traffic crosses from the social overlay page into the EOS SDK inside `EpicGamesLauncher.exe`. The general bridge (`window.ue.*`, `social_bridge_*` commands, unified vs legacy mode, notification channel) is in [Social Bridge](../Social/Bridge.md); this page covers the voice-specific parts and the SDK transport on Windows.

## Transport (Windows)

eglv2 creates the EOS platform with the external-overlay mode (`EOS_PF_EXTERNAL_OVERLAY` string, `EOS_Platform_GetExternalOverlayInterface`). The SDK owns the overlay logic but has no browser; the launcher's WebView2 is the browser:

| SDK callback / call | Launcher side (`eglv2_lib::social::*`) |
| --- | --- |
| `EOS_ExternalOverlay_AddNotifyLoadUrlRequested` | `external_overlay::start_load`: the SDK announces the overlay URL (`StartLoadURL`) |
| `EOS_ExternalOverlay_AddNotifyRegisterJSBindingsRequested` | `external_overlay::bindings`: SDK script sources (`EOSOverlayCommonJS`) injected into the `social` webview; binding set cached in `social-overlay-bindings.json` |
| `EOS_ExternalOverlay_AddNotifyEvaluateJSRequested` / `EOS_ExternalOverlay_ReportEvaluateJSResult` | `windows::js_forward`: runs SDK-supplied JS in the page and returns the value |
| page -> SDK function call | `windows::bridge_reply`: WebView2 `AddHostObjectToScript` exposes host object `eosBridge`; each call is forwarded with `EOS_ExternalOverlay_ReportJSFunctionInvoked` |
| `EOS_ExternalOverlay_AddNotifyResolveJSCallbackRequested` | `bridge_reply` settles the page promise for that `callback_id` |
| `EOS_ExternalOverlay_ReportBrowserStatus` | `external_overlay::status`: `Ready`, `BeginLoad`, `EndLoad`, `LoadError`, `Closed`, `Crashed` |

The SDK script merges `getNextChanges`, `getNextNotifications`, `getFeatures`, `sendIntent`, `getVersion`, `getCodeVerifier`, `verifyIntent`, `sanitizeStrings` onto `window.ue.social`. Their presence plus `window.social.broker` puts the app in unified mode, so every voice intent below reaches the SDK through `sendIntent` -> `eosBridge` -> `ReportJSFunctionInvoked`, and every SDK voice state comes back through `getNextChanges`. Which JS function name the SDK script calls on `eosBridge` is not in the launcher binary (it is SDK-supplied script text); needs a capture of the evaluated script.

## SDK login

Before the overlay can do anything the launcher signs the SDK in (`eglv2_lib::eos`, logs `EosClient.Login.*`):

1. Mint an exchange code from the launcher's EG1 session (`EosClient.Login.ExchangeCodeMinting`).
2. `EOS_Auth_Login` with credential type ExchangeCode (`EOS_Auth_Login(ExchangeCode) failed` / `returned Continuance`), retried with backoff (`EosClient.Login.RetryScheduled`).
3. `EOS_Auth_AddNotifyAccessTokenOverrideRequested`: when the SDK asks, the launcher pushes the EG1 access token with `EOS_Auth_SetAccessTokenOverride` ("Re-pushing EG1 access token to SDK (override-requested)"). DPoP is configured with `EOS_Auth_ConfigureDpop`.
4. Registers `EOS_UI_AddNotifyNotificationReceived`, `EOS_UI_AddNotifyBadgeCountUpdated`, `EOS_UI_AddNotifyDisplaySettingsUpdated`, `EOS_UI_AddNotifyAudioChimeRequested`, `EOS_PartyFeature_AddNotifyLeaveAnalytics`.

Product / sandbox / deployment ids come from `EGL_EOS_PRODUCT_ID`, `EGL_EOS_SANDBOX_ID`, `EGL_EOS_DEPLOYMENT_ID`, `EGL_EOS_CLIENT_ID`, `EGL_EOS_CLIENT_SECRET`, `EGL_EOS_ENCRYPTION_KEY`, `EGL_EOS_BACKEND_ENVIRONMENT` overrides, else built-in defaults (`GameDev` / `Production`); the default values were not located in the string table.

The launcher never calls `EOS_RTC_*` / `EOS_RTCAudio_*` itself. Voice runs entirely inside the SDK's internal party feature (`PartyFeatureClient`, `LogEOSRTCParties`), driven by overlay intents.

## Page -> SDK (feature `party`)

| Intent | Payload | SDK handler |
| --- | --- | --- |
| `connect-voice-room` | `{ participantToken, roomName, clientBaseUrl, roomSettings: { AudioInputDeviceMode: "AlwaysOn" } }` | `HandleConnectVoiceRoomIntent` (`roomSettings` -> `IntentRtcRoomSettings`, may be overridden by ini `RoomSettings.*`) |
| `update-session-info` | `{ participantToken, roomName, clientBaseUrl, requestUniqueIndex }` | `HandleUpdateSessionInfoIntent` (answer to `request-session-info`) |
| `disconnect-voice-room` | `{}` | `HandleDisconnectVoiceRoomIntent` |
| `set-blocked-participants` | `{ participants: [{ id }] }` | `HandleSetBlockedParticipantsIntent`; sent before connect and again whenever the blocked set changes while connected |
| `update-voice-settings` | any of `inputDevice`, `outputDevice`, `inputVolume`, `outputVolume`, `inputMuted`, `audioEnabled`, `pttEnabled`, `pushToTalkInputKeys` (the SDK also reads `aecMode`, not sent by this overlay build) | `HandleUpdateVoiceSettingsIntent` |
| `set-participant-audio` | `{ id, volume }` (0-100, from `userVolume * 100`) or `{ id, muted }` | `HandleSetParticipantAudioIntent` |
| `start-voice-recording` / `pause-voice-recording` | `{}` | voice moderation record resume / suspend |
| `query-recorded-participants` | `{}` | fills `voice-report` |
| `submit-voice-report` | `{}` | uploads the recording, see [Reporting](Moderation.md) |

Push-to-talk binding is registered separately: `{ feature: "application", name: "configure-bindings", payload: { bindings: [{ name: "push-to-talk", keys: ["Control", "V"], isGlobal: true }] } }` (keys mapped to SDK names: `Shift`, `Control`, `Alt`, `AltGr`, `Meta`, `Space`, ...).

## SDK -> page (`getNextChanges` values)

| Name | Shape | Used for |
| --- | --- | --- |
| `voice-room` | `{ participants: [{ id, muted, speaking, notListening, voiceChatOff }], pttActive, status }` | speaking rings, mute / deafen icons, connection status (`connecting`, `connected`, `error`) |
| `request-session-info` | `{ roomName, requestUniqueIndex }` | triggers a new [conferences/connection](../../EpicGames/PartyService/Conferences/ConnectVoiceRoom.md) call |
| `voice-settings` | `{ inputMuted, audioEnabled }` | SDK-side mute / deafen echo |
| `input-device` / `output-device` | `{ currentDevice, preferredDeviceId, options }` | device pickers |
| `bindings` (collection) | `push-to-talk` `{ isActivated }` | PTT pressed -> `update-voice-settings { inputMuted: false, audioEnabled: true }`, released -> `{ inputMuted: true }` |
| `voice-moderation` | `{ recording, reportStatus, reportUploadProgress, emeraldReportToken, localUserId }` | report dialog |
| `voice-report` | `{ recordId, participants: [{ userId, displayName }], status }` | report dialog |
| `voice-terms-acceptance` | `{ status }` (`shouldPrompt`, `accepted`, `declined`, `failed`) | voice terms modal |
| `current-active-device` | `{ platformName, productName, epicConnectId, isDisconnected }` | which device of the account owns voice |

Chimes: the page sends `{ feature: "chimes", name: "play-chime", payload: { intent: { feature: "party", name, payload } } }` with `name` in `party-local-user-joined`, `party-local-user-left`, `party-local-user-switched`, `party-users-joined`, `party-users-left`, `party-joinability-changed`, `message-received`, `party-voice-mute-changed` (`{ isMuted }`). The SDK turns these into `EOS_UI_AddNotifyAudioChimeRequested` (types `PartyUserJoined`, `PartyUserLeft`, `PushToTalkActivated`, `PushToTalkDeactivated`, `VoiceMuted`, `VoiceUnmuted`, `PartyJoinabilityChanged`, `PartyMessageReceived`) and the launcher plays the sound (`eglv2_lib::social::chime`, debounced).

## Page -> launcher (notification channel)

Handled by Rust `src\social\handlers\social.rs` (names from its unhandled-name log):

| name | payload | Launcher action |
| --- | --- | --- |
| `voice-party-state-changed` | `{ state }` | tray icon + taskbar badge, see [Settings](Settings.md#tray-and-taskbar) |
| `set-local-voice-setting` | `{ configName, configValue }` | `VoiceSettingsStore` -> `voice-settings.json` |
| `get-local-voice-setting` | `{ configName }` | answers `get-local-voice-setting-response` `{ configValue }` |
| `mic-permission-changed-subscribe` / `-unsubscribe` | | pushes `mic-permission-changed` `{ isAllowed }` |
