## Connect Service - WebSocket: Connect

Realtime STOMP channel. Full protocol: [Connect](../../Launcher/Social/Connect.md).

URL: wss://connect.ol.epicgames.com/ \
Method: GET (WebSocket upgrade) \
Auth Required: Yes (EG1 access token in the `auth-token` query parameter)

## Headers
`Sec-WebSocket-Protocol`: v12.stomp, v11.stomp, v10.stomp <br/>

## Query Parameters
`auth-token`: Elevated EG1 access token <br/>
`avatarFnDeploymentId`: `62a9473a2dca46b29ccf17577fcf42d7` <br/>
`accept-language`: Locale, e.g. `en-US` <br/>

STOMP: `CONNECT` with `accept-version: 1.2,1.1,1.0` and `heart-beat: 45000,0`, then `SUBSCRIBE` to `<uuid>/account/<accountId>`.
