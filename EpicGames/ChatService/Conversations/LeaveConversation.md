## Chat Service - Conversations: Leave Conversation

Intent `request-leave-text-chat-conversation`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId/members/:accountId \
Method: DELETE \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>
`conversationId`: Conversation id <br/>
`accountId`: Your account id <br/>

---

_Example Response_: 204 No Content

After leaving, requests from that account on the conversation (metadata, messages, invites, leaving again) return 404:

```json
{
  "messageVars": [],
  "errorMessage": "Conversation 07c0ExampleGroupId0001 in namespace _ not found",
  "errorCode": "errors.com.epicgames.social.chat.conversation_not_found",
  "correlationId": "8e4c2a1b-3d5f-4a7b-9c0d-2e1f3a4b5c6d",
  "numericErrorCode": 40401,
  "responseStatus": 404,
  "intent": "prod",
  "originatingService": "chat-service-api-prod"
}
```
