## Party Service - Users: Get Parties Summary

Current party, pending invites (both directions) and join requests of the signed-in user. Fetched on overlay start (`fetch-initial-party-data`), on `party.v2.MEMBER_REFRESH_SUMMARY`, before create/join (to leave the old party) and by `reconcile-active-party`.

URL: https://api.epicgames.dev/epic/party/internal/v2/users/:accountId \
Method: GET \
Auth Required: Yes (Bearer elevated EG1 access token, from `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: The signed-in account id <br/>

`current` is absent when not in a party. `invites` holds both directions; the client splits them on `sent_to` / `sent_by`.

---

_Example Response (shape from client)_

```json
{
  "current": {
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
  },
  "invites": [
    {
      "sent_by": "1b8b8b2f4f3a4e6c9d0e5a7f2c4b6d81",
      "sent_to": "94b1569506b04f9f8557af611e8c5e47",
      "party_id": "a3f6c2d1e9b84f7a8c5d0e1f2a3b4c5d",
      "expires_at": "2026-10-15T16:00:00.000Z",
      "auto": false,
      "group_id": null
    }
  ],
  "join_requests": [
    {
      "requester_id": "1b8b8b2f4f3a4e6c9d0e5a7f2c4b6d81",
      "expires_at": "2026-10-14T16:05:00.000Z",
      "auto": false
    }
  ]
}
```
