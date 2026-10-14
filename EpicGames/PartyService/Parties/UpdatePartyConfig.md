## Party Service - Parties: Update Party Config

Changes party privacy (`update-party-config`, Open / Invite only toggle).

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId \
Method: PATCH \
Auth Required: Yes (Bearer EG1 access token, any client; the overlay uses `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>

## Body
```json
{
  "config": {
    "joinability": "OPEN",
    "max_size": 16
  },
  "revision": 0
}
```

`config` is the client's config object with `joinability` replaced, `revision` the current party `revision` (from [Get Party](GetParty.md), `0` for a new party). The overlay only checks the status.

Members receive `party.v2.PARTY_UPDATED`. A config change carries `author_id` and the `party_state_*` fields that the voice / lead updates leave out; `party_privacy_type` is the new joinability:

```json
{
  "correlationId": "7d5c9168-1f18-4eed-a757-df0a638fa27e",
  "timestamp": 1792000647163,
  "id": "NTRiOTNhNjM3MDNjNjk2Mg",
  "connectionId": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
  "payload": {
    "sent": "2026-10-14T17:57:27.163Z",
    "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "author_id": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
    "party_lead": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
    "party_state_removed": [],
    "meta": {
      "created_by": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"
    },
    "party_state_updated": {},
    "party_state_overridden": {},
    "party_privacy_type": "OPEN",
    "max_number_of_members": 16,
    "chat_conversation_id": "ep-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "created_at": "2026-10-14T17:57:26.752Z",
    "updated_at": "2026-10-14T17:57:27.163Z",
    "is_reportable": false,
    "revision": 1
  },
  "type": "party.v2.PARTY_UPDATED"
}
```

---

_Example Response_

```json
{
  "id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
  "party_lead": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "created_at": "2026-10-14T17:57:26.752Z",
  "updated_at": "2026-10-14T17:57:27.163Z",
  "config": {
    "joinability": "OPEN",
    "max_size": 16
  },
  "meta": {
    "created_by": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"
  },
  "revision": 1,
  "chat_conversation_id": "ep-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
  "is_reportable": false
}
```

The party object without `members`; `revision` is incremented.
