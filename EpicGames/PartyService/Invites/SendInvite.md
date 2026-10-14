## Party Service - Invites: Send Party Invite

Invites a friend to the caller's current party (`send-party-invite`, `send-bulk-party-invite`, second half of `create-and-send-*`). The invitee only sees the invite in EGL when the inviter's presence is published ([Update Presence](../../PresenceService/Presence/UpdatePresence.md)); without it the inviter shows Offline and the invite is hidden.

URL: https://api.epicgames.dev/epic/party/internal/v2/users/:accountId/invites/:inviterId \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4, kept as the invite `correlationId` <br/>

## Path Parameters
`accountId`: Invitee account id <br/>
`inviterId`: The signed-in account id <br/>

## Query Parameters
`auto`: `true` for auto-invites, else `false` <br/>

No body.

Invites expire after one hour. Epic Connect then delivers `party.v2.INVITE_CREATED` to the inviter; when the invitee joins, the inviter receives `party.v2.INVITE_EXPIRED` followed by `party.v2.MEMBER_JOINED` ([README](../README.md#realtime-events)).

---

_Example Response_

```json
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
```
