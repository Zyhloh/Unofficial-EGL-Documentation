## Chat Service - Users: Get User Conversation

One conversation from the user's view. 403 is retried. Intent `request-get-conversation`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/users/:accountId/conversations/:conversationId \
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
`conversationId`: Conversation id <br/>

## Query Parameters
`includeLastMessage`: `true` <br/>

---

_Example Response_ (group, creator's view)

```json
{
  "conversationId": "07c0ExampleGroupId0001",
  "title": "Docs Test",
  "type": "group",
  "createdBy": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "dateCreated": "2026-10-14T22:29:51.034Z",
  "active": true,
  "isActive": true,
  "isReportable": false,
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"],
  "invited": ["94b1569506b04f9f8557af611e8c5e47"],
  "joinedAt": "2026-10-14T22:29:51.132Z",
  "unreadCount": 0,
  "hasMoreUnread": false,
  "lastMessage": {
    "type": "social.chat.v1.NEW_MESSAGE",
    "metadata": {
      "Pub": "<jwt>",
      "Sig": "<base64 ed25519 signature>",
      "TmV": "2"
    },
    "msgId": "07c0ExampleMessageId11",
    "senderId": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
    "createdAt": "2026-10-14T22:29:51.323Z",
    "isReportable": false,
    "message": {
      "body": "<base64 payload>"
    }
  },
  "lastActivityId": "07c0ExampleMessageId10"
}
```

`message.body` decoded:

```json
{"mid":"4a7c1e2d-8b3f-4c6a-9d0e-5f1a2b3c4d5e","sid":"c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60","rid":"07c0ExampleGroupId0001","msg":"hello","tst":1792016991646,"seq":1,"rec":false,"mts":[],"cty":"Persistent"}
```

The client also reads `dateEnded`, `membersJoined`, `inviteTime`, `isInvited`, `inviteReadAt`, `inviter`, `childConversationId` and `lastReadMsgId`; they were absent in this response.
