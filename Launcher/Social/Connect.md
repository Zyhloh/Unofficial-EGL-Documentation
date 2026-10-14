# Social Overlay - Epic Connect

Epic Connect is the realtime push channel: STOMP over WebSocket. The overlay opens its own connection; the Rust launcher opens a second one (`eglv2_lib::epic_connect`).

## Overlay connection

URL: `wss://connect.ol.epicgames.com/?auth-token=<elevated token>&avatarFnDeploymentId=62a9473a2dca46b29ccf17577fcf42d7&accept-language=<locale>`

- `auth-token` is the elevated (EG1) access token (`account-info.elevatedToken`).
- Any `wss://`, `ws://`, `https://`, `http://` prefix in the configured URL is stripped and replaced with `wss://`.
- WebSocket subprotocols offered: `v12.stomp`, `v11.stomp`, `v10.stomp`.
- No STOMP CONNECT headers besides the defaults: `accept-version: 1.2,1.1,1.0`, `heart-beat: 45000,0` (client sends a heartbeat every 45s, expects none).

### Flow

1. Open the socket, send `CONNECT`, receive `CONNECTED`.
2. `SUBSCRIBE` with `id: sub-0`, `destination: <uuid>/account/<accountId>`. The prefix is a `crypto.randomUUID()` generated per client instance (the code names it `deployment`).
3. Every `MESSAGE` body is JSON. The first one is `core.connect.v1.connected`; its `connectionId` is stored as `epicConnectId` and used as the presence connection id ([Update Presence](../../EpicGames/PresenceService/Presence/UpdatePresence.md)).
4. Reconnect on drop: delay `min(500ms * 2^attempt, 5min) * (0.8..1.2)`; STOMP `ERROR` frames carry `{ statusCode, message, type, correlationId }` and only status codes `4003`, `4004`, `4006`, `4009` are retried. A token or locale change forces a full reconnect.

### Message envelope

```json
{
  "id": "6a7c3f0e-...",
  "type": "presence.v1.UPDATE",
  "connectionId": "94b1569506b04f9f8557af611e8c5e47",
  "correlationId": "...",
  "timestamp": 1728900000000,
  "payload": {}
}
```

### Message types handled

| Type | Payload fields read |
| --- | --- |
| `core.connect.v1.connected` | `connectionId` (envelope) |
| `core.connect.v1.disconnected` | synthesized locally on disconnect |
| `friends.v1.FRIENDSHIP_REQUEST` | `from`, `to`, `status` (`ACCEPTED` -> friend added, `PENDING` -> request), `timestamp` |
| `friends.v1.FRIENDSHIP_REMOVE` | `from`, `to`, `reason` (`DELETED` = unfriended, otherwise request removed) |
| `friends.v1.FRIENDSHIP_ENTRY_UPDATE` | `friendId` (refetched via GraphQL `friend`) |
| `friends.v1.USER_BLOCKLIST_UPDATE` | `accountId`, `status` (`BLOCKED` / other) |
| `friends.v1.USER_SETTINGS_UPDATE` | `invitationMode` (`FRIENDS_OF_FRIENDS`, `PRIVATE`, other = public) |
| `presence.v1.UPDATE` | `accountId`, `status`, `perNs[]` (see below). Buffered 500ms |
| `social.chat.v1.NEW_MESSAGE` | `conversation.{conversationId,type}`, `message.{msgId,senderId,time,sourceMsgId,isReportable,body,metadata.Sig,metadata.Pub}` |
| `social.chat.v1.MESSAGE_REDACTED` / `MESSAGE_DELETED` | `msgId`, `conversation.{conversationId,type}`, `senderId`, `time`, `reportable` |
| `social.chat.v1.MESSAGE_READ` | `conversationId`, `lastReadMessageId`, `totalUnreadMessages`, `hasMoreUnreadMessages`, `time` |
| `social.chat.v1.CONVERSATION_CREATED` | `conversationId`, `type`, `members`, `invited`, `inviter`, `dateCreated`, `isReportable`, `isActive` |
| `social.chat.v1.CONVERSATION_DELETED` | `conversationId` |
| `social.chat.v1.NEW_INVITE` | `conversationId`, `type`, `title`, `members`, `invited`, `inviter`, `createdBy`, `conversationCreatedAt`, `inviteTime`, `time`, `msgId`, `isReportable` |
| `social.chat.v1.REPORTABILITY_CHANGE` | `conversationId`, `type`, `isReportable`, `msgId`, `time` |
| `social.chat.v1.TITLE_CHANGE` | `conversationId`, `accountId`, `title`, `time`, `msgId`, `isReportable` |
| `social.chat.v1.MEMBERS_JOIN` / `MEMBERS_LEFT` | `conversationId`, `type`, `members`, `msgId`, `time`, `isReportable` |
| `social.chat.v1.INVITE_READ` | `conversationId`, `totalPendingInvites`, `hasMorePendingInvites` |
| `social.chat.v1.INVITE_REJECTED` | `conversationId`, `rejectedBy`, `msgId`, `time`, `isReportable` |
| `social.chat.v1.CONVERSATION_ACTIVATED` / `CONVERSATION_DEACTIVATED` | `conversationId`, `parentConversationId` |
| `social.chat.v1.NEW_CHILD_CONVERSATION_CREATED` | `parentConversationId`, `childConversationId`, `members`, `msgId`, `time` |
| `socialban.v1.BAN_APPLIED` | `account_id`, `starts_at`, `ends_at`, `duration_s`, `name.features`, `acked`. The app immediately calls [Acknowledge Ban](../../EpicGames/SocialBanService/Bans/AcknowledgeBan.md) |
| `socialban.v1.BAN_ACKED` / `BAN_LIFTED` | same shape |
| `k3s.v1.PARENT_LIMITS_CHANGED` | `productIds` (must contain `prod-fn`), `originalEventSentAt`, `settings[].{namespace,settingName,parentLimit}` |
| `k3s.v1.EFFECTIVE_VALUES_CHANGED` | `productIds`, `originalEventSentAt`, `settings[].{namespace,settingName,effectiveValue}` |
| `party.v2.*` | `PARTY_UPDATED`, `MEMBER_JOINED`, `MEMBER_LEFT`, `MEMBER_KICKED`, `MEMBER_STATE_UPDATED`, `MEMBER_CONNECTED`, `MEMBER_DISCONNECTED`, `MEMBER_EXPIRED_AFTER_DISCONNECT`, `MEMBER_EXPIRED_IN_SOLO_PARTY`, `MEMBER_EXPIRED_PARTY_DISBANDED`, `MEMBER_REFRESH_SUMMARY`, `INVITE_CREATED`, `INVITE_CANCELLED`, `INVITE_EXPIRED`, `JOIN_REQUEST_CREATED`, `JOIN_REQUEST_EXPIRED` (see party docs) |

