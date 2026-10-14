## Chat Service - Messages: Send Message To Conversation

Group / party chat message. Intent `request-send-message-to-conversation`.

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
`sourceMsgId`: Client generated message id <br/>

## Body
```json
{
  "message": { "body": "<base64 signed payload>" },
  "metadata": { "Sig": "...", "Pub": "...", "TmV": "2" },
  "allowedRecipients": ["..."],
  "prohibitedRecipients": ["..."]
}
```

---

_Example Response (shape from client; only `msgId` is read)_

```json
{
  "msgId": "..."
}
```
