## Interactions Service - Interactions: Get Aggregated

Interaction scores between the account and other accounts. The social overlay (`its-api`, `getAggregatedInteractions`) uses them to rank friends. See [Social Overview](../../../Launcher/Social/Overview.md).

URL: https://api.epicgames.dev/epic/interactions/v2/interactions/aggregated/_/:accountId \
Method: GET \
Auth Required: Yes (Bearer access token, attached by the overlay's service fetch wrapper)

## Path Parameters
`accountId`: The account id

---

_Example Response (shortened)_

```json
{
  "aggregatedInteractions": [
    {
      "fromAccountId": "94b1569506b04f9f8557af611e8c5e47",
      "toAccountId": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
      "latestInteraction": {
        "interactionType": "PartyJoined",
        "happenedAt": 1793747888053,
        "app": "party-90d-230"
      },
      "interactionScore": {
        "total": 60,
        "count": 9
      },
      "interactionCount": 9
    },
    {
      "fromAccountId": "94b1569506b04f9f8557af611e8c5e47",
      "toAccountId": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f",
      "latestInteraction": {
        "interactionType": "FriendshipDelete",
        "happenedAt": 1786387901192
      },
      "interactionScore": {
        "total": 90,
        "count": 2
      },
      "interactionCount": 2
    }
  ]
}
```

`happenedAt` is epoch milliseconds. `interactionType` values seen live: `PartyJoined` (with an `app` tag) and `FriendshipDelete`. Accounts you removed as friends stay in the list, some with a zero score. The entries are not sorted.
