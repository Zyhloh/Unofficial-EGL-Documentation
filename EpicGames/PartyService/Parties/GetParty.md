## Party Service - Parties: Get Party

Fetches one party. Used by `get-party`, `get-bulk-parties` (one call per id), join (after the join POST), `refresh-active-party-voice-check` and the stale-revision retry of member meta.

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId \
Method: GET \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>

| Field | Notes |
| --- | --- |
| `members[].connections[]` | `disconnected_at` is set on dead connections; the client keeps only live ones. `is_first_party` and `meta.osName` / `meta.platformName` feed the voice-claim logic. Fortnite connections carry `meta { platform, game }` and ids ending in `#sub-eas-private-<n>` |
| `members[].connections[].active_in_party_voice_room` | set by [Update Member Meta](../Members/UpdateMemberMeta.md) |
| `members[].meta` | member state; voice keys are `active_voice_connection`, `platform_name`, `product_name` |
| `meta` | party state; the client writes `created_by` |
| `config.joinability` | `OPEN` / `INVITE_ONLY` |
| `is_reportable` | server-computed, never written by clients; gates the voice report UI and the "Reporting on" label ([Moderation](../../../Launcher/Voice/Moderation.md#is_reportable)) |
| `party_lead` | current leader; changes on promote and when the leader leaves a party of 3+ ([Leave Party](../Members/LeaveParty.md#disband-behaviour-observed-2026-10-14)) |
| `revision` | party revision; bumped by config changes, lead changes and `is_reportable` changes. [Update Party Config](UpdatePartyConfig.md) must send it |

`is_reportable` is computed by the server (see [Moderation](../../../Launcher/Voice/Moderation.md#is_reportable)): it was `true` while both members of a 2-member EGL party had a connection with `active_in_party_voice_room: true`, and flipped to `false` when one of them deafened.

---

_Example Response (2 EGL members, both in voice)_

```json
{
  "id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
  "party_lead": "94b1569506b04f9f8557af611e8c5e47",
  "created_at": "2026-10-14T17:58:53.823Z",
  "updated_at": "2026-10-14T17:58:54.568Z",
  "config": {
    "joinability": "INVITE_ONLY",
    "max_size": 16
  },
  "meta": {
    "created_by": "94b1569506b04f9f8557af611e8c5e47"
  },
  "revision": 1,
  "chat_conversation_id": "ep-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
  "is_reportable": true,
  "members": [
    {
      "account_id": "94b1569506b04f9f8557af611e8c5e47",
      "meta": {
        "platform_name": "Windows",
        "product_name": "Epic Games Launcher",
        "active_voice_connection": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d"
      },
      "revision": 1,
      "updated_at": "2026-10-14T17:58:54.114Z",
      "joined_at": "2026-10-14T17:58:53.829Z",
      "suspended": false,
      "connections": [
        {
          "id": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
          "deployment_id": "_",
          "connected_at": "2026-10-14T17:58:53.829Z",
          "updated_at": "2026-10-14T17:58:54.114Z",
          "is_first_party": true,
          "meta": {
            "osName": "Windows",
            "platformName": "egs",
            "productName": "Epic Games Launcher"
          },
          "active_in_party_voice_room": true
        }
      ]
    },
    {
      "account_id": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
      "meta": {
        "platform_name": "Windows",
        "product_name": "Epic Games Launcher",
        "active_voice_connection": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b"
      },
      "revision": 1,
      "updated_at": "2026-10-14T17:58:54.537Z",
      "joined_at": "2026-10-14T17:58:54.316Z",
      "suspended": false,
      "connections": [
        {
          "id": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
          "deployment_id": "_",
          "connected_at": "2026-10-14T17:58:54.315Z",
          "updated_at": "2026-10-14T17:58:54.537Z",
          "is_first_party": true,
          "meta": {
            "osName": "Windows",
            "platformName": "egs",
            "productName": "Epic Games Launcher"
          },
          "active_in_party_voice_room": true
        }
      ]
    }
  ]
}
```

_Example Response (Fortnite member, from a 3-member party)_

```json
{
  "account_id": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
  "meta": {
    "platform_name": "Switch",
    "product_name": "Fortnite",
    "active_voice_connection": "8d2e47fffe1b9c63-00000001-05a1c3e7-2f6b8d0e4a9c7135-7e3d5b1a#sub-eas-private-1029384756"
  },
  "revision": 2,
  "updated_at": "2026-10-14T18:05:45.430Z",
  "joined_at": "2026-10-14T18:05:44.735Z",
  "suspended": false,
  "connections": [
    {
      "id": "8d2e47fffe1b9c63-00000001-05a1c3e7-2f6b8d0e4a9c7135-7e3d5b1a#sub-eas-private-1029384756",
      "deployment_id": "62a9473a2dca46b29ccf17577fcf42d7",
      "connected_at": "2026-10-14T18:05:44.733Z",
      "updated_at": "2026-10-14T18:05:45.430Z",
      "is_first_party": true,
      "meta": {
        "platform": "SWT",
        "game": "fn"
      },
      "active_in_party_voice_room": true
    },
    {
      "id": "8d2e47fffe1b9c63-00000001-05a1c3e7-2f6b8d0e4a9c7135-7e3d5b1a#sub-eas-1029384756",
      "deployment_id": "62a9473a2dca46b29ccf17577fcf42d7",
      "connected_at": "2026-10-14T18:05:44.817Z",
      "updated_at": "2026-10-14T18:05:44.818Z",
      "is_first_party": false,
      "meta": {}
    }
  ]
}
```

The secondary `#sub-eas-` connection has no `active_in_party_voice_room` field.

_Example Error (party disbanded or unknown)_

`404`:

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
