# Social Overlay - GraphQL

URL: https://api.epicgames.dev/overlay-graphql/v1/graphql \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

Headers: `X-Epic-Agent: epic-social`, `Authorization: Bearer <token>`, `credentials: include`. Client is urql; retries network errors, 408, 425, 429 and 5xx up to 5 attempts (500ms .. 150s backoff). Errors carry the upstream service response in `graphQLErrors[0].originalError.serviceResponse` (JSON string, parsed into an `UpstreamServiceError`).

## Friends operations

See [Friends Service](../../EpicGames/FriendsService/README.md) for one page per operation.

| Operation | Type | Page |
| --- | --- | --- |
| `friends` | query | [Get Friends](../../EpicGames/FriendsService/GraphQL/GetFriends.md) |
| `friend` | query | [Get Friend](../../EpicGames/FriendsService/GraphQL/GetFriend.md) |
| `inviteFriendRequest` | mutation | [Add Friend](../../EpicGames/FriendsService/GraphQL/AddFriend.md) |
| `deleteFriend` | mutation | [Delete Friend](../../EpicGames/FriendsService/GraphQL/DeleteFriend.md) |
| `block` | mutation | [Block](../../EpicGames/FriendsService/GraphQL/Block.md) |
| `blockMultipleUsers` | mutation | [Block Multiple](../../EpicGames/FriendsService/GraphQL/BlockMultiple.md) |
| `unblock` | mutation | [Unblock](../../EpicGames/FriendsService/GraphQL/Unblock.md) |
| `setAlias` | mutation | [Set Alias](../../EpicGames/FriendsService/GraphQL/SetAlias.md) |
| `deleteAlias` | mutation | [Delete Alias](../../EpicGames/FriendsService/GraphQL/DeleteAlias.md) |
| `privacySettings` | query | [Get Settings](../../EpicGames/FriendsService/GraphQL/GetSettings.md) |
| `setPrivacySettings` | mutation | [Set Settings](../../EpicGames/FriendsService/GraphQL/SetSettings.md) |

## Account operations

```graphql
query account($accountId: String) {
    Account {
        account(id: $accountId) {
            id
            displayName
            displayNameType
            externalAuths {
                type
                externalAuthId
                externalAuthIdType
                externalDisplayName
                authIds { id type }
            }
        }
    }
}
```

```graphql
query accounts($accountIds: [String!]!) {
    Account {
        accounts(accountIds: $accountIds) {
            id
            displayName
            displayNameType
            friendshipStatus
            externalAuths {
                type
                externalAuthId
                externalAuthIdType
                externalDisplayName
                authIds { id type }
            }
        }
    }
}
```

`accountIds` is sent in chunks of 100. `displayNameType: "HIDDEN"` marks a de-identified account.

```graphql
query account($accountId: String) {
    Account {
        account(id: $accountId) {
            id
            cabinedMode
        }
    }
}
```

A variant selecting only `id` and `externalAuths { type externalDisplayName }` feeds the linked-accounts view. `externalAuths[].type` values mapped by the app: `epic`, `nintendo`, `psn`, `steam`, `xbl`.

## Search

```graphql
query getSearchResultsByTerm($searchTerm: String, $platform: String) {
    ExtendedSearchResult {
        extendedSearch(searchTerm: $searchTerm, platform: $platform) {
            epicMutuals
            account {
                id
                displayName
                displayNameType
                externalAuths {
                    externalAuthIdType
                    externalAuthId
                    externalDisplayName
                    type
                    authIds { id type }
                }
            }
        }
    }
}
```

Search config defaults: 1000ms debounce, 3..16 characters. `epicMutuals` is a numeric string (mutual friend count).
