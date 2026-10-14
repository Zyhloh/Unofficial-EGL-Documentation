## Emerald Service - SDK: Initialize Upload (Epic account)

First step of a party voice report upload, sent by the EOS SDK (`EOS_Private_Emerald_InitializeUpload`, task `EmeraldInitializeUploadTask`, route `InitUploadSO`) from `FRTCAudioLogicRecord::StartRecordUploadToEmerald` after the overlay sends `submit-voice-report`. See [Voice Moderation](../../../Launcher/Voice/Moderation.md).

The SDK picks the route by the type of `LocalUserId`: an Epic account id goes to `/emerald/v1/so/*`, a product user id to `/emerald/v1/init` / `/emerald/v1/complete` (same bodies). eglv2 only has an Epic account session (no `EOS_Connect_*`), so voice reports use this route.

URL: https://api.epicgames.dev/emerald/v1/so/init \
Method: POST \
Auth Required: Yes (Bearer Epic account access token)

The host comes from the SDK config `EmeraldService` entry ([Product Config](../../EOSSDKConfigService/Config/ProductConfig.md)), not from the binary. `api.epicgames.dev/emerald/...` is answered by `com.epicgames.emerald-service` (unauthenticated probe: 401 `missing or malformed authorization bearer header`); whether the SDK is pointed there or at `emerald-service-live.ecosec.on.epicgames.com` needs a live capture.

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Correlation-ID`: random id <br/>

## Query Parameters
`platform`: Platform name, optional (value not resolved statically) <br/>

## Body
```json
{
  "game": "..."
}
```

`game` is the only field written by the request serializer; its value is not resolved statically.

---

_Example Response (shape from client)_

```json
{
  "files": {
    "recording.bin": {
      "chunkUrls": [
        "https://..."
      ]
    }
  },
  "token": "..."
}
```

The SDK looks up its upload file name in `files` (`recording.bin`, overridable by the `ReportFileName` config key) and fails if `token` is empty, `files` is missing, `chunkUrls` is empty, or `chunkUrls` has more than one URL. The single URL is used for [Chunk Upload](ChunkUpload.md), the token for [Complete Upload](SOComplete.md).
