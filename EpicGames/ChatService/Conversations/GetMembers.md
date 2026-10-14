## Chat Service - Conversations: Get Conversation Members

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId/members \
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
`accountId`: Your account id <br/>

---

_Example Response_

```json
{
  "conversationId": "GBD2ExampleConversationId00001",
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60", "94b1569506b04f9f8557af611e8c5e47"]
}
```
