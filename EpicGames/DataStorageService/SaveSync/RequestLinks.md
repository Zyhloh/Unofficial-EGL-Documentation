## Data Storage Service - Save Sync: Request Links

Asks for signed write (and read) links for a set of files before an upload (`signed link request`, `CloudSaves.Probe.LinksSigned`). Request body struct `AccessBody`.

URL: https://datastorage-public-service-liveegs.live.use1a.on.epicgames.com/api/v1/access/egstore/savesync/:accountId/:path \
Method: POST \
Auth Required: Yes (Bearer access token)

## Headers
`Content-Type`: application/json <br/>

## Path Parameters
`accountId`: The account id <br/>
`path`: `{appName}/`

## Body
```json
{
  "files": [
    "manifests/94b1569506b04f9f8557af611e8c5e47.manifest",
    "Chunks/0000000000000000.chunk"
  ]
}
```

Method and body key are inferred (struct `AccessBody` and field `files` exist; same contract as the UE launcher's savesync). Response is an [AccessListing](ListFiles.md). Files are then uploaded with a PUT to each `writeLink`.
