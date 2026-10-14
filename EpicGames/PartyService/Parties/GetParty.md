## Party Service - Parties: Get Party

Fetches one party. Used by `get-party`, `get-bulk-parties` (one call per id), join (after the join POST), `refresh-active-party-voice-check` and the stale-revision retry of member meta.

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId \
Method: GET \
Auth Required: Yes (Bearer elevated EG1 access token, from `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>

| Field | Notes |
| --- | --- |
| `members[].connections[]` | `disconnected_at` is set on dead connections; the client keeps only live ones. `is_first_party` and `meta.osName` / `meta.platformName` feed the voice-claim logic |
| `members[].meta` | member state; voice keys are `active_voice_connection`, `platform_name`, `product_name` |
| `meta` | party state; the client writes `created_by` |
| `config.joinability` | `OPEN` / `INVITE_ONLY` |
| `config.discoverability` | read, values not seen in the client |
| `is_reportable` | gates the voice report UI |

---

_Example Response (shape from client)_

```json
{
  "id": "a3f6c2d1e9b84f7a8c5d0e1f2a3b4c5d",
  "created_at": "2026-10-14T16:00:00.000Z",
  "updated_at": "2026-10-14T16:00:00.000Z",
  "is_reportable": true,
  "chat_conversation_id": "ep-a3f6c2d1e9b84f7a8c5d0e1f2a3b4c5d",
  "source_chat_conversation_id": null,
  "meta": {
    "created_by": "94b1569506b04f9f8557af611e8c5e47"
  },
  "revision": 1,
  "members": [
    {
      "account_id": "94b1569506b04f9f8557af611e8c5e47",
      "connections": [
        {
          "id": "b1e2c3d4a5f60718293a4b5c6d7e8f90",
          "connected_at": "2026-10-14T16:00:00.000Z",
          "updated_at": "2026-10-14T16:00:00.000Z",
          "is_first_party": true,
          "local_play_enabled": false,
          "account_pl": "egs",
          "account_pl_dn": "Player",
          "meta": {
            "osName": "Windows",
            "platformName": "egs",
            "productName": "Epic Games Launcher"
          }
        }
      ],
      "joined_at": "2026-10-14T16:00:00.000Z",
      "updated_at": "2026-10-14T16:00:00.000Z",
      "meta": {
        "active_voice_connection": "b1e2c3d4a5f60718293a4b5c6d7e8f90",
        "platform_name": "Windows",
        "product_name": "Epic Games Launcher"
      },
      "revision": 2,
      "suspended": false
    }
  ],
  "party_lead": "94b1569506b04f9f8557af611e8c5e47",
  "config": {
    "joinability": "OPEN",
    "max_size": 16,
    "discoverability": "..."
  }
}
```
