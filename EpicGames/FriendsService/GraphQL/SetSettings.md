## Friends Service - GraphQL: Set Privacy Settings

`acceptInvites` is a `FriendInviteType`; the app sends `all`, `none` or `friends_of_friends` (auto-decline toggle sends `none` / `all`). Success is `setSettings.acceptInvites` equal to the sent value.

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
  "variables": { "acceptInvites": "none" }
}
```

Query:

```graphql
mutation setPrivacySettings($acceptInvites: FriendInviteType!) {
  Friends {
    setSettings(data: {acceptInvites: $acceptInvites}) {
      acceptInvites
    }
  }
}
```

---

_Example Response (shape from client)_

```json
{ "data": { "Friends": { "setSettings": { "acceptInvites": "none" } } } }
```
