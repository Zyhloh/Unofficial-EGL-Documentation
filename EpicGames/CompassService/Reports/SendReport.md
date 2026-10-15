## Compass Service - Reports: Send Report

Player / chat / voice reports from the overlay (intent `compass-send-report`, also the `reporting` feature).

URL: https://compass-service-prod.ecosec.on.epicgames.com/compass/v1/namespace/eos/new_social_overlay_report \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Body
Group chat report as sent by EGL, after [Upload Text Chat](../../EmeraldService/Text/Upload.md):

```json
{
  "reporter_entity_id": "94b1569506b04f9f8557af611e8c5e47",
  "offender_entity_id": "07c0ExampleGroupId0008",
  "reason": "group.chat",
  "emerald_token": "3e7b1c9d-5a2f-4d8e-b6c0-1f4a7e9d2b3c"
}
```

Body per report type:

| type | Fields |
| --- | --- |
| `user` | `offender_entity_id` (account id), `reason`, `reporter_entity_id` |
| `group.chat` | `reporter_entity_id`, `offender_entity_id` (conversation id), `reason`, `emerald_token` |
| `direct.messages` | `reporter_entity_id`, `offender_entity_id` (conversation id), `reason`, `emerald_token` |
| `group.invite` | `reporter_entity_id`, `offender_entity_id` (conversation id), `reason` |
| `voice` | `emerald_token`, `reason`, `product_id`, `reporter_entity_id` |

`reason` values used: `group.chat`, `direct.messages`, `group.invite`, `overlay.reporting.offensiveName`, `voice`.

---

_Example Response_ (`group.chat`)

```json
{
  "report_id": "9c2e4a6b-8d1f-4e3a-b5c7-0a2d4f6e8b1c",
  "product_id": "social_overlay",
  "report_reason": "terms_of_service",
  "report_state": "Pending Moderation",
  "report_status": "open",
  "creation_datetime": "2026-10-15T02:05:23.239987559Z",
  "last_updated": "2026-10-15T02:05:23.239987559Z",
  "reporter_entity_type": "epic_account",
  "offender_entity_type": "epic_account",
  "appeal_id": "",
  "appealed": false,
  "actioned": false,
  "is_appeal_in_review": false,
  "moderation_type": "badger",
  "execution_id": "5d7f9b1e-3a4c-4e6d-8f0b-2c4e6a8d0f1b",
  "product_report_type": "group.chat",
  "history": [
    {
      "id": "1a3c5e7f-9b2d-4f6a-8c0e-4b6d8f0a2c3e",
      "created_at": "2026-10-15T02:05:23.243171955Z",
      "updated_at": "2026-10-15T02:05:23.243196108Z",
      "report_id": "9c2e4a6b-8d1f-4e3a-b5c7-0a2d4f6e8b1c",
      "event": "created"
    }
  ],
  "platform_unique_identifier": "e4f6a8c0-2b3d-4e5f-9a1b-3c5d7e9f1a2b",
  "can_appeal": false,
  "appeal_unavailable_reason": "report_open",
  "has_sanction": false
}
```

The client only reads `report_id`. `offender_entity_type` is `epic_account` even though `offender_entity_id` is a conversation id. Reporting the same conversation twice created two separate open reports. Only `group.chat` was captured; the other report types are from the client code.
