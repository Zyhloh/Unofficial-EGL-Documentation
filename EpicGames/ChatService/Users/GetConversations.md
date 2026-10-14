## Chat Service - Users: Get User Conversations

Conversation list, 20 per page, sorted by activity. `lastMessage` is signature-verified and dropped unless it is a `NEW_MESSAGE`. DM entries whose `members` length is not 2 are ignored. Deactivated party conversations are not listed. 403 is retried. Intent `request-get-user-conversations`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/users/:accountId/conversations \
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

## Query Parameters
`includeLastMessage`: `true` <br/>
`sortBy`: `lastActivity` <br/>
`limit`: Page size (app uses 20) <br/>
`lastActivityBefore`: Pagination cursor, `lastActivityId` of the last row <br/>

---

_Example Response_

```json
{
  "conversations": [
    {
      "conversationId": "GBD2ExampleConversationId00001",
      "type": "dm",
      "createdBy": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
      "dateCreated": "2026-10-14T18:08:25.244Z",
      "active": true,
      "isActive": true,
      "isReportable": false,
      "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60", "94b1569506b04f9f8557af611e8c5e47"],
      "unreadCount": 0,
      "hasMoreUnread": false,
      "lastMessage": {
        "type": "social.chat.v1.NEW_MESSAGE",
        "metadata": {
          "Pub": "<jwt>",
          "Sig": "<base64 ed25519 signature>",
          "TmV": "2"
        },
        "msgId": "07bzExampleMessageId01",
        "senderId": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
        "createdAt": "2026-10-14T18:08:25.369Z",
        "isReportable": false,
        "message": {
          "body": "<base64 payload>"
        }
      },
      "lastActivityId": "07bzExampleMessageId01"
    }
  ]
}
```

With no conversations: `{"conversations":[]}`.

A group entry in this list was not captured; [Get User Conversation](GetConversation.md) has a captured group object (`title`, `invited`, `joinedAt`).
