## Chat Service - Conversations: Get Conversation Metadata

Used for group metadata (`invited`, `members`, `title`) and party chat (`metadata.partyId`). Intents `request-group-conversation-metadata`, `request-conversation-metadata`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId \
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

_Example Response (shape from client)_

```json
{
  "conversationId": "d3c0f4e2-5b7a-4c1e-9f0a-7e2b6c1d8a90",
  "title": "Squad",
  "members": ["94b1569506b04f9f8557af611e8c5e47"],
  "invited": [],
  "metadata": { "partyId": "..." }
}
```
