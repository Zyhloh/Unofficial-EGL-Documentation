## Chat Service - Conversations: Create Conversation

Create a group chat and invite members. Intent `request-create-text-chat-conversation`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>

## Query Parameters
`invite`: `true` <br/>

## Body
```json
{
  "title": "Squad",
  "members": ["b9cd1f0b1b1a4fd7a2f1d1e4c3b2a190"],
  "type": "group"
}
```

---

_Example Response (shape from client)_

```json
{
  "conversationId": "d3c0f4e2-5b7a-4c1e-9f0a-7e2b6c1d8a90",
  "isExisting": false,
  "notInvited": []
}
```
