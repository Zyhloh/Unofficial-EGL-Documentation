## Epic Games Store - GraphQL: Get Media Ref

Resolves a store trailer media ref id to video URLs. Used by `get_store_product_art` for library hero trailers.

URL: https://store.epicgames.com/graphql \
Method: POST \
Auth Required: No

## Headers
`Content-Type`: application/json <br/>
`User-Agent`: EpicGamesLauncher/2 (+https://store.epicgames.com) <br/>

## Body
```json
{
  "query": "query getVideo($mediaRefId: String!) { Media { getMediaRef(mediaRefId: $mediaRefId) { outputs { url key contentType } } } }",
  "variables": {
    "mediaRefId": "94b1569506b04f9f8557af611e8c5e47"
  }
}
```

---

_Example Response (shape from client)_

```json
{
  "data": {
    "Media": {
      "getMediaRef": {
        "outputs": [
          {
            "url": "https://...",
            "key": "...",
            "contentType": "video/mp4"
          }
        ]
      }
    }
  }
}
```

The client reads `/data/Media/getMediaRef/outputs`; an empty list is `Media ref returned no outputs`.
