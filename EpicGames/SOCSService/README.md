# Hosts

This are some (not all) Hosts that you can access the SOCS Service from

- api.epicgames.dev (`/epic/socs`)

<br/>

Recommended Hosts:

- api.epicgames.dev

Per-user social overlay settings (voice devices, voice mode, push-to-talk key, chimes, disclosures). Base URL `EPIC_SOCS_ENDPOINT_URL` is hardcoded in the social overlay; client name `socs-service`. Plain EG1 bearer token from any client. Device settings default to an empty string.

| Method | Path | Page |
| --- | --- | --- |
| POST | `/v1/users/:accountId/settings/query` | [Query User Settings](Settings/QueryUserSettings.md) |
| PUT | `/v1/users/:accountId/settings/:settingId` | [Update User Setting](Settings/UpdateUserSetting.md) |

## Setting ids used by the overlay

| Setting id | Scoped | Value | Overlay intent |
| --- | --- | --- | --- |
| `v1VoiceInputDevice` | yes | device id (Windows: bare `{guid}` part, see below) | `update-voice-input-device-setting` |
| `v1VoiceOutputDevice` | yes | device id | `update-voice-output-device-setting` |
| `v1VoiceInputVolume` | yes | number as string (`0`-`100`, server default `50`; client fallback `60`) | `update-voice-input-volume-setting` |
| `v1VoiceOutputVolume` | yes | number as string (server default `50`) | `update-voice-output-volume-setting` |
| `v1VoiceChatMode` | yes | `openMic` (default) / `pushToTalk` | `update-voice-chat-mode-setting` |
| `v1VoicePushToTalkKeybinding` | yes | keys joined with `+` (e.g. `CONTROL+V`) | `update-voice-ptt-binding-setting` |
| `v1PartyJoinedChimeEnabled`, `v1PartyLeftChimeEnabled`, `v1MutedChimeEnabled`, `v1UnmutedChimeEnabled`, `v1ChatMessageReceivedChimeEnabled` | yes | `"true"` / `"false"` (missing = enabled) | `update-chime-setting` |
| `v1VoiceChatReportingDisclosureAcceptanceStatus` | no | `never-shown` (default) / `seen-not-accepted` / `seen-accepted` | `update-voice-chat-reporting-disclosure-acceptance-status` |
| `v1GlobalNicknamesHasSeenDisclosure` | no | `"true"` | `update-show-new-alias-feature-flag` |
| `v1AgeVerificationChatRestrictionNotificationSeen` | no | `"true"` | `update-show-age-verification-required-notification` |
| `v1EpicPartiesProfileMoveHasSeenDisclosure` | no | `"true"` (default `true`) | `update-profile-move-disclosure-seen` |
| `v1AccessibilityAllowVoiceDictation`, `v1AccessibilityReadMessagesAloud` | | `"true"` / `"false"` (default `false`) | returned by the query; writer not traced |

Scoped settings are written with `scopes: { v1Platform: <osName>, v1DeploymentId: <deploymentId> }`; unscoped ones with `scopes: {}`.

Windows device ids: on save the overlay strips the WASAPI wrapper (`{0.0.0.00000000}.{<guid>}` or `{<guid>}` -> `<guid>`); on load it rebuilds `{0.0.0.00000000}.{<guid>}` for output (render) and `{<guid>}` for input (capture). See [Voice Settings](../../Launcher/Voice/Settings.md).
