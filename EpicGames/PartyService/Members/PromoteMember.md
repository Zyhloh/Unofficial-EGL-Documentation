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

No body.
