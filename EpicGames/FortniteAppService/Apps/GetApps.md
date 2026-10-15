## Fortnite App Service - Apps: Get Apps

Registry of Fortnite-backed apps (`fetch_registry`). `get_fn_deployment_info` (`{ catalogItemId }`) finds the record whose launcher `catalog_id` matches and fetches [Admin Info](../Admin/GetAdminInfo.md) from its backend admin domain. The registry is cached; on failure stale data is served (`FnDeployment.RegistryStaleServed`). Duplicate records for one `catalog_id` keep the later one.

URL: https://fortnite-app-service.eeef.live.use1a.on.epicgames.com/api/v1/apps \
Method: GET \
Auth Required: Unknown (the host does not answer from a public network: connection times out, also with the launcher's bearer token; likely internal only)

---

_Example Response (shape from client)_

```json
{
  "apps": [
    {
      "description": "...",
      "owned_by": {},
      "backend": {
        "environment": "prod",
        "has_backend_service": true,
        "admin_domain": "..."
      },
      "launcher": {
        "catalog_id": "94b1569506b04f9f8557af611e8c5e47"
      }
    }
  ]
}
```

Struct names: `RawAppsResponse`, `RawRegistryApp`, `RawRegistryOwner`, `RawRegistryBackend`, `RawRegistryLauncher`. Which field sits in which struct is inferred from the order of the names in the binary; `owned_by` contents were not recovered.
