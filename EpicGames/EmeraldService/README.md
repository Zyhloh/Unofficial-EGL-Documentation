# Hosts

This are some (not all) Hosts that you can access the Emerald Service from

- emerald-service-live.ecosec.on.epicgames.com
- api.epicgames.dev (path prefix `/emerald`, answered by `com.epicgames.emerald-service`)

<br/>

Recommended Hosts:

- emerald-service-live.ecosec.on.epicgames.com

Two clients use Emerald in eglv2:

- The social overlay web app uploads chat evidence itself, with the hardcoded host above and without `X-Epic-Agent` / `X-EPIC-CORRELATION-ID`.
- The EOS SDK uploads party voice recordings. Its host is the `EmeraldService` entry of the SDK config, which is not in the public platform config and is assumed to come from [Product Config](../EOSSDKConfigService/Config/ProductConfig.md); which of the two hosts it gets needs a live capture.

Endpoints used by eglv2:

- [Text/Upload](Text/Upload.md) - `POST /emerald/v1/text/upload` (overlay, chat reports)
- [SDK/SOInit](SDK/SOInit.md) - `POST /emerald/v1/so/init` (SDK, voice reports)
- [SDK/ChunkUpload](SDK/ChunkUpload.md) - `PUT` to the returned chunk URL
- [SDK/SOComplete](SDK/SOComplete.md) - `POST /emerald/v1/so/complete`

`POST /emerald/v1/init` and `POST /emerald/v1/complete` (routes `InitUpload` / `CompleteUpload`) are the product-user-id variants of the SDK pair; eglv2 never has a product user id, so they are not used.
