## Chat Service - Messages: Send Direct Message

Send a signed whisper to one account. Intent `request-send-direct-message`. Text may be passed through the [moderation filter](../../ModerationService/Moderate/ScreenText.md) first. See [Signing](../../../Launcher/Social/Signing.md).

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
`sourceMsgId`: Client generated message id, also the signed payload `mid` <br/>

## Body
```json
{
  "message": { "body": "<base64 signed payload>" },
  "metadata": { "Sig": "<base64 ed25519 signature>", "Pub": "<public key JWT>", "TmV": "2" }
}
```

---

_Example Response (shape from client; only `msgId` is read)_

```json
{
  "msgId": "...",
  "conversationId": "d3c0f4e2-5b7a-4c1e-9f0a-7e2b6c1d8a90"
}
```
