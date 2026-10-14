# Epic Games Launcher v2

Notes on the Rust / Tauri Epic Games Launcher ("eglv2", reversed from `0.95.1+ge288862`). Service endpoints it calls are documented under [EpicGames](../EpicGames), [EpicGamesStore](../EpicGamesStore) and [ThirdParty](../ThirdParty); this folder covers the client itself.

## Overview

- [Architecture](Architecture.md): stack, windows / webviews, startup, local install API, telemetry, feature flags
- [Environments](Environments.md): prod / gamedev / ci host table, User-Agents, headers, overrides, changes from the UE launcher
- [Local Data](LocalData.md): files under `%LOCALAPPDATA%\com.epicgames.eglv2`
- [Deep Links](DeepLinks.md): `com.epicgames.launcher://` routes, partner hand-off URIs, external pages
- [Self Update](SelfUpdate.md): flags, stable target, `buildinfo.json`, update splash, what's new, v1 migration
- [IPC](IPC/README.md): every Tauri command, event and injected bridge

## Flows

- [Sign In](Flows/SignIn.md)
- [Library](Flows/Library.md)
- [Install And Update](Flows/InstallAndUpdate.md)
- [Game Launch](Flows/GameLaunch.md)
- [Purchase](Flows/Purchase.md)
- [Cloud Saves](Flows/CloudSaves.md)
- [Voice Chat](Flows/VoiceChat.md)

## Topics

- Auth: [Clients](Auth/Clients.md), [Token Storage](Auth/TokenStorage.md), [DPoP](Auth/DPoP.md), [EOS](Auth/EOS.md), [Cabined Mode](Auth/CabinedMode.md), [Account Links](Auth/AccountLinks.md), [V1 Carryover](Auth/V1Carryover.md), [IPC](Auth/IPC.md)
- Library: [Caching](Library/Caching.md), [Artwork](Library/Artwork.md), [External Sources](Library/ExternalSources.md)
- Social: [Overview](Social/Overview.md), [Bridge](Social/Bridge.md), [Connect](Social/Connect.md), [GraphQL](Social/GraphQL.md), [Signing](Social/Signing.md)
- Voice: [Reference Client](Voice/ReferenceClient.md), [RTC Signaling](Voice/RTCSignaling.md), [Media](Voice/Media.md), [Audio Signing](Voice/AudioSigning.md), [Moderation](Voice/Moderation.md), [Settings](Voice/Settings.md), [Native Bridge](Voice/NativeBridge.md)
