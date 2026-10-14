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

_Example Response_ (group with `isReportable: true`)

Only `NEW_MESSAGE` entries, oldest first (the reverse of [Get Messages](GetMessages.md)); system entries are left out.

```json
{
  "page": [
    {
      "type": "social.chat.v1.NEW_MESSAGE",
      "metadata": {
        "Pub": "<jwt>",
        "Sig": "<base64 ed25519 signature>",
        "TmV": "2"
      },
      "msgId": "07c0ExampleMessageId25",
      "senderId": "94b1569506b04f9f8557af611e8c5e47",
      "createdAt": "2026-10-14T22:31:32.281Z",
      "isReportable": true,
      "message": {
        "body": "<base64 payload>"
      }
    },
    {
      "type": "social.chat.v1.NEW_MESSAGE",
      "metadata": {
        "Pub": "<jwt>",
        "Sig": "<base64 ed25519 signature>",
        "TmV": "2"
      },
      "msgId": "07c0ExampleMessageId26",
      "senderId": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
      "createdAt": "2026-10-14T22:31:35.66Z",
      "isReportable": true,
      "message": {
        "body": "<base64 payload>"
      }
    }
  ],
  "hasNextPage": false
}
```

_Example Response_ (DM with `isReportable: false`)

```json
{
  "page": [],
  "hasNextPage": false
}
```
