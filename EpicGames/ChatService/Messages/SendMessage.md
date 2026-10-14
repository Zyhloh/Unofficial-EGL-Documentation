## Chat Service - Messages: Send Message To Conversation

Message to an existing conversation (DM, group or party). Intent `request-send-message-to-conversation`. See [Signing](../../../Launcher/Social/Signing.md).

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId/messages \
Method: POST \
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
`fromAccountId`: Sender account id <br/>
`sourceMsgId`: Client generated UUID v4, also the signed payload `mid` <br/>

## Body
```json
{
  "message": {
    "body": "<base64 payload>"
  },
  "metadata": {
    "Sig": "<base64 ed25519 signature>",
    "Pub": "<jwt>",
    "TmV": "2"
  }
}
```

`message.body` decoded, `rid` is the conversation id:

```json
{"mid":"1e5d3c2b-6f70-4b8c-9dae-1f2a3b4c5d6e","sid":"c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60","rid":"GBD2ExampleConversationId00001","msg":"hello","tst":1792001306956,"seq":1,"rec":false,"mts":[],"cty":"Persistent"}
```

The overlay can also add `allowedRecipients` / `prohibitedRecipients` (arrays of account ids) to the body; not captured.

---

_Example Response_ (201, the client only reads `msgId`)

```json
{
  "conversationId": "GBD2ExampleConversationId00001",
  "msgId": "07bzExampleMessageId02",
  "createdAt": "2026-10-14T18:08:25.783Z",
  "isReportable": false
}
```
