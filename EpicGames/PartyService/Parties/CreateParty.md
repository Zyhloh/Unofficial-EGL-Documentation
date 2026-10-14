## Party Service - Parties: Create Party

Creates a party and joins it with the caller's Epic Connect connection. Intents `create-party`, `create-group-party`, `create-and-send-party-invite`, `create-and-send-auto-invite`. The client first leaves any current party (summary + leave).

URL: https://api.epicgames.dev/epic/party/internal/v2/parties \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token, from `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Body
```json
{
  "config": {
    "joinability": "OPEN",
    "max_size": 16
  },
  "meta": {
    "created_by": "94b1569506b04f9f8557af611e8c5e47"
  },
  "join_info": {
    "connection": {
      "id": "b1e2c3d4a5f60718293a4b5c6d7e8f90",
      "deployment_id": "d0e1f2a3b4c5d6e7f8091a2b3c4d5e6f",
      "meta": {
        "osName": "Windows",
        "platformName": "egs",
        "productName": "Epic Games Launcher"
      }
    }
  }
}
```

`join_info.connection.id` is the Epic Connect connection id (`core.connect.v1.connected` `connectionId`). `deployment_id`, `osName`, `platformName`, `productName` come from the native app info. Group parties send `source_chat_conversation_id` with `config: { joinability: "INVITE_ONLY", max_size: 16 }`. `max_size` is always `16` in this build.

`409 errors.com.epicgames.social.party.user_has_party` makes `create-and-send-auto-invite` adopt `current` from the summary instead.

---

_Example Response (shape from client)_

```json
{
  "id": "a3f6c2d1e9b84f7a8c5d0e1f2a3b4c5d",
  "created_at": "2026-10-14T16:00:00.000Z",
  "updated_at": "2026-10-14T16:00:00.000Z",
  "is_reportable": true,
  "chat_conversation_id": "ep-a3f6c2d1e9b84f7a8c5d0e1f2a3b4c5d",
  "source_chat_conversation_id": null,
  "meta": {
    "created_by": "94b1569506b04f9f8557af611e8c5e47"
  },
  "revision": 1,
  "members": [
    {
      "account_id": "94b1569506b04f9f8557af611e8c5e47",
      "connections": [
        {
          "id": "b1e2c3d4a5f60718293a4b5c6d7e8f90",
          "connected_at": "2026-10-14T16:00:00.000Z",
          "updated_at": "2026-10-14T16:00:00.000Z",
          "is_first_party": true,
          "local_play_enabled": false,
          "account_pl": "egs",
          "account_pl_dn": "Player",
          "meta": {
            "osName": "Windows",
            "platformName": "egs",
            "productName": "Epic Games Launcher"
          }
        }
      ],
      "joined_at": "2026-10-14T16:00:00.000Z",
      "updated_at": "2026-10-14T16:00:00.000Z",
      "meta": {
        "active_voice_connection": "b1e2c3d4a5f60718293a4b5c6d7e8f90",
        "platform_name": "Windows",
        "product_name": "Epic Games Launcher"
      },
      "revision": 2,
      "suspended": false
    }
  ],
  "party_lead": "94b1569506b04f9f8557af611e8c5e47",
  "config": {
    "joinability": "OPEN",
    "max_size": 16,
    "discoverability": "..."
  }
}
```
