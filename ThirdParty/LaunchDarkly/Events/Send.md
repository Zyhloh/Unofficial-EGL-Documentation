## LaunchDarkly - Events: Send

Analytics events (flag evaluations, identify) from the C++ client-side SDK. The launcher enables them (`LDClientConfigBuilder_Events_Enabled(true)`) and keeps the default events host; `/mobile` is the SDK's events path constant. Failed posts are logged by the SDK, e.g. `[LD SDK] flush-worker[0]: error posting 3 event(s) (will retry): CURL error: SSL connect error`.

URL: https://mobile.launchdarkly.com/mobile \
Method: POST \
Auth Required: Yes (mobile key)

`https://events.launchdarkly.com` only appears in the shell webview CSP (`connect-src`); no caller was found.

## Headers
`Authorization`: raw mobile key (per environment, see [Stream Flag Evaluations](../Mobile/StreamEval.md#client-config)) <br/>
`User-Agent`: `CPPClient/3.11.1` <br/>
`X-LaunchDarkly-Tags`: `application-version/<launcher version>` <br/>
`Content-Type`: application/json <br/>
`X-LaunchDarkly-Event-Schema`: schema version <br/>
`X-LaunchDarkly-Payload-Id`: payload id <br/>

`X-LaunchDarkly-Event-Schema` and `X-LaunchDarkly-Payload-Id` values are set by the SDK and were not seen on the wire.

## Body
JSON array of LaunchDarkly client-side events (`identify`, `summary`, ...), with the context from [Stream Flag Evaluations](StreamEval.md#context); `email` is sent redacted as a private attribute.
