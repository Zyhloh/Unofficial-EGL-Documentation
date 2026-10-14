## Chat Service - Users: Update Last Read Message

Mark a conversation read up to a message. Intent `request-update-conversation-last-read-msg-id`. The launcher is also told via the `conversation-read` bridge notification.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/users/:accountId/conversations/:conversationId \
Method: PATCH \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>
`accountId`: Your account id <br/>
`conversationId`: Conversation id <br/>

## Body
```json
{
  "msgId": "07c0ExampleMessageId11"
}
```

---

_Example Response_

```json
{}
```

Event `social.chat.v1.MESSAGE_READ` to your own connections:

```json
{
  "namespace": "_",
  "time": 1792016991662,
  "conversationId": "07c0ExampleGroupId0001",
  "lastReadMessageId": "07c0ExampleMessageId11",
  "totalUnreadMessages": 1,
  "hasMoreUnreadMessages": false
}
```
