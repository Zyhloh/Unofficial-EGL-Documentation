# Hosts

This are some (not all) Hosts that you can access the Chat Service from

- api.epicgames.dev (`/epic/chat`)

<br/>

Recommended Hosts:

- api.epicgames.dev

All paths are prefixed with `/epic/chat`. Conversation and message ids are opaque base62 strings, not UUIDs. Conversation `type` values seen: `dm`, `group`, `epic_party`. Realtime events: `social.chat.v1.*` over [Epic Connect](../../Launcher/Social/Connect.md). Message bodies are signed, see [Signing](../../Launcher/Social/Signing.md).

## Realtime events

Pushed over [Epic Connect](../../Launcher/Social/Connect.md) inside the standard envelope (`correlationId`, `timestamp`, `id`, `connectionId`, `payload`, `type`). Payload fields as captured live (2026-10-14); every payload also carries `namespace: "_"`.

| Type | Trigger | Payload |
| --- | --- | --- |
| `social.chat.v1.CONVERSATION_CREATED` | [Create Conversation](Conversations/CreateConversation.md), sent to the creator and invitees | `conversationId`, `type`, `members`, `isReportable`, `inviter`, `invited`, `dateCreated`, `isActive` |
| `social.chat.v1.NEW_INVITE` | Create Conversation, [Add Members](Conversations/AddMembers.md) | `msgId`, `createdAt`, `time`, `conversationId`, `type`, `createdBy`, `members`, `title` (when set), `isReportable`, `inviter`, `invited`, `inviteTime`, `conversationCreatedAt`, `isActive` |
| `social.chat.v1.REPORTABILITY_CHANGE` | Conversation created | `msgId`, `createdAt`, `time`, `conversationId`, `conversationType`, `isReportable` |
| `social.chat.v1.NEW_MESSAGE` | [Send Message](Messages/SendMessage.md) | `conversation.{conversationId,type}`, `message.{body,senderId,msgId,createdAt,time,metadata,isReportable,sourceMsgId}` |
| `social.chat.v1.TITLE_CHANGE` | [Update Title](Conversations/UpdateTitle.md) | `msgId`, `createdAt`, `time`, `conversationId`, `accountId`, `title`, `previousTitle`, `isReportable` |
| `social.chat.v1.MESSAGE_READ` | [Update Last Read](Users/UpdateLastRead.md) | `time`, `conversationId`, `lastReadMessageId`, `totalUnreadMessages`, `hasMoreUnreadMessages` |
| `social.chat.v1.MEMBERS_JOIN` | [Update Invite Status](Conversations/UpdateInviteStatus.md) `accepted` | `msgId`, `createdAt`, `time`, `conversationId`, `type`, `members` (the joining accounts), `isReportable` |
| `social.chat.v1.INVITE_REJECTED` | [Update Invite Status](Conversations/UpdateInviteStatus.md#rejecting) `rejected`, sent to the remaining members | `conversationId`, `type`, `rejectedBy`, `isReportable`, `isActive` |
| `social.chat.v1.MEMBERS_LEFT` | [Leave Conversation](Conversations/LeaveConversation.md#events) | `msgId`, `createdAt`, `time`, `conversationId`, `type`, `members` (the leaver), `isReportable` |
| `social.chat.v1.CONVERSATION_DEACTIVATED` | Group drops to 1 member with no pending invite | `conversationId`, `isReportable`, `inactiveReason` (`insufficient_members`) |
| `social.chat.v1.CONVERSATION_DELETED` | Last member leaves (also with invites pending) | `conversationId` |

The realtime `NEW_MESSAGE` is nested, unlike the flat history entries of [Get Messages](Messages/GetMessages.md):

```json
{
  "namespace": "_",
  "conversation": {
    "conversationId": "07c0ExampleGroupId0002",
    "type": "group"
  },
  "message": {
    "body": "<base64 payload>",
    "senderId": "94b1569506b04f9f8557af611e8c5e47",
    "msgId": "07c0ExampleMessageId25",
    "createdAt": "2026-10-14T22:31:32.281Z",
    "time": 1792017092281,
    "metadata": {
      "Sig": "<base64 ed25519 signature>",
      "Pub": "<jwt>",
      "TmV": "2"
    },
    "isReportable": true,
    "sourceMsgId": "3c8e1f4a-6b2d-4e9a-8f7c-0d1e2a3b4c5d"
  }
}
```

`CONVERSATION_CREATED` example:

```json
{
  "namespace": "_",
  "conversationId": "07c0ExampleGroupId0002",
  "type": "group",
  "members": ["94b1569506b04f9f8557af611e8c5e47"],
  "isReportable": true,
  "inviter": "94b1569506b04f9f8557af611e8c5e47",
  "invited": ["5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b", "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"],
  "dateCreated": "2026-10-14T22:31:27.477Z",
  "isActive": true
}
```

`REPORTABILITY_CHANGE` example:

```json
{
  "namespace": "_",
  "msgId": "07c0ExampleMessageId22",
  "createdAt": "2026-10-14T22:31:27.592Z",
  "time": 1792017087592,
  "conversationId": "07c0ExampleGroupId0002",
  "conversationType": "group",
  "isReportable": true
}
```

Examples of the others: `NEW_INVITE` in [Add Members](Conversations/AddMembers.md), `TITLE_CHANGE` in [Update Title](Conversations/UpdateTitle.md), `MESSAGE_READ` in [Update Last Read](Users/UpdateLastRead.md), `MEMBERS_JOIN` and `INVITE_REJECTED` in [Update Invite Status](Conversations/UpdateInviteStatus.md), `MEMBERS_LEFT`, `CONVERSATION_DEACTIVATED` and `CONVERSATION_DELETED` in [Leave Conversation](Conversations/LeaveConversation.md#events). The full list of types the overlay handles is in [Epic Connect](../../Launcher/Social/Connect.md#message-types-handled).
