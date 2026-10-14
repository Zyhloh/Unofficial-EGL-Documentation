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

On a conversation that no longer exists: 404 `errors.com.epicgames.social.chat.conversation_not_found` (see [Leave Conversation](LeaveConversation.md)).
