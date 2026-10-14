## Sentry - Envelope: Send

Crash / error reporting. Frontend uses `@sentry/browser` (release `epic-games-launcher@0.95.1+ge288862`, tags `runtime=frontend`, `build_branch`) and ships envelopes through the backend (`plugin:sentry|envelope`, `plugin:sentry|breadcrumb`, tauri-plugin-sentry); the Rust side reports panics (`telemetry::sentry`). Gated by `telemetry-sentry-sample-rate`, `EGL_DISABLE_SENTRY`. `-sentry-test=<panic|js-error|unhandled-rejection|ipc-error>` triggers test events.

URL: https://o10593.ingest.us.sentry.io/api/4511588248256512/envelope/ \
Method: POST \
Auth Required: Yes (`X-Sentry-Auth: Sentry sentry_key=69a1dea2bb3060b8934030e4d3de1d5b, ...`)

DSN (exe and frontend): `https://69a1dea2bb3060b8934030e4d3de1d5b@o10593.ingest.us.sentry.io/4511588248256512`, overridable with `EGL_SENTRY_DSN`.

## Headers
`Content-Type`: application/x-sentry-envelope <br/>
`X-Sentry-Auth`: `Sentry sentry_key=69a1dea2bb3060b8934030e4d3de1d5b, sentry_version=7, sentry_client=...` <br/>

## Body
Standard Sentry envelope: a header line (`event_id`, `sent_at`, `dsn`, `sdk`) followed by item header / payload line pairs (`event`, `session`, `attachment`, ...).

`https://o447951.ingest.sentry.io/api/4509632503087104/envelope/` (key `c1dfb07d783ad5325c245c1fd3725390`) is also in the binary but only inside the bundled Sentry SDK's `diagnoseSdkConnectivity()` helper; it is Sentry's own connectivity probe, not an Epic project.
