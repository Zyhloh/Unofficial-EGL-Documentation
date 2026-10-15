## Emerald Service - Text: Upload Text Chat

Evidence upload for chat reports. The client fetches messages ([Get Messages](../../ChatService/Messages/GetMessages.md) for whole-conversation reports, [Get Reportable Messages](../../ChatService/Messages/GetReportableMessages.md) for single-message reports), uploads them with their signatures, then files a [Compass report](../../CompassService/Reports/SendReport.md) with the returned token. Intent `emerald-text-chat-upload`.

URL: https://emerald-service-live.ecosec.on.epicgames.com/emerald/v1/text/upload \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>

No `X-Epic-Agent` / `X-EPIC-CORRELATION-ID` (unlike the other overlay requests). Sent from the overlay webview (`Origin: https://api.epicgames.dev`).

## Body
Captured from EGL reporting a group chat (one message from `c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60`, reported by `94b1569506b04f9f8557af611e8c5e47`):

```json
{
  "msg": [
    {
      "pl": "<base64 payload>",
      "sg": "<base64 ed25519 signature>",
      "pk": "<jwt>",
      "ts": 1792029903690,
      "sm": "hello",
      "csid": "07c0ExampleMessageId28"
    }
  ],
  "pls": [
    { "sid": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60", "ndn": "ExampleAlt" },
    { "sid": "94b1569506b04f9f8557af611e8c5e47", "ndn": "ExampleUser" }
  ]
}
```

| Field | Value |
| --- | --- |
| `msg[].pl` | The message `body` as stored by the Chat Service (base64 signed payload, see [Signing](../../../Launcher/Social/Signing.md)). Decoded payload of the captured message (ids and text replaced): `{"mid":"6b1e2c3d-4f5a-4b6c-9d7e-8f0a1b2c3d4e","sid":"c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60","rid":"07c0ExampleGroupId0008","msg":"hello","tst":1792029904168,"seq":1,"rec":false,"mts":[],"cty":"Persistent"}` |
| `msg[].sg` | `metadata.Sig` |
| `msg[].pk` | `metadata.Pub` (public key JWT) |
| `msg[].ts` | `Date.parse(createdAt)` of the chat message (server time, not the payload `tst`) |
| `msg[].sm` | Decoded message text |
| `msg[].csid` | Chat `msgId` |
| `pls[]` | Conversation members: `sid` account id, `ndn` Epic display name (`unknown` when missing) |

---

_Example Response_

```json
{
  "token": "3e7b1c9d-5a2f-4d8e-b6c0-1f4a7e9d2b3c"
}
```

The token is a UUID, passed as `emerald_token` to [Send Report](../../CompassService/Reports/SendReport.md). Reporting the same conversation again uploads the same body and gets a new token.
