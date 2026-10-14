## Friends Service - GraphQL: Add Friend

Send a friend request, or accept an incoming one (same mutation for intents `request-friend` and `accept-friend-request`). `pin` is the parental-control PIN when `require-pin-to-add-friend` is enforced.

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
  "variables": { "friendId": "94b1569506b04f9f8557af611e8c5e47", "pin": null }
}
```

Query:

```graphql
mutation inviteFriendRequest($friendId: String!, $pin: String) {
    Friends {
        invite(friendToInvite: $friendId, pin: $pin) {
            success
        }
    }
}
```

---

_Example Response (shape from client)_

```json
{ "data": { "Friends": { "invite": { "success": true } } } }
```
