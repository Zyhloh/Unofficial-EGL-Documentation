## Interactions Service - Interactions: Get Aggregated

Interaction scores between the account and other accounts. The social overlay (`its-api`, `getAggregatedInteractions`) uses them to rank friends. See [Social Overview](../../../Launcher/Social/Overview.md).

URL: https://api.epicgames.dev/epic/interactions/v2/interactions/aggregated/_/:accountId \
Method: GET \
Auth Required: Yes (Bearer access token, attached by the overlay's service fetch wrapper)

## Path Parameters
`accountId`: The account id

---

_Example Response (shape from client)_

```json
{
  "aggregatedInteractions": [
    {
      "toAccountId": "94b1569506b04f9f8557af611e8c5e47",
      "interactionScore": {
        "total": 12
      },
      "latestInteraction": {
        "happenedAt": "2026-10-14T15:18:54.216Z"
      }
    }
  ]
}
```
