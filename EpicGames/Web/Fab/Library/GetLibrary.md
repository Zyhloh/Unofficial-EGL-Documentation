## Fab - Library: Get Library

Paged Fab library of the account (UE assets / plugins). Walked by `eglv2_lib::api::fab` (`Fab.LibraryPageReceived`, `Fab.LibraryWalkCompleted`, `Fab.LibraryPageCapReached`, `Fab.LibraryCursorRepeated`) for the Library tab and for Fab install updates (`download::fab_update`).

URL: https://www.fab.com/e/accounts/:accountId/ue/library \
Method: GET \
Auth Required: Yes (Bearer access token)

## Headers
`Accept-Language`: UI locale <br/>

## Path Parameters
`accountId`: The account id

## Query Parameters
`count`: Page size <br/>
`cursor`: `cursors.next` of the previous page <br/>

---

_Example Response (shape from client, `FabLibraryPage` / `FabAsset` / `FabProjectVersion`)_

```json
{
  "results": [
    {
      "assetID": "94b1569506b04f9f8557af611e8c5e47",
      "assetNamespace": "89efe5924d3d467c839449ab6ab52e7f",
      "distributionMethod": "ASSET_PACK",
      "legacyItemId": "94b1569506b04f9f8557af611e8c5e47",
      "projectVersions": [
        {
          "artifactID": "...",
          "engineVersions": ["UE_5.6"],
          "targetPlatforms": ["Windows"],
          "buildVersions": []
        }
      ]
    }
  ],
  "cursors": {
    "next": "..."
  }
}
```

Values are placeholders. `89efe5924d3d467c839449ab6ab52e7f` is the namespace constant the importer uses for Fab items; distribution methods seen in the binary: `code_plugin`, `complete_project`, `asset_pack`.
