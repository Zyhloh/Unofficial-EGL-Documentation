## LaunchDarkly - Mobile: Stream Flag Evaluations

Feature flags for the launcher (`eglv2_lib::launchdarkly`, `src\launchdarkly\actor.rs`). The launcher links the LaunchDarkly C++ client-side SDK (`LDClientSDK_*`, `LDClientConfigBuilder_*`, version `3.11.1` per the live log `LaunchDarkly client started (non-blocking) sdk_version=3.11.1 env=Prod`) and drives it from Rust. It never picks a data-source method, so the SDK default (streaming) is used; [Poll](PollEval.md) is the SDK's polling alternative. Values reach the frontend through `get_feature_flags`, `flag-changed-event`, `ld-status-changed-event`; the flag list is in [Architecture - Feature flags](../../../Launcher/Architecture.md#feature-flags).

URL: https://clientstream.launchdarkly.com/meval/:context \
Method: GET \
Auth Required: Yes (mobile key)

Request shape (path, header) is the SDK's standard streaming request; only the host, `/meval` and the inputs below come from the exe.

## Headers
`Authorization`: mobile key, e.g. `mob-756bbe9a-3c91-4615-afeb-068c12fa9394` <br/>

## Path Parameters
`context`: base64url of the context JSON below <br/>

## Context

Built in `src\launchdarkly\context.rs`, always a multi-context:

```json
{
  "kind": "multi",
  "machine": {
    "kind": "machine",
    "key": "<machine id>",
    "currentVersion": "0.95.1+ge288862",
    "os": "windows",
    "arch": "x86_64",
    "releaseChannel": "stable"
  },
  "user": {
    "kind": "user",
    "key": "94b1569506b04f9f8557af611e8c5e47",
    "email": "user@example.com",
    "_meta": {
      "privateAttributes": ["email"]
    }
  }
}
```

Signed out, `user` is `{ "kind": "user", "key": "<anonymous key>", "anonymous": true }`. The machine key source and the user keys are inferred (first field of the machine / account structs).

| `releaseChannel` | |
| --- | --- |
| `stable` | default for fresh installs |
| `stage` | pre-release, between stable and canary |
| `canary` | pre-release (replaced `beta` / `dev`, renamed from `nightly`) |
| `manual` | opted out of auto-update |

## Client config

Calls made on `LDClientConfigBuilder_New(mobileKey)`: `Offline` (on with `-disable-ld` / `EGL_DISABLE_LD`), `Events_Enabled(true)`, `DataSource_WithReasons(false)`, `AppInfo_Version`, `HttpProperties_Tls` (CA bundle path), `Logging_Custom`, `Persistence_Custom` (cache in `cache\<env>\launchdarkly\flags.json`). No `ServiceEndpoints_*` setter is called, so the default hosts are used.

Mobile keys compiled into the exe (stored back to back; no code reference to them was found, so which key belongs to prod / gamedev / ci is not resolved):

- `mob-756bbe9a-3c91-4615-afeb-068c12fa9394`
- `mob-a3ca5f1c-8096-4f42-b82a-4fcc182bee42`
- `mob-a2836a0b-e080-4cb1-aa10-dfed41e26ce4`

An empty key for the active environment fails closed (`LaunchDarkly mobile key is empty for this environment; failing closed (every flag at its safe default)`, `Flags.MobileKeyMissing`). `ld-overrides.json(c)` (`-ld-overrides`, `EGL_LD_OVERRIDES`) overrides values locally.

---

Server-sent events (`put`, `patch`, `delete`) carrying flag values per the LaunchDarkly client-side streaming protocol.
