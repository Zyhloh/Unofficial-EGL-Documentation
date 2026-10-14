# Voice - Settings, Mute, Push-To-Talk, Indicators

## Where settings live

| Store | Keys | Written by |
| --- | --- | --- |
| SOCS (cloud, per account, scoped by `v1Platform` + `v1DeploymentId`) | `v1VoiceInputDevice`, `v1VoiceOutputDevice`, `v1VoiceInputVolume`, `v1VoiceOutputVolume`, `v1VoiceChatMode`, `v1VoicePushToTalkKeybinding`, chime toggles, `v1VoiceChatReportingDisclosureAcceptanceStatus` | overlay, [SOCS Service](../../EpicGames/SOCSService/README.md) |
| KWS (cloud, per account) | `chat` / `voice` (audience), `chat` / `enhanced-voice-reporting` (reporting preference) | overlay, [KWS](../../EpicGames/KWS/README.md), see [Moderation](Moderation.md#reporting-preference) |
| `voice-settings.json` in the launcher settings dir (`eglv2_lib::settings::voice_settings`, `VoiceSettingsStore`) | `configName` values the overlay reads with `getlocalvoicesetting`: `muted`, `deafened`, `loudspeaker`, `stt`, `tts` | overlay through `set-local-voice-setting` |
| EOS SDK (`RtcDeviceStateManager`) | current / preferred input and output device, falls back to `{default}` and remembers an unavailable choice | `update-voice-settings` |

A corrupt `voice-settings.json` is preserved and the store starts empty (`Settings.Voice.Corrupt`).

### SOCS voice settings

Server defaults from a captured [Query User Settings](../../EpicGames/SOCSService/Settings/QueryUserSettings.md) response (account with no overrides):

| Setting id | Default |
| --- | --- |
| `v1VoiceChatMode` | `openMic` (`pushToTalk` is the other value) |
| `v1VoiceInputDevice` | `""` |
| `v1VoiceInputVolume` | `50` |
| `v1VoiceOutputDevice` | `""` |
| `v1VoiceOutputVolume` | `50` |
| `v1VoicePushToTalkKeybinding` | `""` (keys joined with `+`, e.g. `CONTROL+V`) |
| `v1VoiceChatReportingDisclosureAcceptanceStatus` | `never-shown` (`seen-not-accepted`, `seen-accepted`) |

Values are strings. None of them affect the server side of a call; a standalone client can ignore SOCS.

## Startup sequence

1. `fetch-initial-socs-settings` -> [Query User Settings](../../EpicGames/SOCSService/Settings/QueryUserSettings.md) -> value `socs-settings` `{ inputDevice, inputVolume, outputDevice, outputVolume, pttEnabled, pushToTalkInputKeys, voiceChatReportingDisclosureStatus, chimeSettings, ... }`.
2. The overlay pushes it to the SDK as `update-voice-settings`. Device ids are deferred until the SDK has published `input-device` / `output-device` options. If `pttEnabled` and no explicit mute, `inputMuted: true` is added.
3. If a PTT key is set and the host supports bindings, `configure-bindings` registers a global `push-to-talk` binding.
4. Local `muted` / `deafened` / `loudspeaker` from `voice-settings.json` (value `settings`) are re-applied as `update-voice-settings`.

## Mute / deafen / push-to-talk

| Action | Intent payload (`party` / `update-voice-settings`) |
| --- | --- |
| Mute | `{ inputMuted: true }` |
| Unmute | `{ inputMuted: false }` |
| Deafen (mic on) | `{ audioEnabled: false, inputMuted: true }`, remembers `inputPreviouslyAutoMuted` |
| Deafen (already muted) | `{ audioEnabled: false }` |
| Undeafen | `{ audioEnabled: true }` |
| PTT pressed (mode `pushToTalk`) | `{ inputMuted: false, audioEnabled: true }` |
| PTT released | `{ inputMuted: true }` |
| Volume | `{ inputVolume }` / `{ outputVolume }` (iOS loudspeaker forces `outputVolume: 100`) |
| Per-member | `set-participant-audio` `{ id, volume }` / `{ id, muted }` (local only) |

PTT state comes back as the `bindings` collection item `push-to-talk` `{ isActivated }` (or an `application` / `binding` notification) and as `voice-room.pttActive`. Deafened state also flips `active_in_party_voice_room` in the member meta ([Update Member Meta](../../EpicGames/PartyService/Members/UpdateMemberMeta.md)) after a 1s debounce.

In the SDK, mute + deafen collapse to `EOS_RTCAS_Enabled` / `EOS_RTCAS_Disabled` / `EOS_RTCAS_NotListeningDisabled`; peers see deafened as `notListening`.

### On the wire

Captured from EGL's signaling ([RTC Signaling](RTCSignaling.md#mute_audio)):

| Action | Signaling messages |
| --- | --- |
| Mute | `mute_audio { is_muted: 1, reason_enum: 1 }` |
| Unmute | `mute_audio { is_muted: 0, reason_enum: 0 }` |
| Deafen | `mute_audio { is_muted: 1, reason_enum: 1 }`, `mute_audio { is_muted: 1, reason_enum: 3 }`, `subscribe { audio: false }` per participant |
| Undeafen | `mute_audio { is_muted: 0, reason_enum: 0 }`, `subscribe { audio: true }` per participant |
| Per-member volume / local mute | nothing sent (local only) |

Muted clients keep the media connection; whether EGL stops sending RTP while muted was not measured.

Settings telemetry names (`eos.social.settingschanged`): `chat.voice.input-device`, `chat.voice.input-volume`, `chat.voice.input-mode`, `chat.voice.output-device`, `chat.voice.output-volume`, `chat.voice.push-to-talk-keybind`, `chat.voice.loudspeaker`.

## Voice eligibility gate

Evaluated in order; anything but `yes` disconnects / blocks voice:

| Result | Cause |
| --- | --- |
| `no:age-verification-required` | age verification pending |
| `no:cabined-mode` | cabined account |
| `no:voice-chat-parental-limit` | KWS parental limit `nobody` (voice reconnects when lifted) |
| `no:voice-chat-social-ban` | active social ban on voice |
| `no:voice-reporting-disclosure` | `v1VoiceChatReportingDisclosureAcceptanceStatus` is not `seen-accepted` |
| `no:voice-chat-setting` | user voice chat setting `nobody` |
| `yes` | |

## Speaking indicators

`voice-room.participants[]` (`speaking`, `muted`, `notListening`, `voiceChatOff`) drive the avatar rings (`isSpeaking`), mute / deafen badges and "voice off" state per member. Members absent from the list get `speaking` reset (`resetAbsentMembersSpeakingValue`).

## Tray and taskbar

The overlay sends `voice-party-state-changed` `{ state }` whenever the computed state changes:

| state | Condition |
| --- | --- |
| `not-in-party` | no active party, or voice is held by another device |
| `deafened` | local output deafened |
| `muted` | local input muted |
| `in-party` | otherwise |

The launcher also accepts `in-party-speaking` (serde enum `not-in-party`, `in-party`, `in-party-speaking`, `muted`, `deafened`), which this overlay build never sends. `eglv2_lib::social::voice_party` renders the state on every "shell surface": `windows::tray_icon` (icon of tray `main-tray`) and `windows::taskbar_badge` (COM taskbar overlay). Writes that fail are retried (`voice_party::retry`, `Social.Voice.SurfaceUpdated` / `Social.Voice.SurfaceUpdateFailed`).
