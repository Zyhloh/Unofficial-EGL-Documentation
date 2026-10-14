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

_Response not read by the client beyond being returned to callers (not captured)_
