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

A new DM starts with a `REPORTABILITY_CHANGE` system entry.

_Example Response (group)_

System entries for invites, joins and title changes sit between the messages.

```json
{
  "page": [
    {
      "type": "social.chat.v1.MEMBERS_JOIN",
      "system": true,
      "msgId": "07c0ExampleMessageId15",
      "createdAt": "2026-10-14T22:29:57.732Z",
      "payload": {
        "members": ["94b1569506b04f9f8557af611e8c5e47"],
        "isReportable": false
      }
    },
    {
      "type": "social.chat.v1.TITLE_CHANGE",
      "system": true,
      "msgId": "07c0ExampleMessageId14",
      "createdAt": "2026-10-14T22:29:51.575Z",
      "payload": {
        "accountId": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
        "title": "Docs Test Renamed",
        "previousTitle": "Docs Test",
        "isReportable": false
      }
    },
    {
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
    {
      "type": "social.chat.v1.REPORTABILITY_CHANGE",
      "system": true,
      "msgId": "07c0ExampleMessageId13",
      "createdAt": "2026-10-14T22:29:51.197Z",
      "payload": {
        "isReportable": false
      }
    },
    {
      "type": "social.chat.v1.NEW_INVITE",
      "system": true,
      "msgId": "07c0ExampleMessageId12",
      "createdAt": "2026-10-14T22:29:51.173Z",
      "payload": {
        "isReportable": false,
        "inviter": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
        "invited": ["94b1569506b04f9f8557af611e8c5e47"]
      }
    }
  ],
  "hasNextPage": false
}
```

| System type | `payload` |
| --- | --- |
| `social.chat.v1.NEW_INVITE` | `isReportable`, `inviter`, `invited` |
| `social.chat.v1.REPORTABILITY_CHANGE` | `isReportable` |
| `social.chat.v1.MEMBERS_JOIN` | `members`, `isReportable` |
| `social.chat.v1.TITLE_CHANGE` | `accountId`, `title`, `previousTitle`, `isReportable` |

After the requesting account has left the group: 404 `errors.com.epicgames.social.chat.conversation_not_found` ([Leave Conversation](../Conversations/LeaveConversation.md)).
