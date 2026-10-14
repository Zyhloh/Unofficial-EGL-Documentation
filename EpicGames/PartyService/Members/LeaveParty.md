## Party Service - Members: Leave Party / Kick Member

Same route for leaving (`leave-party`, own id) and kicking (`kick-party-member`, another member; leader only). `404 errors.com.epicgames.social.party.party_not_found` is ignored when leaving before create/join. A standalone voice client calls it on shutdown after releasing voice ([Update Member Meta](UpdateMemberMeta.md) with `active_in_party_voice_room: false`).

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId \
Method: DELETE \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: Own account id to leave, another member to kick <br/>

No body. Response `204 No Content` for both leave and kick (confirmed live). Only the status is checked.

## Events

| Case | Events (to the remaining members) |
| --- | --- |
| Member leaves | `party.v2.MEMBER_LEFT` (payload carries the leaver's last `member_state_updated`), `social.chat.v1.MEMBERS_LEFT` |
| Leader kicks a member | `party.v2.MEMBER_KICKED` for the kicked member |
| Party disbanded | `party.v2.MEMBER_EXPIRED_PARTY_DISBANDED` for each remaining member, `social.chat.v1.CONVERSATION_DEACTIVATED` for `ep-<partyId>` |
| Leader leaves, party survives | `party.v2.PARTY_UPDATED` with the new `party_lead`, then `MEMBER_LEFT` |

## Disband behaviour (observed 2026-10-14)

| Case | Result |
| --- | --- |
| Creator alone in a party leaves | `MEMBER_LEFT` (self) + `CONVERSATION_DEACTIVATED`; no disband event. A 1-member party you created is not disbanded while you are in it |
| 2 members, leader kicks the other | party disbanded: `MEMBER_EXPIRED_PARTY_DISBANDED` for the leader (the remaining member), `MEMBER_KICKED`, `CONVERSATION_DEACTIVATED`. The party is gone right away |
| 2 members, leader leaves | party disbanded: `MEMBER_LEFT`, `MEMBER_EXPIRED_PARTY_DISBANDED` for the remaining member, `CONVERSATION_DEACTIVATED`; [Get Party](../Parties/GetParty.md) returns `404` from then on |
| 3 members, leader leaves | party survives; `PARTY_UPDATED` makes the remaining member who joined earliest the new `party_lead` |

A party that drops from 2 members to 1 is disbanded; the remaining member does not keep it. Leaving or calling Get Party on it afterwards returns `404` with `party_not_found`.

---

_Example `party.v2.MEMBER_KICKED`_

```json
{
  "correlationId": "c7f4263d-61bc-4d3a-aef1-213f4a9b7003",
  "timestamp": 1792000920422,
  "id": "NmI5YmQ3YjY0NWYxOGRiOQ",
  "connectionId": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
  "payload": {
    "sent": "2026-10-14T18:02:00.421Z",
    "suspended": false,
    "revision": 5,
    "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "account_id": "94b1569506b04f9f8557af611e8c5e47",
    "account_dn": "ExampleUser",
    "member_state_updated": {
      "active_voice_connection": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
      "product_name": "Epic Games Launcher",
      "platform_name": "Windows"
    },
    "joined_at": "2026-10-14T17:58:53.829Z",
    "updated_at": "2026-10-14T17:59:57.390Z"
  },
  "type": "party.v2.MEMBER_KICKED"
}
```

`account_id` is the kicked member. `MEMBER_LEFT` and `MEMBER_EXPIRED_PARTY_DISBANDED` have the same payload shape.

_Example `party.v2.MEMBER_EXPIRED_PARTY_DISBANDED` (sent in the same millisecond as the kick above, for the remaining leader)_

```json
{
  "correlationId": "c7f4263d-61bc-4d3a-aef1-213f4a9b7003",
  "timestamp": 1792000920422,
  "id": "NjBkNGZlODRlZTFjM2IyNQ",
  "connectionId": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
  "payload": {
    "sent": "2026-10-14T18:02:00.422Z",
    "suspended": false,
    "revision": 1,
    "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "account_id": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
    "account_dn": "ExampleAlt",
    "member_state_updated": {
      "active_voice_connection": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
      "product_name": "Epic Games Launcher",
      "platform_name": "Windows"
    },
    "joined_at": "2026-10-14T17:58:54.316Z",
    "updated_at": "2026-10-14T17:58:54.537Z"
  },
  "type": "party.v2.MEMBER_EXPIRED_PARTY_DISBANDED"
}
```

When the disbanded party had a voice room, the signaling server then sends `user_left` and `kick_user` ([RTC Signaling](../../../Launcher/Voice/RTCSignaling.md#kick_user)).

_Example Error (leave after the party was disbanded)_

```json
{
  "errorCode": "errors.com.epicgames.social.party.party_not_found",
  "errorMessage": "Party [2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f] does not exist.",
  "messageVars": [
    "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f"
  ],
  "numericErrorCode": 51002,
  "originatingService": "party-v2",
  "intent": "prod"
}
```
