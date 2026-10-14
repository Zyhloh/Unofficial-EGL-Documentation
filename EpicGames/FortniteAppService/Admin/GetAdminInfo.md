## Fortnite App Service - Admin: Get Admin Info

Build info of the Fortnite backend that serves an app. Host is the `admin_domain` from [Get Apps](../Apps/GetApps.md), not a fixed host (`invalid FN admin domain` when it does not parse). Result is returned by `get_fn_deployment_info` as `FnDeploymentInfo { adminUrl, build }`.

URL: https://:adminDomain/fortnite/api/admin/info \
Method: GET \
Auth Required: Unknown

## Path Parameters
`adminDomain`: Backend admin domain from the app registry

---

_Example Response (shape from client, `FnDeploymentBuildInfo`)_

```json
{
  "productVersion": "...",
  "branchName": "...",
  "changelist": 0,
  "buildNumber": 0,
  "calendarOffsetMinutes": 0
}
```

Field types are placeholders.
