# Epic Games Error Code

Example Error Response

```json
{
  "errorCode": "errors.com.epicgames.unauthorized",
  "errorMessage": "The request is missing authentication, or the authentication is no longer valid.",
  "numericErrorCode": 1002,
  "messageVars": [],
  "originatingService": "com.epicgames.account.public",
  "intent": "prod"
}
```

The launcher (Rust) reads `errorCode` and `numericErrorCode`. The social overlay reads `errorCode`, `errorMessage` and `messageVars`.

## Error Codes Handled By The Launcher

| Error Code                                                  | Where                      |
| ----------------------------------------------------------- | -------------------------- |
| `errors.com.epicgames.account.oauth.too_many_sessions`      | Sign in                    |
| `errors.com.epicgames.launcher.no_download_access`          | Install / assets           |
| `errors.com.epicgames.library.invalid_argument`             | Library                    |
| `errors.com.epicgames.library.invalid_time`                 | Library / playtime         |
| `errors.com.epicgames.partnerintegration.account_not_found` | Partner integration        |
| `errors.com.epicgames.unknown`                              | Fallback                   |

## Error Codes Handled By The Social Overlay

| Error Code                                                        | Where   |
| ----------------------------------------------------------------- | ------- |
| `errors.com.epicgames.social.party.party_not_found`               | Parties |
| `errors.com.epicgames.social.party.stale_revision`                | Parties |
| `errors.com.epicgames.social.party.user_has_party`                | Parties |
| `errors.com.epicgames.social.party.client_policy_unknown`         | Parties |
| `errors.com.epicgames.social.chat.group_conversation_limit_exceeded` | Chat |
| `errors.com.epicgames.social.chat.invite_accepted`                | Chat    |
| `errors.com.epicgames.social.chat.title_validation_failed`        | Chat    |
| `errors.com.epicgames.chat.group_conversation_limit_exceeded`     | Chat    |
| `errors.com.epicgames.chat.group_name_too_long`                   | Chat    |
| `errors.com.epicgames.chat.group_name_toxic`                      | Chat    |
| `errors.com.epicgames.friends.invites.invaliduser`                | Friends |
| `errors.com.epicgames.friends.cannot_friend_due_to_missing_pin`   | Friends |
| `errors.com.epicgames.friends.cannot_friend_due_to_invalid_pin`   | Friends |
| `errors.com.epicgames.friends.cannot_friend_due_to_pin_attempts_exceeded` | Friends |
| `errors.com.epicgames.lobbies.session_not_found`                  | Lobbies |
| `errors.com.epicgames.lobby.toomanyplayers`                       | Lobbies |
