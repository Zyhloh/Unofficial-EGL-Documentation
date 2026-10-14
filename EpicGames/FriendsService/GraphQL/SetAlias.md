## Friends Service - GraphQL: Set Alias

Set a friend nickname (intent `request-alias-friend`).

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
  "variables": { "friendId": "94b1569506b04f9f8557af611e8c5e47", "alias": "Nick" }
}
```

Query:

```graphql
mutation setAlias($friendId: String!, $alias: String!) {
  Friends {
    setAlias(alias: $alias, friendId: $friendId) {
      success
    }
  }
}
```

---

_Example Response (shape from client)_

```json
{ "data": { "Friends": { "setAlias": { "success": true } } } }
```
