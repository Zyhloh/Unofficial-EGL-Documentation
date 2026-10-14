## Friends Service - GraphQL: Get Friend

Single confirmed friend. Called after `friends.v1.FRIENDSHIP_REQUEST` (`ACCEPTED`) and `friends.v1.FRIENDSHIP_ENTRY_UPDATE`.

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
  "variables": { "accountId": "94b1569506b04f9f8557af611e8c5e47", "displayNames": false }
}
```

Query:

```graphql
query friend($displayNames: Boolean, $accountId: String!) {
    Friends {
        friend(friendId: $accountId, displayNames: $displayNames) {
            alias
            account {
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
            }
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
      "friend": { "alias": "Nick", "account": [ {
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
          } ] }
    }
  }
}
```
