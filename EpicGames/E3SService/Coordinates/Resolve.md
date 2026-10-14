## E3S Service - Coordinates: Resolve

Resolves a game-invite weblink (Sony weblink transport) to the session and artifact it points at (`eglv2_lib::api::e3s`, `src\api\e3s.rs`). Triggered when a `com.epicgames.launcher://invite?payload=<payload>` deep link is drained by `src\social\game_invite\weblink.rs`, only while the `game-invites-weblink` flag is on, the user is signed in and not in restricted mode. The resolved `artifactId` is mapped to an installed game; then the launcher calls [Join Session](../Session/Join.md) and launches the game.

URL: https://e3s-prod.social.live.on.epicgames.com/api/v1/coordinates \
Method: POST \
Auth Required: Yes (Bearer access token)

Sent through the shared API client (Bearer, refresh and retry on 401). The base URL is the `e3s_service` endpoint key (overridable with `-baseurl.e3s_service=`).

## Headers
`Content-Type`: application/json <br/>

## Body
```json
{
  "jsonWebToken": "<weblink token>"
}
```

`CoordinatesRequest` has one field. Where the token comes from (the invite deep-link payload) is inferred from the call order.

---

_Example Response (shape from client)_

```json
{
  "sessionId": "94b1569506b04f9f8557af611e8c5e47",
  "artifactId": "Fortnite",
  "expires": "2026-10-14T12:00:00.000Z",
  "sandboxId": "fn",
  "catalogItemId": "94b1569506b04f9f8557af611e8c5e47"
}
```

Field names from `CoordinatesResponse` (5 fields). Values and the `expires` format are placeholders.

| Outcome | Log / telemetry |
| --- | --- |
| `sessionId` or `artifactId` missing | `game-invite: weblink dropped (coordinates missing session/artifact)`, `Social.Invites.WeblinkCoordinatesIncomplete` |
| Request failed | `game-invite: weblink dropped (coordinates resolve failed)`, `Social.Invites.WeblinkCoordinatesFailed` |
| `artifactId` not a known game | `game-invite: weblink dropped (artifact resolved to no known game)` |
| Unsupported OS | `game-invite: weblink dropped (unsupported OS)`, `Social.Invites.WeblinkDroppedUnsupportedOs` |

On success the shell gets `social://game-invite-accepted` (or `social://game-invite-store` with `productSlug` / `appId` when the game is not installed, inferred from the event names next to the weblink code).
