# Social Overlay - Epic Connect

Epic Connect is the realtime push channel: STOMP over WebSocket. The overlay opens its own connection; the Rust launcher opens a second one (`eglv2_lib::epic_connect`).

## Overlay connection

URL: `wss://connect.ol.epicgames.com/?auth-token=<elevated token>&avatarFnDeploymentId=62a9473a2dca46b29ccf17577fcf42d7&accept-language=<locale>`

- `auth-token` is the EG1 access token (`account-info.elevatedToken`); any client's EG1 token works.
- Any `wss://`, `ws://`, `https://`, `http://` prefix in the configured URL is stripped and replaced with `wss://`.
- WebSocket subprotocols offered: `v12.stomp`, `v11.stomp`, `v10.stomp`.
- No STOMP CONNECT headers besides the defaults: `accept-version: 1.2,1.1,1.0`, `heart-beat: 45000,0` (client sends a heartbeat every 45s, expects none). The server answers `heart-beat:0,45000`.

### Flow

1. Open the socket, send `CONNECT`, receive `CONNECTED`. The `session` header of `CONNECTED` is the connection id.
2. `SUBSCRIBE` with `id: sub-0`, `destination: <uuid>/account/<accountId>`. The prefix is a `crypto.randomUUID()` generated per client instance (the code names it `deployment`).
3. Every `MESSAGE` body is JSON. The first one is `core.connect.v1.connected`; its `connectionId` (same value as `session`) is stored as `epicConnectId` and used as the presence connection id ([Update Presence](../../EpicGames/PresenceService/Presence/UpdatePresence.md)) and the party connection id ([Create Party](../../EpicGames/PartyService/Parties/CreateParty.md)).
4. Reconnect on drop: delay `min(500ms * 2^attempt, 5min) * (0.8..1.2)`; STOMP `ERROR` frames carry `{ statusCode, message, type, correlationId }` and only status codes `4003`, `4004`, `4006`, `4009` are retried. A token or locale change forces a full reconnect.

Any EG1 token works (a standalone client with a `launcherAppClient2` token received the same events). Server frames can be binary WebSocket messages; decode as UTF-8 and strip the trailing NUL.

### Captured frames

```
CONNECT
accept-version:1.2,1.1,1.0
heart-beat:45000,0

^@
```

```
CONNECTED
version:1.2
heart-beat:0,45000
session:3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d

^@
```

```
SUBSCRIBE
id:sub-0
destination:20d0a958-8dd0-490a-bb7f-fe8939e7be44/account/94b1569506b04f9f8557af611e8c5e47

^@
```

```
MESSAGE
destination:20d0a958-8dd0-490a-bb7f-fe8939e7be44/account/94b1569506b04f9f8557af611e8c5e47
subscription:sub-0
message-id:6f2b8c1e-4d7a-4e93-b5c0-1a9d3e7f2b64
content-type:application/json
content-length:195

{"correlationId":"d2d7de01-db20-4daa-ba85-f71bcc689c6e","timestamp":1791996819605,"connectionId":"3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d","type":"core.connect.v1.connected"}^@
```

The connection id format is `<16 hex>-<8 hex>-<8 hex>-<16 hex>-<8 hex>`. Fortnite (EOS) connections append `#sub-eas-<n>` / `#sub-eas-private-<n>`.

### Message envelope

```json
{
  "correlationId": "31e2f66b-2d79-4da9-828c-6e01a0c06c24",
  "timestamp": 1791996825167,
  "id": "NzE0YjJlOGQ1YzNhNDZmMT",
  "connectionId": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
  "payload": {
    "namespace": "_",
    "metadata": { "partyId": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f" },
    "conversationId": "ep-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "type": "epic_party",
    "members": [ "94b1569506b04f9f8557af611e8c5e47" ],
    "isReportable": false,
    "dateCreated": "2026-10-14T16:53:45.123Z",
    "isActive": true
  },
  "type": "social.chat.v1.CONVERSATION_CREATED"
}
```

