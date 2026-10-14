## Party Service - Parties: Create Party

Creates a party and joins it with the caller's Epic Connect connection. Intents `create-party`, `create-group-party`, `create-and-send-party-invite`, `create-and-send-auto-invite`. An account can be in one party only: leave `current` from [Get Parties Summary](../Users/GetUserSummary.md) first ([Leave Party](../Members/LeaveParty.md)).

URL: https://api.epicgames.dev/epic/party/internal/v2/parties \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Body
```json
{
  "config": {
    "joinability": "INVITE_ONLY",
    "max_size": 16
  },
  "meta": {
    "created_by": "94b1569506b04f9f8557af611e8c5e47"
  },
  "join_info": {
    "connection": {
      "id": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
      "deployment_id": "_",
      "meta": {
        "osName": "Windows",
        "platformName": "egs",
        "productName": "Epic Games Launcher"
      }
    }
  }
}
```

`join_info.connection.id` is the Epic Connect connection id (STOMP `CONNECTED` `session` header / `core.connect.v1.connected` `connectionId`, see [Connect](../../../Launcher/Social/Connect.md)). EGL sends `deployment_id: "_"`. `joinability` is `OPEN` or `INVITE_ONLY`; `max_size` is always `16` in this build. Group parties also send `source_chat_conversation_id`.

`409 errors.com.epicgames.social.party.user_has_party` when the account already has a party; `create-and-send-auto-invite` then adopts `current` from the summary.

Realtime events that follow on Epic Connect: `social.chat.v1.CONVERSATION_CREATED` (`ep-<partyId>`), `social.chat.v1.REPORTABILITY_CHANGE`, `party.v2.MEMBER_JOINED` for the creator.

---

_Example Response_

```json
{
  "id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
  "party_lead": "94b1569506b04f9f8557af611e8c5e47",
  "created_at": "2026-10-14T16:53:45.111Z",
  "updated_at": "2026-10-14T16:53:45.111Z",
  "config": {
    "joinability": "INVITE_ONLY",
    "max_size": 16
  },
  "meta": {
    "created_by": "94b1569506b04f9f8557af611e8c5e47"
  },
  "revision": 0,
  "chat_conversation_id": "ep-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
  "is_reportable": false,
  "members": [
    {
      "account_id": "94b1569506b04f9f8557af611e8c5e47",
      "meta": {},
      "revision": 0,
      "updated_at": "2026-10-14T16:53:45.116Z",
      "joined_at": "2026-10-14T16:53:45.116Z",
      "suspended": false,
      "connections": [
        {
          "id": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
          "deployment_id": "_",
          "connected_at": "2026-10-14T16:53:45.116Z",
          "updated_at": "2026-10-14T16:53:45.111Z",
          "is_first_party": true,
          "meta": {
            "osName": "Windows",
            "platformName": "egs",
            "productName": "Epic Games Launcher"
          },
          "active_in_party_voice_room": false
        }
      ]
    }
  ]
}
```

`members[].revision` is the value the first [Update Member Meta](../Members/UpdateMemberMeta.md) must send.
