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
```json
{
  "reporter_entity_id": "94b1569506b04f9f8557af611e8c5e47",
  "offender_entity_id": "d3c0f4e2-5b7a-4c1e-9f0a-7e2b6c1d8a90",
  "reason": "group.chat",
  "emerald_token": "..."
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

_Example Response (shape from client; only `report_id` is read)_

```json
{
  "report_id": "..."
}
```
