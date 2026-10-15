## Data Storage Service - Save Sync: Request Links

Returns signed S3 write (and read) links for files that are about to be uploaded. The links are then used with a plain `PUT` of the file bytes.

URL: https://datastorage-public-service-liveegs.live.use1a.on.epicgames.com/api/v1/access/egstore/savesync/:accountId/:appName/ \
Method: POST \
Auth Required: Yes (Bearer access token, own account)

## Headers
`Content-Type`: application/json <br/>

## Path Parameters
`accountId`: The account id <br/>
`appName`: App name of the game, with the trailing slash

## Body
```json
{
  "files": [
    "ChunksV4/54/C77D6244688E8608_E761F7D5C0944F0FBFBC565AABC3ECB9.chunk",
    "manifests/2026.10.15-12.19.04.manifest"
  ]
}
```

`files`: Paths relative to the game folder

---

_Example Response_

```json
{
  "files": {
    "ChunksV4/54/C77D6244688E8608_E761F7D5C0944F0FBFBC565AABC3ECB9.chunk": {
      "readLink": "https://eos-cloudsaves-live.s3.amazonaws.com/savesync/94b1569506b04f9f8557af611e8c5e47/24b4ee8b16e4450184fe33ff871cc0ee/ChunksV4/54/...",
      "writeLink": "https://eos-cloudsaves-live.s3.amazonaws.com/savesync/94b1569506b04f9f8557af611e8c5e47/24b4ee8b16e4450184fe33ff871cc0ee/ChunksV4/54/...",
      "hash": null,
      "lastModified": null,
      "size": 0,
      "fileLocked": false
    },
    "manifests/2026.10.15-12.19.04.manifest": {
      "readLink": "https://eos-cloudsaves-live.s3.amazonaws.com/...",
      "writeLink": "https://eos-cloudsaves-live.s3.amazonaws.com/...",
      "hash": null,
      "lastModified": null,
      "size": 0,
      "fileLocked": false
    }
  },
  "folderThrottled": false,
  "maxFileSizeBytes": -1,
  "maxFolderSizeBytes": -1,
  "expiresAt": "2026-10-15T12:35:26.802Z"
}
```

Unlike [List Files](ListFiles.md), the keys here are the relative paths from the request. Asking for links creates nothing: a file only appears in the listing after its `PUT` succeeds.
