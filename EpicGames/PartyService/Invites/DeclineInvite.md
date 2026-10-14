## Party Service - Invites: Decline Party Invite

Declines a received invite (`decline-party-invite`).

URL: https://api.epicgames.dev/epic/party/internal/v2/users/:accountId/invites/:inviterId \
Method: DELETE \
Auth Required: Yes (Bearer EG1 access token, any client; the overlay uses `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: The signed-in account id <br/>
`inviterId`: Account id that sent the invite <br/>

No body.

Response `204 No Content` (confirmed live). The invite is consumed and the invitee receives `party.v2.INVITE_EXPIRED` (same event as when an invite is accepted):

```json
{
  "correlationId": "ebbc5056-8ba2-4da0-aebc-2195351554a5",
  "timestamp": 1792001131149,
  "id": "N2EwZjM4MzI1MWFkZTAzMg",
  "connectionId": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
  "payload": {
    "sent": "2026-10-14T18:05:31.149Z",
    "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
    "inviter_id": "94b1569506b04f9f8557af611e8c5e47",
    "inviter_dn": "ExampleUser",
    "invitee_id": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
    "sent_at": "2026-10-14T18:05:30.901Z",
    "updated_at": "2026-10-14T18:05:30.901Z",
    "expires_at": "2026-10-14T19:05:30.901Z",
    "auto": false,
    "meta": {}
  },
  "type": "party.v2.INVITE_EXPIRED"
}
```
