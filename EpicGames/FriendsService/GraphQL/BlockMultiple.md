## Friends Service - GraphQL: Block Multiple Users

Intent `request-block-multiple-users`.

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
  "variables": { "usersIdsToBlock": ["94b1569506b04f9f8557af611e8c5e47"] }
}
```

Query:

```graphql
mutation blockMultipleUsers($usersIdsToBlock: [String]!) {
  Friends {
    blockMultipleUsers(usersIdsToBlock: $usersIdsToBlock) {
      blockedEntries {
        accountId
        created
        displayName
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
      "blockMultipleUsers": {
        "blockedEntries": [ { "accountId": "94b1569506b04f9f8557af611e8c5e47", "created": "2026-10-14T00:00:00.000Z", "displayName": "Example" } ]
      }
    }
  }
}
```
