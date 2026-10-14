## Chat Service - Messages: Get Reportable Messages

Context window around a reported message; the result is uploaded to [Emerald](../../EmeraldService/Text/Upload.md). Intent `get-conversation-reportable-messages`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId/reportable-messages \
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
`reportedMessageId`: Message being reported <br/>
`contextWindowSize`: Optional, app default 25 <br/>

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
    }
  ]
}
```
