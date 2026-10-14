## Party Service - Users: Get Parties Summary

Current party, pending invites (both directions) and join requests of the signed-in user. Fetched on overlay start (`fetch-initial-party-data`), on `party.v2.MEMBER_REFRESH_SUMMARY`, before create/join (to leave the old party) and by `reconcile-active-party`. A standalone client calls it first and leaves `current` before creating a party (one party per account).

URL: https://api.epicgames.dev/epic/party/internal/v2/users/:accountId \
Method: GET \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: The signed-in account id <br/>

`current` is absent when not in a party. `invites` holds both directions; the client splits them on `sent_to` / `sent_by`.

---

_Example Response (not in a party)_

```json
{
  "invites": [],
  "join_requests": []
}
```

_Example Response (in a party you created)_

```json
{
  "current": {
    "id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "party_lead": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
    "created_at": "2026-10-14T17:57:26.752Z",
    "updated_at": "2026-10-14T17:57:26.752Z",
    "config": {
      "joinability": "INVITE_ONLY",
      "max_size": 16
    },
    "meta": {
      "created_by": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"
    },
    "revision": 0,
    "chat_conversation_id": "ep-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "is_reportable": false,
    "members": [
      {
        "account_id": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
        "meta": {},
        "revision": 0,
        "updated_at": "2026-10-14T17:57:26.758Z",
        "joined_at": "2026-10-14T17:57:26.758Z",
        "suspended": false,
        "connections": [
          {
            "id": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
            "deployment_id": "_",
            "connected_at": "2026-10-14T17:57:26.757Z",
            "updated_at": "2026-10-14T17:57:26.752Z",
            "is_first_party": true,
            "meta": {
              "osName": "Windows",
              "platformName": "egs",
              "productName": "Epic Games Launcher"
            },
            "active_in_party_voice_room": false
          }
        ]
      }
    ]
  },
  "invites": [],
  "join_requests": []
}
```

`current` is the full [Get Party](../Parties/GetParty.md) object.

_Example Response (not in a party, one pending invite received)_

```json
{
  "invites": [
    {
      "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
      "sent_by": "94b1569506b04f9f8557af611e8c5e47",
      "auto": false,
      "meta": {},
      "sent_to": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
      "sent_at": "2026-10-14T17:58:54.041Z",
      "updated_at": "2026-10-14T17:58:54.041Z",
      "expires_at": "2026-10-14T18:58:54.041Z"
    }
  ],
  "join_requests": []
}
```

Pending invites expire after one hour (`expires_at`); accept with [Join Party](../Members/JoinParty.md), reject with [Decline Party Invite](../Invites/DeclineInvite.md). A `join_requests` entry was not captured (inferred: same fields as the [Send Join Request](../JoinRequests/SendJoinRequest.md) response).
