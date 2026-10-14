## Connect Service - WebSocket: Connect

Realtime STOMP channel. Its connection id is the party connection id and the presence connection id. Full protocol: [Connect](../../Launcher/Social/Connect.md).

URL: wss://connect.ol.epicgames.com/ \
Method: GET (WebSocket upgrade) \
Auth Required: Yes (EG1 access token from any client, in the `auth-token` query parameter)

## Headers
`Sec-WebSocket-Protocol`: v12.stomp, v11.stomp, v10.stomp (sent by the overlay; a client without it also works) <br/>

## Query Parameters
`auth-token`: EG1 access token <br/>
`avatarFnDeploymentId`: `62a9473a2dca46b29ccf17577fcf42d7` (overlay only, optional) <br/>
`accept-language`: Locale, e.g. `en` or `en-US` <br/>

## Frames

Client:
```
CONNECT
accept-version:1.2,1.1,1.0
heart-beat:45000,0

^@
```

Server:
```
CONNECTED
version:1.2
heart-beat:0,45000
session:3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d

^@
```

Client:
```
SUBSCRIBE
id:sub-0
destination:20d0a958-8dd0-490a-bb7f-fe8939e7be44/account/94b1569506b04f9f8557af611e8c5e47

^@
```

`^@` is the NUL terminator. `session` is the connection id. The destination prefix is a random UUID per client. Server frames can arrive as binary WebSocket messages; decode as UTF-8. Send a heartbeat (`\n`) at least every 45s.
