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

_Example Response (shortened)_

```json
{
  "cursors": {
    "next": null
  },
  "results": [
    {
      "assetId": "26757664d35f47088139090bd7f73a81",
      "assetNamespace": "89efe5924d3d467c839449ab6ab52e7f",
      "categories": [
        { "id": "923f0caf-2fed-4ab4-94a3-e0a86ff711b0", "name": "Weapons & Combat" }
      ],
      "description": "Military Weapons Dark",
      "listingType": "3D",
      "seller": "Adia Entertainment",
      "distributionMethod": "ASSET_PACK",
      "images": [
        {
          "md5": null,
          "type": "Featured",
          "url": "https://media.fab.com/image_previews/gallery_images/bbd69765-fe30-4223-a803-a50c5d72752b/737e9a16-1287-4860-9c1e-a62bf7deae46.jpg",
          "width": "320",
          "height": "165",
          "uploadedDate": "2024-10-17T10:32:58.854420Z"
        }
      ],
      "projectVersions": [
        {
          "artifactId": "MilitaryWeapDark",
          "engineVersions": ["UE_4.4", "UE_4.27"],
          "targetPlatforms": ["Windows", "Mac"],
          "buildVersions": [
            { "buildVersion": "4.21.0-6954822+++depot+UE4-UserContent-Windows", "platform": "Windows" }
          ]
        }
      ],
      "source": "fab",
      "title": "Military Weapons Dark",
      "url": "https://www.fab.com/listings/480fc7b6-4b4b-42b4-829a-9690b16dcff2",
      "customAttributes": [
        { "ListingIdentifier": "480fc7b6-4b4b-42b4-829a-9690b16dcff2" }
      ],
      "legacyItemId": "0dd1b879a8404e76bcbab8d50eb2acf5"
    }
  ]
}
```

Works with the launcher's normal access token. `cursors.next` is base64 of per-source offsets (`emp=2&fab=2&ues=1`), `null` on the last page. Unreal Engine versions the account owns also appear here (`listingType` `Legacy`, `distributionMethod` `ENGINE`, `source` `uem`, `artifactId` e.g. `UE_4.27Chaos`, `buildVersions` with the engine build). Fab listings have `source` `fab` and a `url`. Values seen: `listingType` `Legacy`, `3D`; `distributionMethod` `ASSET_PACK`, `ENGINE` (the binary also knows `code_plugin`, `complete_project`). `89efe5924d3d467c839449ab6ab52e7f` is the namespace of Fab assets.
