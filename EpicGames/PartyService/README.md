# Hosts

This are some (not all) Hosts that you can access the Party Service from

- api.epicgames.dev (`/epic/party`)

<br/>

Recommended Hosts:

- api.epicgames.dev

Base URL is hardcoded in the social overlay (`EPIC_PARTY_ENDPOINT_URL`). Every route is under `/internal/v2`. Calls carry `X-Epic-Agent: epic-social` and `X-EPIC-CORRELATION-ID`; the client retries on `5xx`, `429` and `Retry-After`.

Auth is a plain EG1 bearer token from any client (verified with `launcherAppClient2` `34a02cf8f4414e29b15921876da36f9a` via `authorization_code`). One party per account. The party is shared with Fortnite: a Fortnite (Switch) client joined an EGL party, claimed voice and talked in the same room. Full voice walkthrough: [Voice Chat](../../Launcher/Flows/VoiceChat.md).

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/internal/v2/users/:accountId` | [Get Parties Summary](Users/GetUserSummary.md) |
| GET | `/internal/v2/parties/:partyId` | [Get Party](Parties/GetParty.md) |
| POST | `/internal/v2/parties` | [Create Party](Parties/CreateParty.md) |
| PATCH | `/internal/v2/parties/:partyId` | [Update Party Config](Parties/UpdatePartyConfig.md) |
| POST | `/internal/v2/parties/:partyId/members/:accountId/join` | [Join Party](Members/JoinParty.md) |
| DELETE | `/internal/v2/parties/:partyId/members/:accountId` | [Leave Party / Kick Member](Members/LeaveParty.md) |
| POST | `/internal/v2/parties/:partyId/members/:accountId/promote` | [Promote Member](Members/PromoteMember.md) |
| POST | `/internal/v2/parties/:partyId/members/:accountId/keep-alive` | [Keep Alive](Members/KeepAlive.md) |
| PATCH | `/internal/v2/parties/:partyId/members/:accountId/meta` | [Update Member Meta](Members/UpdateMemberMeta.md) |
| POST | `/internal/v2/parties/:partyId/members/:accountId/conferences/connection` | [Get Voice Room Connection](Conferences/ConnectVoiceRoom.md) |
| POST | `/internal/v2/users/:accountId/invites/:inviterId` | [Send Party Invite](Invites/SendInvite.md) |
| DELETE | `/internal/v2/users/:accountId/invites/:inviterId` | [Decline Party Invite](Invites/DeclineInvite.md) |
| POST | `/internal/v2/users/:accountId/joinRequests/:requesterId` | [Send Join Request](JoinRequests/SendJoinRequest.md) |
| DELETE | `/internal/v2/users/:accountId/joinRequests/:requesterId` | [Decline Join Request](JoinRequests/DeclineJoinRequest.md) |
| POST | `/internal/v2/groups/:groupId/parties/current/join` | [Join Group Party](Groups/JoinGroupParty.md) |

## Error codes read by the client

| Error Code | Status | Handling |
| --- | --- | --- |
| `errors.com.epicgames.social.party.party_not_found` | 404 | `numericErrorCode` `51002`, `originatingService` `party-v2`; ignored when leaving the old party. Returned for disbanded parties ([example](Parties/GetParty.md)) |
| `errors.com.epicgames.social.party.user_has_party` | 409 | create falls back to the existing `current` party |
| `errors.com.epicgames.social.party.stale_revision` | 409 | member meta PATCH is retried with the fresh revision |
| `errors.com.epicgames.social.party.client_policy_unknown` | | client-side only, logged when relationship state is unknown |

## Realtime events

Party changes are pushed over Epic Connect ([Connect](../../Launcher/Social/Connect.md)), not polled. Envelope: `{ correlationId, timestamp, id, connectionId, payload, type }`; `correlationId` is the `X-EPIC-CORRELATION-ID` of the REST call that caused the event, or `EOS-<32 hex>` when another product (EOS SDK) caused it.

| Type | Fields read |
| --- | --- |
| `party.v2.MEMBER_JOINED` | `party_id`, `account_id`, `account_dn`, `connection { id, meta, deployment_id, connected_at, updated_at }`, `revision`, `suspended`, `member_state_updated`, `joined_at`, `updated_at`, `sent` |
| `party.v2.MEMBER_LEFT`, `party.v2.MEMBER_EXPIRED_AFTER_DISCONNECT` | `party_id`, `account_id`, `account_dn`, `revision`, `suspended`, `member_state_updated` (leaver's last state), `joined_at`, `updated_at`, `sent` |
| `party.v2.MEMBER_EXPIRED_IN_SOLO_PARTY`, `party.v2.MEMBER_EXPIRED_PARTY_DISBANDED` | same, marks the party disbanded. `MEMBER_EXPIRED_PARTY_DISBANDED` is sent for the remaining member when a 2-member party drops to 1 ([disband behaviour](Members/LeaveParty.md#disband-behaviour-observed-2026-10-14)) |
| `party.v2.MEMBER_KICKED` | same, `account_id` = kicked member; raises `current-user-kicked-from-party` for self ([example](Members/LeaveParty.md#events)) |
| `party.v2.MEMBER_CONNECTED` / `party.v2.MEMBER_DISCONNECTED` | `party_id`, `account_id`, `account_dn`, `connection`, `revision`, `suspended` |
| `party.v2.MEMBER_STATE_UPDATED` | `party_id`, `account_id`, `account_dn`, `connection`, `revision`, `suspended`, `member_state_updated`, `member_state_removed`, `member_state_overridden` |
| `party.v2.JOIN_REQUEST_CREATED`, `party.v2.JOIN_REQUEST_EXPIRED` | `requester_id`, `requester_dn`, `requestee_id`, `sent_at`, `expires_at`, `auto`, `sent` ([example](JoinRequests/SendJoinRequest.md)). `EXPIRED` also when the leader accepts by inviting |
| `party.v2.INVITE_CREATED` | `party_id`, `inviter_id`, `inviter_dn`, `invitee_id`, `sent_at`, `updated_at`, `expires_at`, `auto` (+ `group_id`, `inviter_pl_dn` read by the client) |
| `party.v2.INVITE_CANCELLED`, `party.v2.INVITE_EXPIRED` | `inviter_id`, `invitee_id`. Captured `INVITE_EXPIRED` = the `INVITE_CREATED` payload + `meta: {}`, sent when the invitee joins or [declines](Invites/DeclineInvite.md). `INVITE_CANCELLED` not captured |
| `party.v2.MEMBER_REFRESH_SUMMARY` | none, triggers Get Parties Summary |
| `party.v2.PARTY_UPDATED` | `party_id`, `party_lead`, `meta`, `party_privacy_type`, `max_number_of_members`, `chat_conversation_id`, `created_at`, `updated_at`, `is_reportable`, `revision`, `sent`; config changes add `author_id`, `party_state_updated`, `party_state_removed`, `party_state_overridden` (client also reads `source_chat_conversation_id`). Sent on `is_reportable` changes, promote, leader leaving, config changes ([example](Members/PromoteMember.md)) |

Captured order when EGL creates a party, invites a Fortnite (Switch) friend who accepts, and both claim voice: `social.chat.v1.CONVERSATION_CREATED`, `social.chat.v1.REPORTABILITY_CHANGE`, `MEMBER_JOINED` (self), `INVITE_CREATED`, `MEMBER_STATE_UPDATED` (self voice claim), `INVITE_EXPIRED`, `MEMBER_JOINED` (friend), `social.chat.v1.MEMBERS_JOIN`, `MEMBER_CONNECTED` (friend), `MEMBER_STATE_UPDATED` (friend `platform_name` / `product_name`), `MEMBER_STATE_UPDATED` (friend `active_voice_connection`).

_Example `party.v2.MEMBER_JOINED` (Fortnite member)_

```json
{
  "correlationId": "EOS-1e08232aceb343b3950060b0b986d73d",
  "timestamp": 1791996825458,
  "id": "YjE5ZTNkN2E0YzBmNDI2MW",
  "connectionId": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
  "payload": {
    "sent": "2026-10-14T16:53:45.453Z",
    "connection": {
      "id": "8d2e47fffe1b9c63-00000001-05a1c3e7-2f6b8d0e4a9c7135-7e3d5b1a#sub-eas-private-1029384756",
      "meta": { "platform": "SWT", "game": "fn" },
      "deployment_id": "62a9473a2dca46b29ccf17577fcf42d7",
      "connected_at": "2026-10-14T16:53:45.449Z",
      "updated_at": "2026-10-14T16:53:45.442Z"
    },
    "suspended": false,
    "revision": 0,
    "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "account_id": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
    "account_dn": "ExampleFriend",
    "member_state_updated": {},
    "joined_at": "2026-10-14T16:53:45.451Z",
    "updated_at": "2026-10-14T16:53:45.451Z"
  },
  "type": "party.v2.MEMBER_JOINED"
}
```

_Example `party.v2.MEMBER_STATE_UPDATED` (voice claim)_

```json
{
  "correlationId": "2dc2bf06-48ce-4205-9d29-404c5fa27eca",
  "timestamp": 1791996825379,
  "id": "OTk4ZTFhNmIyYzRkNDA3Zj",
  "connectionId": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
  "payload": {
    "sent": "2026-10-14T16:53:45.379Z",
    "connection": {
      "id": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
      "meta": { "osName": "Windows", "platformName": "egs", "productName": "Epic Games Launcher" },
      "deployment_id": "_",
      "connected_at": "2026-10-14T16:53:45.116Z",
      "updated_at": "2026-10-14T16:53:45.378Z"
    },
    "suspended": false,
    "revision": 1,
    "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "account_id": "94b1569506b04f9f8557af611e8c5e47",
    "account_dn": "ExampleUser",
    "member_state_removed": [],
    "member_state_updated": {
      "platform_name": "Windows",
      "product_name": "Epic Games Launcher",
      "active_voice_connection": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d"
    },
    "member_state_overridden": {},
    "joined_at": "2026-10-14T16:53:45.116Z",
    "updated_at": "2026-10-14T16:53:45.378Z"
  },
  "type": "party.v2.MEMBER_STATE_UPDATED"
}
```

_Example `party.v2.INVITE_CREATED`_

```json
{
  "correlationId": "029ad58c-6a66-4cf0-9fb3-0045ad5bebb5",
  "timestamp": 1791996825322,
  "id": "NmQ3YTFjMmU5YjRmNDA4ZT",
  "connectionId": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
  "payload": {
    "sent": "2026-10-14T16:53:45.322Z",
    "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "inviter_id": "94b1569506b04f9f8557af611e8c5e47",
    "inviter_dn": "ExampleUser",
    "invitee_id": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
    "sent_at": "2026-10-14T16:53:45.315Z",
    "updated_at": "2026-10-14T16:53:45.315Z",
    "expires_at": "2026-10-14T17:53:45.315Z",
    "auto": false
  },
  "type": "party.v2.INVITE_CREATED"
}
```

`is_reportable` is computed by the server from the members' voice connections and pushed in `PARTY_UPDATED`; clients never write it ([Moderation](../../Launcher/Voice/Moderation.md#is_reportable)).

A Fortnite member has two connections: `<id>#sub-eas-private-<n>` (`meta { platform, game }`, used as `active_voice_connection`) and `<id>#sub-eas-<n>` (`meta {}`, seen in `MEMBER_CONNECTED`).

The launcher (Rust, `src\social\party_leave.rs`) also consumes `party.v2.MEMBER_LEFT` (`VOLUNTARY`), `MEMBER_KICKED` (`KICKED`), `MEMBER_EXPIRED_AFTER_DISCONNECT` (`DISCONNECTED`), `MEMBER_EXPIRED_PARTY_DISBANDED` (`DISBANDED`) and `MEMBER_EXPIRED_IN_SOLO_PARTY` from its own Epic Connect client, for party-leave analytics.
