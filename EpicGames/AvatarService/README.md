# Hosts

This are some (not all) Hosts that you can access the Avatar Service from

- api.epicgames.dev (base path `/epic/avatar`)
- avatars-service-prod.social.live.on.epicgames.com (used by the social overlay before November 2026)

<br/>

Recommended Hosts:

- api.epicgames.dev

The social overlay shows Fortnite outfit avatars for the signed-in account, friends, party members and group chat members. Every route takes the avatars deployment id; the overlay uses `9c9906b240c74a92a6b9100d6e4ccbd0` (`EPIC_AVATARS_FN_DEPLOYMENT_ID`). Requests carry the account's EG1 access token (the overlay's "elevated" token) and `X-Epic-Agent: epic-social`; an EOS token from `/epic/oauth/v2/token` is rejected with 401. The service names itself `avatar-service-v2-api` in errors.

Avatar image URLs contain `{}` where the client puts the wanted height in pixels, e.g. `.../cdn-cgi/image/height=64,format=png/v1/item/...`.

- [Avatar Settings](Avatars/Settings.md)
- [Fallback Avatar](Avatars/Fallback.md)
- [Friends Assignments](Avatars/FriendsAssignments.md)
- [Party Assignments](Avatars/PartyAssignments.md)
- [Group Assignments](Avatars/GroupAssignments.md)
