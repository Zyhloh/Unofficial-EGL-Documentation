## Chat Service - Conversations: Update Invite Status

Accept or reject a group chat invite. Intent `request-update-text-chat-invite-status`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId/invites/:accountId \
Method: PATCH \
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

## Query Parameters
`setMessagesToRead`: `true` / `false` <br/>

## Body
```json
{
  "status": "accepted"
}
```

| Status | Description |
| --- | --- |
| `pending` | Initial state of an invite |
| `accepted` | Join the group |
| `rejected` | Decline the invite |

---

_Example Response_

```json
{}
```

After accepting, the account moves from `invited` to `members` ([Get Members](GetMembers.md)) and the group receives `social.chat.v1.MEMBERS_JOIN`:

```json
{
  "namespace": "_",
  "msgId": "07c0ExampleMessageId23",
  "createdAt": "2026-10-14T22:31:27.827Z",
  "time": 1792017087827,
  "conversationId": "07c0ExampleGroupId0002",
  "type": "group",
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"],
  "isReportable": true
}
```

### Rejecting

Body (EGL sends the same 21 byte body):

```json
{"status":"rejected"}
```

Response 200 `{}`. The rejecter loses access right away; [Get Conversation Metadata](GetConversationMetadata.md) then returns 404:

```json
{
  "messageVars": [],
  "errorMessage": "Conversation 07c0ExampleGroupId0004 in namespace _ not found",
  "errorCode": "errors.com.epicgames.social.chat.conversation_not_found",
  "correlationId": "2d7a9c4e-1b3f-4e8a-9d6c-5f0b1a2e3c4d",
  "numericErrorCode": 40401,
  "responseStatus": 404,
  "intent": "prod",
  "originatingService": "chat-service-api-prod"
}
```

The remaining members receive `social.chat.v1.INVITE_REJECTED` (no `msgId` / `time` in the captured payload):

```json
{
  "namespace": "_",
  "conversationId": "07c0ExampleGroupId0007",
  "type": "group",
  "rejectedBy": "94b1569506b04f9f8557af611e8c5e47",
  "isReportable": true,
  "isActive": true
}
```

A rejection does not deactivate the group while an invite is still pending: after `94b1569506b04f9f8557af611e8c5e47` rejected, the group stayed active with one member and one pending invite:

```json
{
  "conversationId": "07c0ExampleGroupId0007",
  "title": "Docs Reject Me",
  "type": "group",
  "createdBy": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "dateCreated": "2026-10-15T02:01:43.297Z",
  "active": true,
  "isActive": true,
  "isReportable": true,
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"],
  "invited": ["5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b"]
}
```

On a conversation that no longer exists: 404 `errors.com.epicgames.social.chat.conversation_not_found` (see [Leave Conversation](LeaveConversation.md)).
