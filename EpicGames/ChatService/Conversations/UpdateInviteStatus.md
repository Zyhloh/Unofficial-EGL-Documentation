## Chat Service - Conversations: Update Invite Status

Accept / reject / mark-read a group chat invite. Intent `request-update-text-chat-invite-status`. Status values are not enumerated in the client bundle.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId/invites/:accountId \
Method: PATCH \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>
`conversationId`: Conversation id <br/>
`accountId`: Your account id <br/>

## Query Parameters
`setMessagesToRead`: `true` / `false` <br/>

## Body
```json
{
  "status": "<invite status>"
}
```

---

_Response body returned to caller (not captured)_
