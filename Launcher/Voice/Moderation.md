# Voice - Moderation And Reporting

Party voice rooms are moderated: every participant registers an Ed25519 key, signs its audio, and the SDK keeps a local recording that can be uploaded as a report. Key and room-mode behaviour confirmed live on 2026-10-14; the report upload path is from the SDK and overlay code.

## Voice moderation key

1. Generate an Ed25519 key pair (EGL: `Moderation::GenerateKeys`).
2. Register the raw 32-byte public key with a plain EG1 token: [Register Public Key](../../EpicGames/PublicKeyService/PublicKey/Register.md) `{ "algorithm": "ed25519", "key": "<base64>" }` -> `{ key, account_id, key_guid, kid, expiration, jwt, type }`. JWT (EdDSA, `kid` `20230621`) claims `account_id`, `generated`, `key_guid`, `kid`, `key`, `expiration` (about two months), `type: "legacy"`. `/publickey/v2/so/` rejects EG1.
3. Join with `voice_moderation: { signed_public_key: <jwt> }` and option `signed_audio` ([RTC Signaling](RTCSignaling.md#join)). `join_res.options` echoes `signed_audio`.
4. Sign every outgoing Opus payload with the private key ([Audio Signing](AudioSigning.md)).
5. Other participants' JWTs arrive in `user_joined.voice_moderation.signed_public_key` (also inside the `join_res.users` strings). Verify the JWT with Epic's signing key ([Get Signing Keys](../../EpicGames/PublicKeyService/PublicKey/SigningKeys.md#verifying-a-key-jwt): header has no `kid`, take `kid` from the payload, EdDSA over `header.payload`; confirmed working), check `account_id` = the participant's `user_token`, then use the `key` claim to verify their audio ([Audio Signing](AudioSigning.md#receiving)).

### Room mode

The first participant to join fixes the room's moderation mode. A client that joins without `signed_audio` + `signed_public_key` creates an unmoderated room; EGL joining afterwards fails with `VoiceModerationModeMismatch` and shows "Unable to connect to voice chat". Every client must join moderated. The SDK itself refuses to join moderated without a signer (`RTCRoom JoinRoom was not sent due to misconfigured voice moderation settings. A sending signature was missed`).

## Reporting preference

The overlay's "Reporting on / off" label:

```
reportingOn = party.is_reportable || kws(chat/enhanced-voice-reporting).effectiveValue == "recording"
```

- `is_reportable` is computed by the server and only read by the client ([below](#is_reportable)). New parties start `false`.
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

### is_reportable

Party field, computed by the server, pushed in `party.v2.PARTY_UPDATED` and returned by [Get Party](../../EpicGames/PartyService/Parties/GetParty.md). Clients never write it. Observed live (2026-10-14, two EGL members):

| Event | `is_reportable` |
| --- | --- |
| party created, one member in voice | `false` |
| second member claims voice (`active_in_party_voice_room: true`) | `true` |
| a member deafens (EGL PATCHes its member meta with `active_in_party_voice_room: false`) | `false` |
| that member undeafens (`true` again) | `true` |
| mic mute / unmute (meta PATCH, flag stays `true`) | unchanged |

So it is `true` while at least 2 members have a connection with `active_in_party_voice_room: true`. Exception seen: a 3-member party with one EGL member and one Fortnite (Switch) member both flagged active stayed `false`; the rule for cross-product parties is not pinned down. The chat conversation has its own flag (`social.chat.v1.REPORTABILITY_CHANGE`, `isReportable`), which stayed `false` in all captures.

Captured `PARTY_UPDATED` when the second member claimed voice:

```json
{
  "correlationId": "92e55a4e-8896-4046-a67a-46bb36b68e17",
  "timestamp": 1792000734569,
  "id": "ZDAwYzYyNmRmM2FiMTJmYQ",
  "connectionId": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
  "payload": {
    "sent": "2026-10-14T17:58:54.569Z",
    "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "party_lead": "94b1569506b04f9f8557af611e8c5e47",
    "meta": {
      "created_by": "94b1569506b04f9f8557af611e8c5e47"
    },
    "party_privacy_type": "INVITE_ONLY",
    "max_number_of_members": 16,
    "chat_conversation_id": "ep-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "created_at": "2026-10-14T17:58:53.823Z",
    "updated_at": "2026-10-14T17:58:54.568Z",
    "is_reportable": true,
    "revision": 1
  },
  "type": "party.v2.PARTY_UPDATED"
}
```

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
