## Friends Service - GraphQL: Get Friends

Full friends summary. Used by the `FriendsDataProvider` on start and on reinitialize. Entries without `account[0]` are dropped; `incoming` carries `created`.

URL: https://api.epicgames.dev/overlay-graphql/v1/graphql \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`Authorization`: Bearer {token} <br/>

## Body
```json
{
  "query": "<query below>",
  "variables": { "displayNames": false }
}
```

Query:

```graphql
query friends($displayNames: Boolean) {
    Friends {
        summary(displayNames: $displayNames) {
            friends { alias account {
                id
                displayName
                displayNameType
                externalAuths {
                    type
                    externalAuthId
                    externalAuthIdType
                    externalDisplayName
                    authIds { id type }
                }
            } }
            incoming { alias account {
                id
                displayName
                displayNameType
                externalAuths {
                    type
                    externalAuthId
                    externalAuthIdType
                    externalDisplayName
                    authIds { id type }
                }
            } created }
            outgoing { alias account {
                id
                displayName
                displayNameType
                externalAuths {
                    type
                    externalAuthId
                    externalAuthIdType
                    externalDisplayName
                    authIds { id type }
                }
            } }
            blocklist { alias account {
                id
                displayName
                displayNameType
                externalAuths {
                    type
                    externalAuthId
                    externalAuthIdType
                    externalDisplayName
                    authIds { id type }
                }
            } }
        }
    }
}
```

---

_Example Response (shape from client)_

```json
{
  "data": {
    "Friends": {
      "summary": {
        "friends": [ { "alias": null, "account": [ {
            "id": "94b1569506b04f9f8557af611e8c5e47",
            "displayName": "Example",
            "displayNameType": "<type, HIDDEN = de-identified>",
            "externalAuths": [
              {
                "type": "steam",
                "externalAuthId": "76561190000000000",
                "externalAuthIdType": "<idType>",
                "externalDisplayName": "Example",
                "authIds": [{ "id": "76561190000000000", "type": "<idType>" }]
              }
            ]
          } ] } ],
        "incoming": [ { "alias": null, "account": [], "created": "2026-10-14T00:00:00.000Z" } ],
        "outgoing": [],
        "blocklist": []
      }
    }
  }
}
```
