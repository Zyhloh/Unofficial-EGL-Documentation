## Avatar Service - Avatars: Fallback

The avatar to show for accounts that have none.

URL: https://api.epicgames.dev/epic/avatar/v1/:deploymentId/avatar/fallback \
Method: GET \
Auth Required: Yes (Bearer EG1 access token)

## Path Parameters
`deploymentId`: Avatars deployment, `9c9906b240c74a92a6b9100d6e4ccbd0`

---

_Example Response_

```json
{
  "url": "https://cosmo.fdeb.live.use1a.on.epicgames.com/cdn-cgi/image/height={},format=png/v1/item/uW4bCf0yPfr8vFyMBYZ4cRVh51ZmvMKstuuRr3rfZYo/png"
}
```

Without a token: 401 `errors.com.epicgames.unauthorized`. The social overlay also bundles its own `fallback-avatar-eglv2-<hash>.png`.
