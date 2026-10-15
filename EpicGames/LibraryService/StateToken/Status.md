## Library Service - State Token: Status

Checks whether a library `stateToken` (from [Library Items](../Library/Items.md)) is still current. If `valid` is `true` the launcher extends its library cache TTL and skips the full page walk ("Refresh skipped (state token valid)"). Otherwise it performs a full refresh.

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/stateToken/:stateToken/status \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`stateToken`: The `responseMetadata.stateToken` of the last library walk

---

_Example Response_

```json
{
  "valid": true
}
```
