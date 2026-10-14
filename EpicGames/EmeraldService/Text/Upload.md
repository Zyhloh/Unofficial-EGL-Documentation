## Emerald Service - Text: Upload Text Chat

Evidence upload for chat reports. The client fetches messages ([Get Messages](../../ChatService/Messages/GetMessages.md) for whole-conversation reports, [Get Reportable Messages](../../ChatService/Messages/GetReportableMessages.md) for single-message reports), uploads them with their signatures, then files a [Compass report](../../CompassService/Reports/SendReport.md) with the returned token. Intent `emerald-text-chat-upload`.

URL: https://emerald-service-live.ecosec.on.epicgames.com/emerald/v1/text/upload \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>

## Body
```json
{
  "msg": [
    {
      "pl": "<message.signingPayload, base64 signed payload>",
      "sg": "<metadata.Sig>",
      "pk": "<metadata.Pub JWT>",
      "ts": 1728864000000,
      "sm": "<decoded message text>",
      "csid": "<msgId>"
    }
  ],
  "pls": [
    { "sid": "b9cd1f0b1b1a4fd7a2f1d1e4c3b2a190", "ndn": "DisplayName" }
  ]
}
```

`pls` lists the conversation members (or the senders in the reportable window) with their Epic display name (`unknown` when missing). `ts` is `Date.parse(createdAt)`.

---

_Example Response (shape from client; only `token` is read)_

```json
{
  "token": "..."
}
```
