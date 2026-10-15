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

### Events

The remaining members receive `social.chat.v1.MEMBERS_LEFT` (`members` = the leaver):

```json
{
  "namespace": "_",
  "msgId": "07c0ExampleMessageId27",
  "createdAt": "2026-10-14T22:52:57.609Z",
  "time": 1792018377609,
  "conversationId": "07c0ExampleGroupId0003",
  "type": "group",
  "members": ["94b1569506b04f9f8557af611e8c5e47"],
  "isReportable": false
}
```

| Group after the leave | Result |
| --- | --- |
| 2+ members | Stays active |
| 1 member, invite still pending | Stays active |
| 1 member, no pending invite | Deactivated: `social.chat.v1.CONVERSATION_DEACTIVATED`, metadata returns `active: false`, `inactiveReason: "insufficient_members"` ([Get Conversation Metadata](GetConversationMetadata.md)) |
| 0 members (last member left, also with invites pending) | Deleted: `social.chat.v1.CONVERSATION_DELETED` |

`CONVERSATION_DEACTIVATED` (sent right after `MEMBERS_LEFT`):

```json
{
  "namespace": "_",
  "conversationId": "07c0ExampleGroupId0003",
  "isReportable": false,
  "inactiveReason": "insufficient_members"
}
```

The remaining member of a deactivated group can still leave (204).

`CONVERSATION_DELETED` (the last member left a group that still had a pending invite):

```json
{
  "namespace": "_",
  "conversationId": "07c0ExampleGroupId0005"
}
```
