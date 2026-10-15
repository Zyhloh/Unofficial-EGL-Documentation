## Data Storage Service - Save Sync: List Files

Lists cloud save files with signed S3 read and write links. See [Cloud Saves](../../../Launcher/Flows/CloudSaves.md).

URL: https://datastorage-public-service-liveegs.live.use1a.on.epicgames.com/api/v1/access/egstore/savesync/:accountId/:path \
Method: GET \
Auth Required: Yes (Bearer access token, own account)

## Path Parameters
`accountId`: The account id <br/>
`path`: Empty for every game of the account, `{appName}/` for one game. The trailing slash is required: `.../savesync/:accountId` without it returns 404

---

_Example Response (one game, shortened)_

```json
{
  "files": {
    "savesync/94b1569506b04f9f8557af611e8c5e47/24b4ee8b16e4450184fe33ff871cc0ee/manifests/2026.10.15-12.17.43.manifest": {
      "readLink": "https://eos-cloudsaves-live.s3.amazonaws.com/savesync/94b1569506b04f9f8557af611e8c5e47/24b4ee8b16e4450184fe33ff871cc0ee/manifests/2026.10.15-12.17.43.manifest?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20261015T115839Z&X-Amz-SignedHeaders=host&X-Amz-Credential=...&X-Amz-Expires=999&X-Amz-Signature=...",
      "writeLink": "https://eos-cloudsaves-live.s3.amazonaws.com/savesync/94b1569506b04f9f8557af611e8c5e47/24b4ee8b16e4450184fe33ff871cc0ee/manifests/2026.10.15-12.17.43.manifest?X-Amz-Algorithm=AWS4-HMAC-SHA256&...",
      "hash": "960bd292cd953dae47c83d33382141cb",
      "lastModified": "2026-10-15T12:17:43.000Z",
      "size": 1716,
      "fileLocked": false
    },
    "savesync/94b1569506b04f9f8557af611e8c5e47/24b4ee8b16e4450184fe33ff871cc0ee/ChunksV4/63/13F2B424DDC3F52A_5B4E896CCE2B4BC5A6382AA5D4801E18.chunk": {
      "readLink": "https://eos-cloudsaves-live.s3.amazonaws.com/...",
      "writeLink": "https://eos-cloudsaves-live.s3.amazonaws.com/...",
      "hash": "e057bbecc6b09a8e3c245c2b936029d0",
      "lastModified": "2026-10-15T12:17:43.000Z",
      "size": 39866,
      "fileLocked": false
    }
  },
  "folderThrottled": false,
  "maxFileSizeBytes": -1,
  "maxFolderSizeBytes": -1,
  "expiresAt": "2026-10-15T12:15:46.833Z"
}
```

Keys are full object paths (`savesync/<accountId>/<appName>/...`). `hash` is the MD5 of the stored object, `size` its stored size. Links are presigned for 999 seconds. Each game folder holds `manifests/<UTC timestamp>.manifest` and `ChunksV4/<group>/<hash>_<guid>.chunk`; see [Cloud Saves](../../../Launcher/Flows/CloudSaves.md#storage-format).

_Example Response (no trailing slash)_

```json
{
  "errorCode": "errors.com.epicgames.datastorage.folder_not_found_or_not_allowed",
  "errorMessage": "Resource not found or access denied",
  "code": "errors.com.epicgames.datastorage.folder_not_found_or_not_allowed",
  "message": "Resource not found or access denied",
  "status": 404,
  "context": {}
}
```
