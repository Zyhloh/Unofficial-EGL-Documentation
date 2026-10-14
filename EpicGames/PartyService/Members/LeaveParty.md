## Party Service - Members: Leave Party / Kick Member

Same route for leaving (`leave-party`, own id) and kicking (`kick-party-member`, other member). `404 errors.com.epicgames.social.party.party_not_found` is ignored when leaving before create/join.

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId \
Method: DELETE \
Auth Required: Yes (Bearer elevated EG1 access token, from `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: Own account id to leave, another member to kick <br/>

No body. Only the status is checked.
