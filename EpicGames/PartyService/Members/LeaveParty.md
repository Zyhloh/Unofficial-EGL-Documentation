## Party Service - Members: Leave Party / Kick Member

Same route for leaving (`leave-party`, own id) and kicking (`kick-party-member`, other member). `404 errors.com.epicgames.social.party.party_not_found` is ignored when leaving before create/join. A standalone voice client calls it on shutdown after releasing voice ([Update Member Meta](UpdateMemberMeta.md) with `active_in_party_voice_room: false`).

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId \
Method: DELETE \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: Own account id to leave, another member to kick <br/>

No body. Only the status is checked.

Remaining members receive `party.v2.MEMBER_LEFT` (payload carries the leaver's last `member_state_updated`). `party.v2.MEMBER_EXPIRED_PARTY_DISBANDED` was also seen during a two-member party teardown; exact trigger not isolated.
