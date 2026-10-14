# Hosts

This are some (not all) Hosts that you can access the Party Service from

- api.epicgames.dev (`/epic/party`)

<br/>

Recommended Hosts:

- api.epicgames.dev

Base URL is hardcoded in the social overlay (`EPIC_PARTY_ENDPOINT_URL`). Every route is under `/internal/v2`. Calls carry `X-Epic-Agent: epic-social` and `X-EPIC-CORRELATION-ID`; the client retries on `5xx`, `429` and `Retry-After`.

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
| `errors.com.epicgames.social.party.party_not_found` | 404 | ignored when leaving the old party |
| `errors.com.epicgames.social.party.user_has_party` | 409 | create falls back to the existing `current` party |
| `errors.com.epicgames.social.party.stale_revision` | 409 | member meta PATCH is retried with the fresh revision |
| `errors.com.epicgames.social.party.client_policy_unknown` | | client-side only, logged when relationship state is unknown |

## Realtime events

Party changes are pushed over Epic Connect ([Connect](../../Launcher/Social/Connect.md)), not polled:

| Type | Fields read |
| --- | --- |
| `party.v2.MEMBER_JOINED` | `party_id`, `account_id`, `connection { id, connected_at, local_play_enabled }`, `revision`, `suspended` |
| `party.v2.MEMBER_LEFT`, `party.v2.MEMBER_EXPIRED_AFTER_DISCONNECT` | `party_id`, `account_id`, `sent` |
| `party.v2.MEMBER_EXPIRED_IN_SOLO_PARTY`, `party.v2.MEMBER_EXPIRED_PARTY_DISBANDED` | same, marks the party disbanded |
| `party.v2.MEMBER_KICKED` | same, raises `current-user-kicked-from-party` for self |
| `party.v2.MEMBER_CONNECTED` / `party.v2.MEMBER_DISCONNECTED` | `party_id`, `account_id`, `connection`, `revision`, `suspended` |
| `party.v2.MEMBER_STATE_UPDATED` | `party_id`, `account_id`, `revision`, `suspended`, `member_state_updated`, `member_state_removed` |
| `party.v2.JOIN_REQUEST_CREATED` | `requester_id`, `expires_at`, `auto` |
| `party.v2.JOIN_REQUEST_EXPIRED` | `requester_id`, `requestee_id`, `sent_at` |
| `party.v2.INVITE_CREATED` | `inviter_id`, `group_id`, `expires_at`, `inviter_pl_dn`, `inviter_dn`, `party_id`, `auto` (+ message `correlationId`) |
| `party.v2.INVITE_CANCELLED`, `party.v2.INVITE_EXPIRED` | `inviter_id`, `invitee_id` |
| `party.v2.MEMBER_REFRESH_SUMMARY` | none, triggers Get Parties Summary |
| `party.v2.PARTY_UPDATED` | `is_reportable`, `party_lead`, `updated_at`, `revision`, `chat_conversation_id`, `source_chat_conversation_id`, `party_privacy_type`, `party_state_updated` |

The launcher (Rust, `src\social\party_leave.rs`) also consumes `party.v2.MEMBER_LEFT` (`VOLUNTARY`), `MEMBER_KICKED` (`KICKED`), `MEMBER_EXPIRED_AFTER_DISCONNECT` (`DISCONNECTED`), `MEMBER_EXPIRED_PARTY_DISBANDED` (`DISBANDED`) and `MEMBER_EXPIRED_IN_SOLO_PARTY` from its own Epic Connect client, for party-leave analytics.
