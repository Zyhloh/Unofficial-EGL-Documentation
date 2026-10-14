## Overlay Feature Flags Service - Features: Get Features

Server-side LaunchDarkly evaluation for the social overlay (`flags-module`, base `EPIC_LAUNCHDARKLY_ENDPOINT`). The launcher's own flags are separate, see [Architecture](../../../Launcher/Architecture.md#feature-flags).

URL: https://api.epicgames.dev/overlay-launch-darkly/v1/features \
Method: POST \
Auth Required: No (no Authorization header is set)

## Headers
`Content-Type`: application/json <br/>

## Body
```json
{
  "accountId": "94b1569506b04f9f8557af611e8c5e47",
  "flags": {},
  "custom": {
    "platformName": "egs",
    "gitHash": "48a8a998c785c6c7358b56ddc82474ca23ae565f",
    "features": ["account", "friends", "party", "presence"]
  }
}
```

`flags` holds the overlay's default flag values; `custom` is the platform info object plus `gitHash` and the SDK feature list.

---

_Example Response_

```json
{}
```

A map of flag key to value. The overlay caches it in `localStorage` under `epicld-<accountId>` (`epicld-anonymous` when signed out) and falls back to it, then to the defaults, on error.
