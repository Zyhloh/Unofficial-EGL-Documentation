## Deck - Features: Evaluate Features

Evaluates a set of feature flags for one machine and returns their served values. Polled by the launcher (`eglv2_lib::launchdarkly::relay_actor`, `src\launchdarkly\relay_http.rs`) at start and then every `flag-poll-interval-minutes` (15), logged as `flag relay poll ok flags=37` (`Flags.RelayPolled`).

URL: https://distro-gateway-prod.ol.epicgames.com/deck/v1/features \
Method: POST \
Auth Required: No

## Headers
`Content-Type`: application/json <br/>

## Body

```json
{
  "flags": {
    "presence-mode": "social-overlay",
    "quiet-hours-enabled": true,
    "self-update-mode": "disabled"
  },
  "context": {
    "kind": "multi",
    "machine": {
      "environment": "prod",
      "os": "windows",
      "arch": "x86_64",
      "currentVersion": "0.115.0+gd6d2ef8",
      "releaseChannel": "stable"
    },
    "user": {
      "anonymous": true
    }
  }
}
```

`flags`: Required. Object of flag key to the client's default value <br/>
`context`: `RelayContext` with a `machine` (`RequestAttributes`: `environment` `prod` / `gamedev` / `ci`, `os`, `arch`, `currentVersion`, `releaseChannel` `stable` / `stage` / `canary` / `manual`) and an anonymous `user` <br/>

---

_Example Response_

```json
{
  "presence-mode": "social-overlay",
  "quiet-hours-enabled": false,
  "self-update-mode": "forced"
}
```

One entry per requested key. A key the relay does not know comes back with the default that was sent.

Values served on 13 November 2026 that differ from the client defaults (all 37 registry flags were requested):

| Flag | Client default | Served |
| --- | --- | --- |
| `cloud-saves-enabled` | `false` | `true` |
| `feedback-enabled` | `false` | `true` |
| `whats-new-modal-enabled` | `false` | `true` |
| `in-place-updates-enabled` | `true` | `false` |
| `quiet-hours-enabled` | `true` | `false` |
| `self-update-mode` | `"disabled"` | `"forced"` |
| `self-update-target-version` | `""` | `"0.115.0+gd6d2ef8"` |
| `self-update-cdn-base-urls` | `[]` | `["https://content-download-egs.distro.on.epicgames.com/Builds/EGLv2"]` |
| `self-update-lazy-hold-minutes` | `60` | `1` |
| `dev-build-polling-tiers` | `null` | `{"turbo": 2, "fast": 10}` |

Errors:

| Request | Response |
| --- | --- |
| No `flags` | 400 `{"message":"flags is a required parameter.","correlationId":"..."}` |
| `GET` | 404 `{"message":"Route GET:/api/v1 not found","error":"Not Found","statusCode":404}` |
| `flags` as an array or string | 200, but the relay spreads it into an index-keyed object (`{"0":"presence-mode"}`), so the client must send an object |
