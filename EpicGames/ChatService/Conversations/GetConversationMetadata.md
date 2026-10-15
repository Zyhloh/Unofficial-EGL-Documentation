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

_Example Response (DM)_

```json
{
  "conversationId": "GBD2ExampleConversationId00001",
  "type": "dm",
  "createdBy": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "dateCreated": "2026-10-14T18:08:25.244Z",
  "active": true,
  "isActive": true,
  "isReportable": false,
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60", "94b1569506b04f9f8557af611e8c5e47"]
}
```

_Example Response (group)_

```json
{
  "conversationId": "07c0ExampleGroupId0001",
  "title": "Docs Test",
  "type": "group",
  "createdBy": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "dateCreated": "2026-10-14T22:29:51.034Z",
  "active": true,
  "isActive": true,
  "isReportable": false,
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"],
  "invited": ["94b1569506b04f9f8557af611e8c5e47"]
}
```

_Example Response (deactivated group)_

After the only other member left ([Leave Conversation](LeaveConversation.md#events)):

```json
{
  "conversationId": "07c0ExampleGroupId0003",
  "title": "Docs Reject Test",
  "type": "group",
  "createdBy": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "dateCreated": "2026-10-14T22:52:13.936Z",
  "active": false,
  "isActive": false,
  "inactiveReason": "insufficient_members",
  "isReportable": false,
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"]
}
```

_Example Response (invitee, before accepting)_

```json
{
  "conversationId": "07c0ExampleGroupId0004",
  "type": "group",
  "createdBy": "94b1569506b04f9f8557af611e8c5e47",
  "dateCreated": "2026-10-14T22:52:28.378Z",
  "active": true,
  "isActive": true,
  "members": ["94b1569506b04f9f8557af611e8c5e47"],
  "invited": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60", "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b"]
}
```

After rejecting the invite the same request returns 404 `conversation_not_found` ([Update Invite Status](UpdateInviteStatus.md#rejecting)).

An invited account can read the metadata before accepting. A group created from EGL, read by an invitee before accepting, returned neither `title` nor `isReportable` (same in the example above, created by the other account without a title). Party conversations return `metadata.partyId` (read by the client; not captured).
