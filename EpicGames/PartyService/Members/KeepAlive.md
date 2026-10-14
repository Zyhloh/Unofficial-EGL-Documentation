## Party Service - Members: Keep Alive

Revives the signed-in member after the service marked it `suspended`. Not on a timer: the party chat panel fires `party-keep-alive-request` whenever the local member of the active party has `suspended: true` (set from `party.v2.MEMBER_DISCONNECTED` / `MEMBER_STATE_UPDATED`).

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId/keep-alive \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client; the overlay uses `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: The signed-in account id <br/>

No body. The parsed response is not read.
