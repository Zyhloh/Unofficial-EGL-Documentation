# Hosts

This are some (not all) Hosts that you can access the Friends Service from

- api.epicgames.dev (`/overlay-graphql/v1/graphql`)
- api-gamedev.ol.epicgames.net (`/overlay-graphql/v1/graphql`, gamedev)

<br/>

Recommended Hosts:

- api.epicgames.dev

The EGL v2 social overlay does not call a REST friends API; every friends read and write is a GraphQL operation on the overlay GraphQL gateway. Realtime changes arrive over Epic Connect as `friends.v1.*` messages ([Connect](../../Launcher/Social/Connect.md)). Account lookup and search operations on the same gateway are listed in [GraphQL](../../Launcher/Social/GraphQL.md).
