## Chat Service - Users: Get DM Conversation

Look up the DM with another account. When the body has no `conversationId` the client treats it as a new DM (still reads `isReportable` / `isActive`). Intent `request-get-dm-conversation`.

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

_Example Response (shape from client)_

```json
{
  "conversationId": "d3c0f4e2-5b7a-4c1e-9f0a-7e2b6c1d8a90",
  "type": "dm",
  "title": "Squad",
  "createdBy": "94b1569506b04f9f8557af611e8c5e47",
  "dateCreated": "2026-10-14T00:00:00.000Z",
  "dateEnded": null,
  "members": ["94b1569506b04f9f8557af611e8c5e47", "b9cd1f0b1b1a4fd7a2f1d1e4c3b2a190"],
  "membersJoined": [],
  "invited": [],
  "inviteTime": null,
  "joinedAt": "2026-10-14T00:00:00.000Z",
  "isReportable": true,
  "isActive": true,
  "isInvited": false,
  "inviteReadAt": null,
  "inviter": null,
  "lastActivityId": "...",
  "childConversationId": null,
  "lastReadMsgId": "...",
  "unreadCount": 0,
  "lastMessage": {
    "msgId": "...",
    "type": "social.chat.v1.NEW_MESSAGE",
    "senderId": "b9cd1f0b1b1a4fd7a2f1d1e4c3b2a190",
    "createdAt": "2026-10-14T00:00:00.000Z",
    "message": { "body": "<base64 signed payload>" },
    "metadata": { "Sig": "...", "Pub": "..." }
  }
}
```
