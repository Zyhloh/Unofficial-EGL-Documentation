## Data Storage Service - Save Sync: Delete File

Deletes one cloud save file: an old manifest, or a chunk no remaining manifest uses.

URL: https://datastorage-public-service-liveegs.live.use1a.on.epicgames.com/api/v1/data/egstore/savesync/:accountId/:appName/:path \
Method: DELETE \
Auth Required: Yes (Bearer access token, own account)

Note the `data` segment (listing and link requests use `access`).

## Path Parameters
`accountId`: The account id <br/>
`appName`: App name of the game <br/>
`path`: File path inside the game folder, e.g. `manifests/2024.12.30-10.25.20.manifest` or `ChunksV4/00/9EF6137997193143_EB4C91A544215B392DFB44A3DE672520.chunk`

---

_Example Response_

Success, no body. The file is gone from the next [List Files](ListFiles.md).
