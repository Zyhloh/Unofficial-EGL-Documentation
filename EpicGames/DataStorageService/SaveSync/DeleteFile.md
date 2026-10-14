## Data Storage Service - Save Sync: Delete File

Removes an old manifest or an unused chunk after a successful upload (`CloudSaves.OldManifestDeleteFailed`, `CloudSaves.UnusedChunkDeleteFailed`, `CloudSaves.CleanedUp`).

URL: https://datastorage-public-service-liveegs.live.use1a.on.epicgames.com/api/v1/data/egstore/savesync/:accountId/:path \
Method: DELETE \
Auth Required: Yes (Bearer access token)

## Path Parameters
`accountId`: The account id <br/>
`path`: File path under the account, e.g. `{appName}/manifests/<name>.manifest`

The `data` variant of the path is in the binary next to `access`; that it is used for deletes is inferred from the cleanup log events.
