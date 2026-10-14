## EOS Auth Service - OAuth: Token (v1)

Present in the launcher's environment table as `{epic_dev}/auth/v1/oauth/token` (built in `sub_140E00FD0`, stored at EndpointUrls +0x228). No Rust code path that sends a request to this URL was found; the EOS SDK carries the same path as its Connect `TokenExchange` call. Documented here so the table entry is accounted for.

URL: https://api.epicgames.dev/auth/v1/oauth/token \
Method: POST \
Auth Required: Yes (Basic Authentication where the username is the Client Id and the password is the Client Secret; standard for this endpoint, not traced in eglv2)

## Headers
`Content-Type`: application/x-www-form-urlencoded <br/>

## Body

Form field names present in the EOS SDK next to this path: `grant_type`, `deployment_id`, `sandbox_id`; grant values `client_credentials`, `external_auth`, `urn:ietf:params:oauth:grant-type:token-exchange`, plus `external_auth_type`, `external_auth_token`, `subject_token`, `subject_token_type`. Which of these eglv2 would send is not determined.

---

Needs a live capture to confirm whether eglv2 (or the SDK on its behalf) ever calls this URL.
