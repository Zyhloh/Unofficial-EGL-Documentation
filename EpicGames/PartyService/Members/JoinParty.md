## Party Service - Members: Join Party

Joins a party (`accept-party-invite`, accepted join request, join from presence). The client leaves a different current party first, then calls [Get Party](../Parties/GetParty.md) with the returned id.

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId/join \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client; the overlay uses `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: the invite correlation id when joining from an invite, else random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: The signed-in account id <br/>

## Body
```json
{
  "connection": {
    "id": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
    "deployment_id": "_",
    "meta": {
      "osName": "Windows",
      "platformName": "egs",
      "productName": "Epic Games Launcher"
    }
  }
}
```

`connection` is the joiner's Epic Connect connection, same shape as [Create Party](../Parties/CreateParty.md) `join_info.connection`. Accepted live from a standalone client (2026-10-14).

Works for a pending invite ([Send Party Invite](../Invites/SendInvite.md)) and after the leader accepted a [join request](../JoinRequests/SendJoinRequest.md) (which is an invite). Events right after a join: `party.v2.MEMBER_JOINED` (joiner, `revision 0`, empty `member_state_updated`), `party.v2.INVITE_EXPIRED` (the consumed invite, now with `meta: {}`), `social.chat.v1.MEMBERS_JOIN` for `ep-<partyId>`. The joiner's member has `meta: {}` and `active_in_party_voice_room: false` until it [claims voice](UpdateMemberMeta.md).

---

_Example Response_

```json
{
  "status": "JOINED",
  "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f"
}
```
