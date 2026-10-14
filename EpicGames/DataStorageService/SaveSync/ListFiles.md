## Data Storage Service - Save Sync: List Files

Lists the cloud save files of one game with signed read links. Used by the cloud save service (`eglv2_lib::cloud_saves::service`, probe `CloudSaves.Probe.AccountListed`, `CloudSaves.Probe.ManifestsListed`). See [Cloud Saves](../../../Launcher/Flows/CloudSaves.md).

URL: https://datastorage-public-service-liveegs.live.use1a.on.epicgames.com/api/v1/access/egstore/savesync/:accountId/:path \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`accountId`: The account id <br/>
`path`: Folder under the account, `{appName}/` for a game; deeper segments (`manifests/`, `Chunks/`) address sub folders. Segments `.` / `..` are refused client side (`DataStorage path has a dot segment`)

---

_Example Response (shape from client, `AccessListing` / `AccessEntry`)_

```json
{
  "files": {
    "94b1569506b04f9f8557af611e8c5e47/Fortnite/manifests/94b1569506b04f9f8557af611e8c5e47.manifest": {
      "readLink": "https://...",
      "writeLink": "https://...",
      "lastModified": "2026-10-14T15:18:54.216Z",
      "size": 1024
    }
  }
}
```

Field names are from the binary; the key format of `files` is inferred. A 404 is `NOT_FOUND: the service refused the folder (404)`.
