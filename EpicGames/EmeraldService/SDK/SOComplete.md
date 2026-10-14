## Emerald Service - SDK: Complete Upload (Epic account)

Last step of a party voice report upload, sent by the EOS SDK (`EOS_Private_Emerald_FinalizeUpload`, task `EmeraldFinalizeUploadTask`, route `CompleteUploadSO`) after [Upload Recording](ChunkUpload.md). On success the SDK logs `The report has been successfully registered in the Emerald service` and publishes `voice-moderation` `{ reportStatus: "success", emeraldReportToken }`; the overlay then files the [Compass report](../../CompassService/Reports/SendReport.md) with that token.

Product user ids use `POST /emerald/v1/complete` with the same body instead.

URL: https://api.epicgames.dev/emerald/v1/so/complete \
Method: POST \
Auth Required: Yes (Bearer Epic account access token)

Host: see [Initialize Upload](SOInit.md).

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Correlation-ID`: random id <br/>

## Query Parameters
`platform`: Platform name, optional (value not resolved statically) <br/>

## Body
```json
{
  "token": "..."
}
```

`token` is the `token` from [Initialize Upload](SOInit.md); the SDK rejects an empty one (`EOS_Emerald_FinalizeUploadOptions.Token reason: can't be null or empty`).

---

No response fields are deserialized.
