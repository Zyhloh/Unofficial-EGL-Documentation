## Chat Service - Messages: Get Conversation Messages

Message history, 30 per page, newest first. Every non-system message is signature-verified; failures are dropped. Intent `get-conversation-messages`.

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

_Example Response_

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
      "msgId": "07c0ExampleMessageId04",
      "senderId": "94b1569506b04f9f8557af611e8c5e47",
      "createdAt": "2026-10-14T22:05:43.889Z",
      "isReportable": false,
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
      "msgId": "07bzExampleMessageId02",
      "senderId": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
      "createdAt": "2026-10-14T18:08:25.783Z",
      "isReportable": false,
      "message": {
        "body": "<base64 payload>"
      }
    },
    {
      "type": "social.chat.v1.REPORTABILITY_CHANGE",
      "system": true,
      "msgId": "07bzExampleMessageId03",
      "createdAt": "2026-10-14T18:08:25.337Z",
      "payload": {
        "isReportable": false
      }
    }
  ],
  "hasNextPage": false
}
```

`message.body` of the first entry decoded (sent by EGL):

```json
{"mid":"2f6e4d3c-7081-4c9d-aebf-2a3b4c5d6e7f","sid":"94b1569506b04f9f8557af611e8c5e47","rid":"GBD2ExampleConversationId00001","msg":"hello","tst":1792015544211,"seq":1,"rec":false,"mts":[],"cty":"Persistent"}
```

A new DM starts with a `REPORTABILITY_CHANGE` system entry. Other system types (e.g. `social.chat.v1.MEMBERS_JOIN`) use the same `system` / `payload` layout; not captured.
