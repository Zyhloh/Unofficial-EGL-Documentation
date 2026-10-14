## E3S Service - Session: Join

Second step of a game-invite weblink, after [Resolve Coordinates](../Coordinates/Resolve.md) (`src\api\e3s.rs`). A failure is logged as `game-invite: weblink join failed` (`Social.Invites.WeblinkJoinFailed`). The debug command `debug_simulate_weblink_invite` stubs this call (`debug_simulate_weblink_invite: stub E3S join called session_id=`).

URL: https://e3s-prod.social.live.on.epicgames.com/api/v1/session/join \
Method: POST \
Auth Required: Yes (Bearer access token)

The path is built by pushing the segments `api`, `v1`, `session`, `join` onto the E3S base URL (`E3S base URL cannot be a base`, `invalid E3S base URL`).

## Headers
`Content-Type`: application/json <br/>

## Body
```json
{
  "jsonWebToken": "<weblink token>",
  "platform": "<platform>"
}
```

Field names from `JoinSessionRequest`. The `platform` value was not recovered.

---

The response type was not recovered.