`correlationId` echoes the `X-EPIC-CORRELATION-ID` of the REST call that caused the event (`EOS-<32 hex>` when an EOS SDK client caused it). `id` equals the STOMP `message-id` for most events.

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
| `social.chat.v1.REPORTABILITY_CHANGE` | `conversationId`, `type`, `isReportable`, `msgId`, `time` (the captured payload carries `conversationType`, not `type`) |
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
| `party.v2.*` | `PARTY_UPDATED`, `MEMBER_JOINED`, `MEMBER_LEFT`, `MEMBER_KICKED`, `MEMBER_STATE_UPDATED`, `MEMBER_CONNECTED`, `MEMBER_DISCONNECTED`, `MEMBER_EXPIRED_AFTER_DISCONNECT`, `MEMBER_EXPIRED_IN_SOLO_PARTY`, `MEMBER_EXPIRED_PARTY_DISBANDED`, `MEMBER_REFRESH_SUMMARY`, `INVITE_CREATED`, `INVITE_CANCELLED`, `INVITE_EXPIRED`, `JOIN_REQUEST_CREATED`, `JOIN_REQUEST_EXPIRED`. Captured live (2026-10-14): `MEMBER_JOINED`, `MEMBER_LEFT`, `MEMBER_KICKED`, `MEMBER_CONNECTED`, `MEMBER_STATE_UPDATED`, `MEMBER_EXPIRED_PARTY_DISBANDED`, `PARTY_UPDATED`, `INVITE_CREATED`, `INVITE_EXPIRED`, `JOIN_REQUEST_CREATED`, `JOIN_REQUEST_EXPIRED` ([Party Service events](../../EpicGames/PartyService/README.md#realtime-events), [disband behaviour](../../EpicGames/PartyService/Members/LeaveParty.md#disband-behaviour-observed-2026-10-14)) |

Chat types captured live (2026-10-14): `CONVERSATION_CREATED`, `NEW_INVITE`, `REPORTABILITY_CHANGE`, `NEW_MESSAGE`, `TITLE_CHANGE`, `MESSAGE_READ`, `MEMBERS_JOIN` ([Chat Service events](../../EpicGames/ChatService/README.md#realtime-events), with payload examples). `NEW_MESSAGE` is nested (`conversation`, `message`), unlike the flat history entries.

The client-only types `social.chat.v1.PENDING_MESSAGE`, `PENDING_MESSAGE_FAILED`, `PENDING_INIT_DM`, `PENDING_INIT_DM_FAILED`, `CONVERSATION_PARTY_STARTED`, `CONVERSATION_PARTY_ENDED`, `CONVERSATION_PARTY_CHAT_ENDED` share the namespace but are used for local message state.

### presence.v1.UPDATE payload

Captured (a friend playing Fortnite on Switch):

```json
{
  "accountId": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
  "status": "online",
  "perNs": [
    {
      "status": "online",
      "activity": {},
      "party": { "joinable": false, "invitable": true },
      "ns": "_",
      "conns": [
        { "id": "8d2e47fffe1b9c63-00000001-05a1c3e7-2f6b8d0e4a9c7135-7e3d5b1a#sub-eas-private-1029384756", "props": {} }
      ]
    },
    {
      "productId": "prod-fn",
      "appId": "fghi4567FNFBKFz3E4TROb0bmPS8h1GW",
      "status": "online",
      "activity": { "value": "Available" },
      "ns": "62a9473a2dca46b29ccf17577fcf42d7",
      "props": {
        "EOS_ProductName": "Fortnite",
        "EOS_ProductVersion": "++Fortnite+Release-42.30-CL-58557680",
        "EOS_Platform": "SWT",
        "EOS_IntegratedPlatform": "UNKNOWN",
        "EOS_OnlinePlatformType": "2000",
        "EOS_Session": "{\"version\":3}",
        "EOS_Lobby": "{\"version\":3}",
        "FortPartySize": "i1",
        "FortSubGame": "i1",
        "FortLFG": "i0",
        "IsInZone": "bfalse",
        "InUnjoinableMatch": "bfalse",
        "IslandCode": "s",
        "party.joininfodata.286331153": "m{\"bIsPrivate\":true}"
      },
      "conns": [
        { "id": "8d2e47fffe1b9c63-00000001-05a1c3e7-2f6b8d0e4a9c7135-7e3d5b1a#sub-eas-1029384756", "props": {} }
      ]
    }
  ]
}
```

Fortnite `props` values are type-prefixed strings (`i` int, `b` bool, `s` string, `m` JSON). After the friend joined an EGL party, `party.joininfodata.286331153` carried `m{"sDN":"ExampleFriend","sP":"SWT","p":"2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f-<n>-default","d":"Fortnite",...}`. Status values: `online`, `away`, `xa` (shown as away), `dnd` (shown as offline), `offline`. The `_` namespace carries party presence; the best non-`_` entry (ordered `online < away < dnd < xa`) supplies the game shown. Overlay-side fields read from the `_` entry also include `party.id`, `party.memberCount` and `conns[].props.running_app_id` / `running_app_name` (from the client code).

## Launcher connection (Rust)

`src\epic_connect\{episode,ws}.rs` dials `wss://connect.epicgames.dev` (environment table) with the EG1 access token in a request header (header name not recovered; `TokenHeaderInvalid` aborts the dial), offering `Sec-WebSocket-Protocol: v10.stomp,v11.stomp,v12.stomp` and retrying without the offer if the server does not echo one. It sends STOMP heartbeats (`Social.EpicConnect.HeartbeatSent`) and captures the connection id (`ConnectionIdCaptured`). Consumers: party leave (`Social.PartyLeave.EpicConnect*`) and launcher presence (`epic-connect: (re)publishing presence on connect`, see [Update Presence (Launcher)](../../EpicGames/PresenceService/Presence/UpdatePresenceLauncher.md)).
