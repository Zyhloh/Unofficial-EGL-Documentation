# Voice - Moderation And Reporting

Party voice rooms are moderated: every participant registers an Ed25519 key, signs its audio, and the SDK keeps a local recording that can be uploaded as a report. Key and room-mode behaviour confirmed live on 2026-10-14; the report upload path is from the SDK and overlay code.

## Voice moderation key

1. Generate an Ed25519 key pair (EGL: `Moderation::GenerateKeys`).
2. Register the raw 32-byte public key with a plain EG1 token: [Register Public Key](../../EpicGames/PublicKeyService/PublicKey/Register.md) `{ "algorithm": "ed25519", "key": "<base64>" }` -> `{ "jwt" }`. JWT (EdDSA, `kid` `20230621`) claims `account_id`, `generated`, `key_guid`, `kid`, `key`, `expiration` (about two months), `type: "legacy"`. `/publickey/v2/so/` rejects EG1.
3. Join with `voice_moderation: { signed_public_key: <jwt> }` and option `signed_audio` ([RTC Signaling](RTCSignaling.md#join)). `join_res.options` echoes `signed_audio`.
4. Sign every outgoing Opus payload with the private key ([Audio Signing](AudioSigning.md)).
5. Other participants' JWTs arrive in `user_joined.voice_moderation.signed_public_key`; their `key` claim verifies their audio.

### Room mode

The first participant to join fixes the room's moderation mode. A client that joins without `signed_audio` + `signed_public_key` creates an unmoderated room; EGL joining afterwards fails with `VoiceModerationModeMismatch` and shows "Unable to connect to voice chat". Every client must join moderated. The SDK itself refuses to join moderated without a signer (`RTCRoom JoinRoom was not sent due to misconfigured voice moderation settings. A sending signature was missed`).

## Reporting preference

The overlay's "Reporting on / off" label:

```
reportingOn = party.is_reportable || kws(chat/enhanced-voice-reporting).effectiveValue == "recording"
```

- `is_reportable` is server-set and only read by the client ([Get Party](../../EpicGames/PartyService/Parties/GetParty.md), `party.v2.PARTY_UPDATED`, `social.chat.v1.REPORTABILITY_CHANGE`). New parties start `false`.
- The personal preference is KWS `chat` / `enhanced-voice-reporting`: [Get Setting Values](../../EpicGames/KWS/Settings/GetValues.md) / [Update Setting Values](../../EpicGames/KWS/Settings/UpdateValues.md).

Toggle (real, response captured):

```
PATCH https://api.kws.ol.epicgames.com/v1/epic-settings/public/users/94b1569506b04f9f8557af611e8c5e47/values
```

```json
{
  "game": "fn",
  "settings": [
    { "namespace": "chat", "settingName": "enhanced-voice-reporting", "preferredValue": "prefer-not-recording" }
  ]
}
```

`preferredValue`: `recording` ("Always On") or `prefer-not-recording` ("Off When Possible", the age-bracket default). The same PATCH shape sets `text`, `voice`, `enhanced-text-reporting`, `filter-out-mature-language`, `filter-out-pii` and `party` / `party-joinability`.

When the label is on and the room is connected, the overlay tells the SDK to resume recording (`start-voice-recording`); otherwise it suspends it (`pause-voice-recording`). The preference does not change the room's moderation mode or the need to sign audio.

## Preconditions for voice

- Voice reporting disclosure accepted: SOCS `v1VoiceChatReportingDisclosureAcceptanceStatus` = `seen-accepted` (default `never-shown`; dialog `VoiceReportUpdate*`, links `https://fn.gg/voice-reporting-faqs`, `https://fn.gg/voice-text-reporting`). Accepting also re-sends the KWS settings with `voiceChatSetting` (`update-fortnite-settings`). Until then the overlay blocks voice (`no:voice-reporting-disclosure`). Whether the server enforces it was not tested.
- Reports need `is_reportable: true` on the party.

## Recording

With voice moderation the SDK keeps a rolling local recording per room (`FRTCAudioLogicRecord`, `RecordMaxDurationSeconds`) of signed audio frames. State is published as `voice-moderation` `{ recording, reportStatus, reportUploadProgress, emeraldReportToken, localUserId }`.

## Report flow

1. User opens `report-party-voice-chat` (`ReportPartyVoiceChatDialog`). The overlay sends `set-party-voice-report-in-progress` `{ inProgress: true }` (feature `parties`) and `query-recorded-participants` (feature `party`).
2. SDK `HandleQueryRecordedParticipantsIntent` (`QueryRecordInformationPrivate`) publishes `voice-report` `{ recordId, participants: [{ userId, displayName }], status }`. The dialog lists everyone recorded except the reporter, 8 per row. Nobody else recorded -> "no voice data".
3. User presses Submit -> `submit-voice-report` `{}`.
4. SDK `HandleSubmitVoiceReportIntent` -> `FRTCAudioLogicRecord::StartRecordUploadToEmerald`:
   - [Emerald SO init](../../EpicGames/EmeraldService/SDK/SOInit.md) (`EOS_Private_Emerald_InitializeUpload`) returns `token` and `files` -> `recording.bin` -> `chunkUrls` (exactly one URL).
   - The archived recording is `PUT` to that URL ([Upload Recording](../../EpicGames/EmeraldService/SDK/ChunkUpload.md), `UploadReportArchive`).
   - [Emerald SO complete](../../EpicGames/EmeraldService/SDK/SOComplete.md) (`EOS_Private_Emerald_FinalizeUpload`) with the token.
   - `voice-moderation.reportStatus` goes `uploading` (with `reportUploadProgress`) -> `success` with `emeraldReportToken`, or `failure` / `noVoiceData`.
5. On `success` the overlay sends `compass-send-report` -> [Compass Send Report](../../EpicGames/CompassService/Reports/SendReport.md) with body (shape from client):

```json
{
  "emerald_token": "...",
  "reason": "voice",
  "product_id": "...",
  "reporter_entity_id": "94b1569506b04f9f8557af611e8c5e47"
}
```

6. The returned `report_id` is shown with the lookup link `https://epic.gm/my-reports`.

The report upload was not captured.

## Emerald routes in the SDK

The SDK uses the `/emerald/v1/so/*` pair because the reporter is an Epic account id; `/emerald/v1/init` / `/emerald/v1/complete` are the product-user-id variant. Host and bodies: [Emerald Service](../../EpicGames/EmeraldService/README.md). Recording can also go to a custom URL (`StartRecordUploadToCustomUrl`), not used by the overlay.