The client-only types `social.chat.v1.PENDING_MESSAGE`, `PENDING_MESSAGE_FAILED`, `PENDING_INIT_DM`, `PENDING_INIT_DM_FAILED`, `CONVERSATION_PARTY_STARTED`, `CONVERSATION_PARTY_ENDED`, `CONVERSATION_PARTY_CHAT_ENDED` share the namespace but are used for local message state.

### presence.v1.UPDATE payload

```json
{
  "accountId": "94b1569506b04f9f8557af611e8c5e47",
  "status": "online",
  "perNs": [
    {
      "ns": "_",
      "status": "online",
      "statusManual": false,
      "party": { "id": "...", "joinable": true, "invitable": true, "memberCount": 2 },
      "conns": [ { "props": { "running_app_id": "...", "running_app_name": "..." } } ]
    },
    {
      "ns": "<deployment>",
      "status": "online",
      "productId": "...",
      "activity": { "value": "In Lobby" },
      "props": { "EOS_ProductName": "...", "EOS_Platform": "...", "EOS_IntegratedPlatform": "EGS", "EOS_Lobby": "...", "EOS_Session": "...", "X_NonEOS_ProductName": "..." }
    }
  ]
}
```

_Shape from client_. Status values: `online`, `away`, `xa` (shown as away), `dnd` (shown as offline), `offline`. The `_` namespace carries party presence; the best non-`_` entry (ordered `online < away < dnd < xa`) supplies the game shown.

## Launcher connection (Rust)

`src\epic_connect\{episode,ws}.rs` dials `wss://connect.epicgames.dev` (environment table) with the EG1 access token in a request header (header name not recovered; `TokenHeaderInvalid` aborts the dial), offering `Sec-WebSocket-Protocol: v10.stomp,v11.stomp,v12.stomp` and retrying without the offer if the server does not echo one. It sends STOMP heartbeats (`Social.EpicConnect.HeartbeatSent`) and captures the connection id (`ConnectionIdCaptured`). Consumers: party leave (`Social.PartyLeave.EpicConnect*`) and launcher presence (`epic-connect: (re)publishing presence on connect`, see [Update Presence (Launcher)](../../EpicGames/PresenceService/Presence/UpdatePresenceLauncher.md)).
