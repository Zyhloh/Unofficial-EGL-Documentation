# Epic Games Launcher (v2) - API Documentation

Unofficial documentation of the services, endpoints and internal flows used by the new Epic Games Launcher.

Documented build: `0.95.1+ge288862` <br/>
Social overlay build: `48a8a998c785c6c7358b56ddc82474ca23ae565f` (`social-overlay@2.9.2`) <br/>
EOS SDK: `1.19.4230.0-57929184@LauncherV2`

## Getting started

The new launcher is a Rust ([Tauri](https://tauri.app)) application with a React frontend rendered in WebView2. Most Epic API calls are made by the Rust backend; friends, chat, parties and voice are handled by the hosted social overlay, which is loaded into its own webview from `https://api.epicgames.dev/overlay-override/v1/launcher-eglv2.html`.

All requests that require normal authentication require the `Authorization` header with the access token, like `bearer {accessToken}`. <br/>
Requests made by the social overlay use the launcher's EG1 access token and additionally send `X-Epic-Agent: epic-social` and a random `X-EPIC-CORRELATION-ID`.

Start with the [sign in flow](./Launcher/Flows/SignIn.md) to see how the launcher gets its tokens, and the [OAuth clients](./Launcher/Auth/Clients.md) it uses.

Errors follow the usual [Epic Games error format](./EpicGames/Errors.md).

## Content

- [Epic Games](./EpicGames)
  - [Account Service](./EpicGames/AccountService)
  - [Artifact Delivery Service](./EpicGames/ArtifactDeliveryService)
  - [Catalog Service](./EpicGames/CatalogService)
  - [Chat Service](./EpicGames/ChatService)
  - [Compass Service](./EpicGames/CompassService)
  - [Connect Service](./EpicGames/ConnectService)
  - [Emerald Service](./EpicGames/EmeraldService)
  - [EOS Auth Service](./EpicGames/EOSAuthService)
  - [Entitlement Service](./EpicGames/EntitlementService)
  - [Friends Service](./EpicGames/FriendsService)
  - [KWS](./EpicGames/KWS)
  - [Launcher Service](./EpicGames/LauncherService)
  - [Library Service](./EpicGames/LibraryService)
  - [Moderation Service](./EpicGames/ModerationService)
  - [Party Service](./EpicGames/PartyService)
  - [Presence Service](./EpicGames/PresenceService)
  - [Public Key Service](./EpicGames/PublicKeyService)
  - [RTC Service](./EpicGames/RTCService)
  - [SOCS Service](./EpicGames/SOCSService)
  - [Social Ban Service](./EpicGames/SocialBanService)
  - [Web APIs](./EpicGames/Web)
    - [Id](./EpicGames/Web/Id)
  - [Errors](./EpicGames/Errors.md)
- [Launcher](./Launcher)
  - [Flows](./Launcher/Flows)
    - [Sign In](./Launcher/Flows/SignIn.md)
    - [Game Launch](./Launcher/Flows/GameLaunch.md)
    - [Library](./Launcher/Flows/Library.md)
    - [Install And Update](./Launcher/Flows/InstallAndUpdate.md)
    - [Voice Chat](./Launcher/Flows/VoiceChat.md)
  - [Auth](./Launcher/Auth)
    - [Clients](./Launcher/Auth/Clients.md)
    - [Token Storage](./Launcher/Auth/TokenStorage.md)
    - [DPoP](./Launcher/Auth/DPoP.md)
    - [EOS](./Launcher/Auth/EOS.md)
    - [Cabined Mode](./Launcher/Auth/CabinedMode.md)
    - [Account Links](./Launcher/Auth/AccountLinks.md)
    - [V1 Carryover](./Launcher/Auth/V1Carryover.md)
    - [IPC](./Launcher/Auth/IPC.md)
  - [Library](./Launcher/Library)
    - [Caching](./Launcher/Library/Caching.md)
    - [Artwork](./Launcher/Library/Artwork.md)
    - [External Sources](./Launcher/Library/ExternalSources.md)
  - [Voice](./Launcher/Voice)
    - [Native Bridge](./Launcher/Voice/NativeBridge.md)
    - [RTC Signaling](./Launcher/Voice/RTCSignaling.md)
    - [Settings](./Launcher/Voice/Settings.md)
    - [Moderation](./Launcher/Voice/Moderation.md)
  - [Social Overlay](./Launcher/Social)
    - [Overview](./Launcher/Social/Overview.md)
    - [Bridge](./Launcher/Social/Bridge.md)
    - [Connect (WebSocket)](./Launcher/Social/Connect.md)
    - [GraphQL](./Launcher/Social/GraphQL.md)
    - [Message Signing](./Launcher/Social/Signing.md)

## Contributions

- Only contribute if you actually know what you are doing and talking about on the API / Operation
- Follow the formatting of the existing files (check the Markdown source)
- Include an example response (shortened), never real tokens or personal data
- Note the launcher build your changes are based on

## Honorable Mention

Huge thanks to [Lele](https://github.com/LeleDerGrasshalmi) and everyone who contributed to the [Epic Games / Fortnite Endpoints Documentation](https://github.com/LeleDerGrasshalmi/FortniteEndpointsDocumentation). It has documented the core Epic Games and Fortnite APIs for years and remains the go-to reference for anything outside the launcher. If a service you need is not covered here, check there first.

The structure and page formatting of this repository are taken directly from that project, so the two can be read side by side. All credit for the format goes to Lele.

## Disclaimer

This project is not affiliated with or endorsed by Epic Games, Inc.
