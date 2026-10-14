## Chat Service - Conversations: Update Conversation Title

Max 64 characters (client rejects longer with `errors.com.epicgames.chat.group_name_too_long`). `null` clears it. Intent `request-update-text-chat-conversation-title`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId \
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

## Query Parameters
`requestingAccountId`: Your account id <br/>

## Body
```json
{
  "title": "New title"
}
```

---

_Example Response_: any 2xx, body ignored
