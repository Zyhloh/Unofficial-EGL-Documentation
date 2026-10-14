## Social Ban Service - Bans: Acknowledge Ban

Ack the current social ban. Sent after Get User Summary and on every `socialban.v1.BAN_APPLIED` Epic Connect message.

URL: https://social-ban-public-service-prod.social.live.on.epicgames.com/socialban/api/public/v1/:accountId/ban/ack \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: Your account id <br/>

---

_Example Response_: `204 No Content`
