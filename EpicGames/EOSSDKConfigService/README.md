# Hosts

This are some (not all) Hosts that you can access the EOS SDK Config Service from

- api.epicgames.dev (`prod`, path prefix `/sdk`)
- api-gamedev.ol.epicgames.net (`gamedev`, path prefix `/sdk`)

<br/>

Recommended Hosts:

- api.epicgames.dev

The only service base URLs compiled into the EOS SDK. They sit in an XOR-obfuscated ini embedded in `EOSSDK-Win64-Shipping.dll` (decoded at platform init, `sub_1806AAA30`):

```ini
[SDKConfig]
BaseUrl="https://api.epicgames.dev/sdk"

[SDKConfig GameDev]
BaseUrl="https://api-gamedev.ol.epicgames.net/sdk"

[SDKAnalytics]
BaseUrl="https://api.epicgames.dev/telemetry/data/"
UploadType="sdkevents"
```

The `GameDev` section is used when the platform's backend environment is `GameDev` (`EGL_EOS_BACKEND_ENVIRONMENT`, see [Clients](../../Launcher/Auth/Clients.md#eos-platform-config)).

The SDK (`FSDKConfigClient`) fetches both configs after `EOS_Platform_Create` and applies them on top of the embedded ini. Every other SDK service resolves its host from the `services` map: the route's service name plus `Service` (`Emerald` -> `EmeraldService`), falling back to an error `EpicGamesPlatform::GetBaseURL(%s) service name not found.`

Endpoints used by eglv2 (through the SDK):

- [Config/PlatformConfig](Config/PlatformConfig.md) - `GET /sdk/v1/default`
- [Config/ProductConfig](Config/ProductConfig.md) - `GET /sdk/v1/product/:productId`
