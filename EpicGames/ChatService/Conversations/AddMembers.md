## Chat Service - Conversations: Add Members

Invite more accounts to a group. Intent `request-add-members-to-conversation`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId/members \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>
`conversationId`: Conversation id <br/>

## Query Parameters
`requestingAccountId`: Your account id <br/>
`invite`: `true` <br/>

## Body
```json
{
  "members": ["b9cd1f0b1b1a4fd7a2f1d1e4c3b2a190"]
}
```

---

_Response body not read (not captured)_
