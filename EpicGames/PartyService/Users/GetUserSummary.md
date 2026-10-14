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

_Example Response (in a party; `current` is the party object from [Get Party](../Parties/GetParty.md), invite entries as returned by [Send Party Invite](../Invites/SendInvite.md); populated summary not captured)_

```json
{
  "current": {
    "id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "party_lead": "94b1569506b04f9f8557af611e8c5e47",
    "config": { "joinability": "INVITE_ONLY", "max_size": 16 },
    "meta": { "created_by": "94b1569506b04f9f8557af611e8c5e47" },
    "revision": 0,
    "chat_conversation_id": "ep-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "is_reportable": false,
    "members": []
  },
  "invites": [
    {
      "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
      "sent_by": "94b1569506b04f9f8557af611e8c5e47",
      "auto": false,
      "meta": {},
      "sent_to": "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b",
      "sent_at": "2026-10-14T16:53:45.315Z",
      "updated_at": "2026-10-14T16:53:45.315Z",
      "expires_at": "2026-10-14T17:53:45.315Z"
    }
  ],
  "join_requests": []
}
```
