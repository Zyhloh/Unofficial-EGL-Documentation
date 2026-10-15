## Launcher Service - Assets: Bulk Sidecars

Returns the "artifact sidecars" (per-artifact config blob + revision) for a list of apps (`src\api\sidecars.rs`, `Download.SidecarsRefreshed`). The sidecar's revision and deployment id are later passed to the game at launch. Only apps that have a sidecar are returned; most titles have none.

URL: https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/bulk/sidecars \
Method: PUT \
Auth Required: Yes (Bearer access token)

The URL is the assets base with its trailing `/v2` removed, plus `/bulk/sidecars`. Despite the method it is a read: it changes nothing.

## Headers
`Content-Type`: application/json <br/>

## Body

A bare JSON array of sidecar keys (`SidecarQuery` / server-side `SidecarKey`):

```json
[
  {
    "namespace": "37baf50c268d47779020d73143bb02b0",
    "catalogItemId": "fbd21ae74fe24bfa972828c85d43bdd1",
    "appName": "Chicken"
  },
  {
    "namespace": "fn",
    "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
    "appName": "Fortnite"
  }
]
```

`namespace`: Catalog namespace (sandbox) <br/>
`catalogItemId`: Catalog item id, required, must be unique within the request <br/>
`appName`: App / artifact name

---

_Example Response_

```json
{
  "data": [
    {
      "config": "{  \"deploymentId\" : \"2bcff9c95ae646b78347e46805b79845\"}",
      "rvn": 1,
      "appName": "Chicken",
      "namespace": "37baf50c268d47779020d73143bb02b0"
    }
  ]
}
```

`config` is a JSON document encoded as a string (seen: `{"deploymentId": "<EOS deployment id>"}`). `rvn` is the sidecar revision. Apps without a sidecar are left out; a request where none has one returns `{"data": []}`.

_Example Response (same catalogItemId twice)_

```json
{
  "errorCode": "errors.com.epicgames.launcher.bad_argument",
  "errorMessage": "Duplicated catalog items detected: SidecarKey{appName='UE_4.8', namespace='ue', catalogItemId='3ddb1bad6e004b99a7192c1a29f2318a'} | SidecarKey{appName='UE_4.4', namespace='ue', catalogItemId='3ddb1bad6e004b99a7192c1a29f2318a'}",
  "messageVars": [
    "SidecarKey{appName='UE_4.8', namespace='ue', catalogItemId='3ddb1bad6e004b99a7192c1a29f2318a'}",
    "SidecarKey{appName='UE_4.4', namespace='ue', catalogItemId='3ddb1bad6e004b99a7192c1a29f2318a'}"
  ],
  "numericErrorCode": 30016,
  "originatingService": "launcher-service",
  "intent": "prod"
}
```

_Example Response (`catalogItemId` missing, shortened)_

```json
{
  "errorCode": "errors.com.epicgames.validation.validation_failed",
  "errorMessage": "Validation Failed. Invalid fields were [arg0[0].catalogItemId]",
  "messageVars": ["[arg0[0].catalogItemId]"],
  "numericErrorCode": 1040,
  "originatingService": "launcher-service",
  "intent": "prod",
  "validationFailures": {
    "arg0[0].catalogItemId": {
      "fieldName": "arg0[0].catalogItemId",
      "errorMessage": "must not be null",
      "errorCode": "javax.validation.constraints.NotNull",
      "invalidValue": "null",
      "messageVars": {}
    }
  }
}
```

A body that is not an array (e.g. `{}` or `{"items": [...]}`) returns 400 `errors.com.epicgames.common.json_mapping_error` (1019).
