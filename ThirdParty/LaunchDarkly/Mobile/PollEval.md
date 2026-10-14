## LaunchDarkly - Mobile: Poll Flag Evaluations

Polling counterpart of [Stream Flag Evaluations](StreamEval.md). Present as the SDK default polling endpoint (`/msdk/evalx/contexts`, and `/msdk/evalx/context` for the REPORT variant); the launcher does not call `LDClientConfigBuilder_DataSource_MethodPoll`, so this build is not expected to use it (inferred).

URL: https://clientsdk.launchdarkly.com/msdk/evalx/contexts/:context \
Method: GET \
Auth Required: Yes (mobile key)

## Headers
`Authorization`: mobile key <br/>

## Path Parameters
`context`: base64url of the context JSON (see [Stream Flag Evaluations](StreamEval.md#context)) <br/>

---

Response: flag key -> evaluation map (LaunchDarkly client-side protocol, not visible in the exe).
