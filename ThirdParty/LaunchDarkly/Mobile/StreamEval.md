## LaunchDarkly - Mobile: Stream Flag Evaluations

Feature flags for the launcher (`eglv2_lib::launchdarkly`, `src\launchdarkly\actor.rs`). The launcher links the LaunchDarkly C++ client-side SDK (`LDClientSDK_*`, `LDClientConfigBuilder_*`, version `3.11.1` per the live log `LaunchDarkly client started (non-blocking) sdk_version=3.11.1 env=Prod`) and drives it from Rust. It never picks a data-source method, so the SDK default (streaming) is used; [Poll](PollEval.md) is the SDK's polling alternative. Values reach the frontend through `get_feature_flags`, `flag-changed-event`, `ld-status-changed-event`; the flag list is in [Architecture - Feature flags](../../../Launcher/Architecture.md#feature-flags).

URL: https://clientstream.launchdarkly.com/meval/:context \
Method: GET \
Auth Required: Yes (mobile key)

Request shape (path, header) is the SDK's standard streaming request; only the host, `/meval` and the inputs below come from the exe. No `?withReasons=true` (`DataSource_WithReasons(false)`).

## Headers
`Authorization`: raw mobile key, no prefix, e.g. `mob-756bbe9a...` <br/>
`User-Agent`: `CPPClient/3.11.1` <br/>
`X-LaunchDarkly-Tags`: `application-version/<launcher version>` <br/>

## Path Parameters
`context`: base64url of the context JSON below <br/>

## Context

Built in `src\launchdarkly\context.rs`, always a multi-context:

```json
{
  "kind": "multi",
  "machine": {
    "kind": "machine",
    "key": "<device_id>",
    "currentVersion": "0.95.1+ge288862",
    "os": "windows",
    "arch": "x86_64",
    "releaseChannel": "stable"
  },
  "user": {
    "kind": "user",
    "key": "<accountId>",
    "email": "<email>",
    "_meta": {
      "privateAttributes": ["email"]
    }
  }
}
```

`machine.key` is `device_id` from `device.json` (uuid v4 created on first run). Signed in, `user.key` is the account id. Signed out, `user` is `{ "kind": "user", "key": "<device_id>", "anonymous": true }` with the same `device_id`.

| `releaseChannel` | |
| --- | --- |
| `stable` | default for fresh installs |
| `stage` | pre-release, between stable and canary |
| `canary` | pre-release (replaced `beta` / `dev`, renamed from `nightly`) |
| `manual` | opted out of auto-update |

## Client config

Calls made on `LDClientConfigBuilder_New(mobileKey)`: `Offline` (on with `-disable-ld` / `EGL_DISABLE_LD`), `Events_Enabled(true)`, `DataSource_WithReasons(false)`, `AppInfo_Version`, `HttpProperties_Tls` (CA bundle path), `Logging_Custom`, `Persistence_Custom` (cache in `cache\<env>\launchdarkly\flags.json`). No `ServiceEndpoints_*` setter is called, so the default hosts are used.

Mobile key per environment (`ld_start_client` reads it from a relative lookup table indexed by the environment, so the keys have no direct xrefs):

| `-epicenv` | Key |
| --- | --- |
| prod | `mob-756bbe9a...` |
| gamedev | `mob-a3ca5f1c...` |
| ci | `mob-a2836a0b...` |

An empty key for the active environment fails closed (`LaunchDarkly mobile key is empty for this environment; failing closed (every flag at its safe default)`, `Flags.MobileKeyMissing`). `ld-overrides.json(c)` (`-ld-overrides`, `EGL_LD_OVERRIDES`) overrides values locally.

Persistence: the `flags.json` namespace is `LaunchDarkly_` + base64(sha256(mobile key)); cached contexts are keyed by base64(sha256(canonical key)), e.g. `machine:<device_id>:user:<accountId>`.

---

Server-sent events (`put`, `patch`, `delete`) carrying flag values per the LaunchDarkly client-side streaming protocol.
