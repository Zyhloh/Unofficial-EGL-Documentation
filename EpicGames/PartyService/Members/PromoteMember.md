## Party Service - Members: Promote Member

Makes another member party lead (`promote-party-member`).

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId/promote \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client; the overlay uses `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: Account id of the new lead <br/>

No body. Request not captured (sent by EGL); the resulting event was.

Every member receives `party.v2.PARTY_UPDATED` with the new `party_lead` and a bumped party `revision`; `meta.created_by` keeps the original creator. Captured after EGL promoted the other member:

```json
{
  "correlationId": "69ab9aeb-f268-470f-a991-0484d6dbda74",
  "timestamp": 1792000798420,
  "id": "NDk0NDU5OTc0OTQzMDg4Mg",
  "connectionId": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
  "payload": {
    "sent": "2026-10-14T17:59:58.420Z",
    "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "party_lead": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
    "meta": {
      "created_by": "94b1569506b04f9f8557af611e8c5e47"
    },
    "party_privacy_type": "INVITE_ONLY",
    "max_number_of_members": 16,
    "chat_conversation_id": "ep-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "created_at": "2026-10-14T17:58:53.823Z",
    "updated_at": "2026-10-14T17:59:58.419Z",
    "is_reportable": true,
    "revision": 4
  },
  "type": "party.v2.PARTY_UPDATED"
}
```

The new leader can then kick ([Leave Party / Kick Member](LeaveParty.md)) and change the config.
