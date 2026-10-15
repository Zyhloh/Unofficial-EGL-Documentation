## Chat Service - Conversations: Add Members

Invite more accounts to a group. Intent `request-add-members-to-conversation`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations/:conversationId/members \
Method: POST \
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
`requestingAccountId`: Your account id <br/>
`invite`: `true` <br/>

## Body
```json
{
  "members": ["5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b"]
}
```

---

_Example Response_

```json
{
  "invited": ["5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b"],
  "notInvited": []
}
```

The invited account in this capture was a friend of another group member, not of the inviter; it was invited without error.

Event `social.chat.v1.NEW_INVITE` to the group:

```json
{
  "namespace": "_",
  "msgId": "07c0ExampleMessageId16",
  "createdAt": "2026-10-14T22:30:18.097Z",
  "time": 1792017018097,
  "conversationId": "07c0ExampleGroupId0001",
  "type": "group",
  "createdBy": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60", "94b1569506b04f9f8557af611e8c5e47"],
  "title": "Docs Test Renamed",
  "isReportable": true,
  "inviter": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "invited": ["5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b"],
  "inviteTime": "2026-10-14T22:30:18.05Z",
  "conversationCreatedAt": "2026-10-14T22:29:51.034Z",
  "isActive": true
}
```

`isReportable` was `false` while the group had one member and `true` in this event (two members). How the initial value is set: [Create Conversation](CreateConversation.md#isreportable).
