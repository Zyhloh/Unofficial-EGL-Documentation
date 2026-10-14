## Chat Service - Conversations: Update Conversation Title

Max 64 characters (client rejects longer with `errors.com.epicgames.chat.group_name_too_long`). `null` clears it. Intent `request-update-text-chat-conversation-title`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId \
Method: PATCH \
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

## Body
```json
{
  "title": "Docs Test Renamed"
}
```

---

_Example Response_: 200 with an empty body

Event `social.chat.v1.TITLE_CHANGE` to the group:

```json
{
  "namespace": "_",
  "msgId": "07c0ExampleMessageId14",
  "createdAt": "2026-10-14T22:29:51.575Z",
  "time": 1792016991575,
  "conversationId": "07c0ExampleGroupId0001",
  "accountId": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "title": "Docs Test Renamed",
  "previousTitle": "Docs Test",
  "isReportable": false
}
```

The change is also kept in the history as a `TITLE_CHANGE` system entry ([Get Messages](../Messages/GetMessages.md)).
