## Chat Service - Users: Get DM Conversation

Look up the DM with another account. Before the first message there is no conversation and the body has no `conversationId`; the client then treats it as a new DM (still reads `isReportable` / `isActive`) and sends the first message with [Send Direct Message](../Messages/SendDirectMessage.md). Intent `request-get-dm-conversation`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/users/:accountId/conversations/dm/:toAccountId \
Method: GET \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>
`accountId`: Your account id <br/>
`toAccountId`: Other account id <br/>

## Query Parameters
`includeLastMessage`: `true` <br/>

---

_Example Response (no DM yet)_

```json
{
  "type": "dm",
  "active": true,
  "isActive": true,
  "isReportable": false
}
```

_Example Response_

```json
{
  "conversationId": "GBD2ExampleConversationId00001",
  "type": "dm",
  "createdBy": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "dateCreated": "2026-10-14T18:08:25.244Z",
  "active": true,
  "isActive": true,
  "isReportable": false,
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60", "94b1569506b04f9f8557af611e8c5e47"],
  "unreadCount": 1,
  "hasMoreUnread": false,
  "lastMessage": {
    "type": "social.chat.v1.NEW_MESSAGE",
    "metadata": {
      "Pub": "<jwt>",
      "Sig": "<base64 ed25519 signature>",
      "TmV": "2"
    },
    "msgId": "07c0ExampleMessageId04",
    "senderId": "94b1569506b04f9f8557af611e8c5e47",
    "createdAt": "2026-10-14T22:05:43.889Z",
    "isReportable": false,
    "message": {
      "body": "<base64 payload>"
    }
  },
  "lastActivityId": "07c0ExampleMessageId04"
}
```
