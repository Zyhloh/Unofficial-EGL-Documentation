## Chat Service - Messages: Get Conversation Messages

Message history, 30 per page. Every non-system message is signature-verified; failures are dropped. Intent `get-conversation-messages`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId/messages \
Method: GET \
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
`limit`: Page size (app uses 30) <br/>
`before`: Message id cursor for older pages <br/>
`after`: Message id cursor for newer pages (inferred from `query.after`) <br/>

---

_Example Response (shape from client)_

```json
{
  "page": [
    {
      "msgId": "...",
      "senderId": "b9cd1f0b1b1a4fd7a2f1d1e4c3b2a190",
      "createdAt": "2026-10-14T00:00:00.000Z",
      "system": false,
      "type": "social.chat.v1.NEW_MESSAGE",
      "message": { "body": "<base64 signed payload>" },
      "metadata": { "Sig": "...", "Pub": "..." }
    },
    { "msgId": "...", "system": true, "type": "social.chat.v1.MEMBERS_JOIN", "createdAt": "2026-10-14T00:00:00.000Z", "payload": {} }
  ],
  "hasNextPage": false
}
```
