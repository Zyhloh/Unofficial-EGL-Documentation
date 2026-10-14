## Chat Service - Messages: Send Direct Message

Send a signed whisper to one account. Creates the DM conversation if none exists. Intent `request-send-direct-message`. Text may be passed through the [moderation filter](../../ModerationService/Moderate/ScreenText.md) first. See [Signing](../../../Launcher/Social/Signing.md).

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/dm/:fromAccountId/:toAccountId \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>
`fromAccountId`: Sender account id <br/>
`toAccountId`: Recipient account id <br/>

## Query Parameters
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

`message.body` decoded. `rid` is omitted for the first DM (there is no conversation id yet):

```json
{"mid":"0d4c2b1a-5e6f-4a7b-8c9d-0e1f2a3b4c5d","sid":"c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60","msg":"hello","tst":1792001306342,"seq":1,"rec":false,"mts":[],"cty":"Persistent"}
```

---

_Example Response_ (201, the client only reads `msgId`)

```json
{
  "conversationId": "GBD2ExampleConversationId00001",
  "msgId": "07bzExampleMessageId01",
  "createdAt": "2026-10-14T18:08:25.369Z",
  "isReportable": false
}
```
