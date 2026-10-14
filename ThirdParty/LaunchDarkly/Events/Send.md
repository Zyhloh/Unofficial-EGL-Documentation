## LaunchDarkly - Events: Send

Analytics events (flag evaluations, identify) from the C++ client-side SDK. The launcher enables them (`LDClientConfigBuilder_Events_Enabled(true)`) and keeps the default events host.

URL: https://mobile.launchdarkly.com/mobile \
Method: POST \
Auth Required: Yes (mobile key)

`https://events.launchdarkly.com` only appears in the shell webview CSP (`connect-src`); no caller was found.

## Headers
`Authorization`: mobile key <br/>
`Content-Type`: application/json <br/>
`X-LaunchDarkly-Event-Schema`: schema version <br/>
`X-LaunchDarkly-Payload-Id`: payload id <br/>

Header names from the SDK strings; values not recovered.

## Body
JSON array of LaunchDarkly client-side events (`identify`, `summary`, ...), with the context from [Stream Flag Evaluations](StreamEval.md#context); `email` is sent redacted as a private attribute.
