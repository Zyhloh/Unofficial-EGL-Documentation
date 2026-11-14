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

_Example Response_

```json
{
  "data": {
    "Friends": {
      "friend": {
        "alias": "",
        "account": [
          {
            "id": "94b1569506b04f9f8557af611e8c5e47",
            "displayName": "Example",
            "displayNameType": null,
            "externalAuths": [
              {
                "type": "xbl",
                "externalAuthId": null,
                "externalAuthIdType": "xuid",
                "externalDisplayName": "Example",
                "authIds": []
              }
            ]
          }
        ]
      }
    }
  }
}
```

No alias is `""`. `displayNameType` was `null` for a normal Epic display name. An Xbox link carries its gamertag in `externalDisplayName` but no `externalAuthId` or `authIds` here.
