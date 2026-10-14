## Party Service - Invites: Decline Party Invite

Declines a received invite (`decline-party-invite`).

URL: https://api.epicgames.dev/epic/party/internal/v2/users/:accountId/invites/:inviterId \
Method: DELETE \
Auth Required: Yes (Bearer elevated EG1 access token, from `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: The signed-in account id <br/>
`inviterId`: Account id that sent the invite <br/>

No body.
