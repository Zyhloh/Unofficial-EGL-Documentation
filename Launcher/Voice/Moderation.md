# Voice - Moderation And Reporting

Party voice reports are two uploads: the EOS SDK uploads the recorded audio to Emerald and gets a token, then the overlay files a Compass report with that token.

## Preconditions

- The party has `is_reportable: true` ([Get Party](../../EpicGames/PartyService/Parties/GetParty.md), `party.v2.PARTY_UPDATED`).
- Voice reporting disclosure accepted: SOCS `v1VoiceChatReportingDisclosureAcceptanceStatus` = `seen-accepted` (dialog `VoiceReportUpdate*`, links `https://fn.gg/voice-reporting-faqs`, `https://fn.gg/voice-text-reporting`). Accepting also re-sends the KWS settings with `voiceChatSetting` (`update-fortnite-settings`). Until then voice is blocked (`no:voice-reporting-disclosure`).
- KWS `enhancedVoiceReportingEffectiveValue` decides whether the room records (`recording` / `prefer-not-recording`).

## Recording

When the room connects with voice moderation the SDK keeps a rolling local recording per room (`FRTCAudioLogicRecord`, `RecordMaxDurationSeconds`) of signed audio frames. The overlay can steer it with `start-voice-recording` / `pause-voice-recording` (feature `party`). State is published as `voice-moderation` `{ recording, reportStatus, reportUploadProgress, emeraldReportToken, localUserId }`.

## Flow

1. User opens `report-party-voice-chat` (`ReportPartyVoiceChatDialog`). The overlay sends `set-party-voice-report-in-progress` `{ inProgress: true }` (feature `parties`) and `query-recorded-participants` (feature `party`).
2. SDK `HandleQueryRecordedParticipantsIntent` (`QueryRecordInformationPrivate`) publishes `voice-report` `{ recordId, participants: [{ userId, displayName }], status }`. The dialog lists everyone recorded except the reporter, 8 per row. Nobody else recorded -> "no voice data".
3. User presses Submit -> `submit-voice-report` `{}`.
4. SDK `HandleSubmitVoiceReportIntent` -> `FRTCAudioLogicRecord::StartRecordUploadToEmerald`:
   - [Emerald SO init](../../EpicGames/EmeraldService/SDK/SOInit.md) (`EOS_Private_Emerald_InitializeUpload`) returns `token` and `files` -> `recording.bin` -> `chunkUrls` (exactly one URL).
   - The archived recording is `PUT` to that URL ([Upload Recording](../../EpicGames/EmeraldService/SDK/ChunkUpload.md), `UploadReportArchive`).
   - [Emerald SO complete](../../EpicGames/EmeraldService/SDK/SOComplete.md) (`EOS_Private_Emerald_FinalizeUpload`) with the token.
   - `voice-moderation.reportStatus` goes `uploading` (with `reportUploadProgress`) -> `success` with `emeraldReportToken`, or `failure` / `noVoiceData`.
5. On `success` the overlay sends `compass-send-report` -> [Compass Send Report](../../EpicGames/CompassService/Reports/SendReport.md) with body:

```json
{
  "emerald_token": "...",
  "reason": "voice",
  "product_id": "...",
  "reporter_entity_id": "94b1569506b04f9f8557af611e8c5e47"
}
```

6. The returned `report_id` is shown with the lookup link `https://epic.gm/my-reports`.

## Emerald routes in the SDK

The SDK uses the `/emerald/v1/so/*` pair because the reporter is an Epic account id; `/emerald/v1/init` / `/emerald/v1/complete` are the product-user-id variant. Host and bodies: [Emerald Service](../../EpicGames/EmeraldService/README.md). Recording can also go to a custom URL (`StartRecordUploadToCustomUrl`), not used by the overlay.
