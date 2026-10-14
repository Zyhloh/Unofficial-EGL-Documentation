## Friends Service - GraphQL: Get Privacy Settings

Who can send friend requests. The app reads the value as a string: `public` maps to `all`, `private` to `none`; `all`, `none`, `friends_of_friends` pass through. Missing value = `all`.

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
  "variables": {}
}
```

Query:

```graphql
query privacySettings {
  Friends {
    settings {
      acceptInvites
    }
  }
}
```

---

_Example Response (shape from client)_

```json
{ "data": { "Friends": { "settings": { "acceptInvites": "all" } } } }
```
