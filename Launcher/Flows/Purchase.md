# Purchase

How a purchase started in the Store webview completes. Rust: `eglv2_lib::api::purchase`, `commands::purchase`, `commands::checkout`, `commands::launcher_bridge`, `commands::store_auth`. The store page drives it through the injected store bridge (`store-bridge.js`, see [Events](../IPC/Events.md#bridge-objects-in-content-webviews)).

## Store sign-in

The store is a remote page (`https://store.epicgames.com`) in the `store-webview` child webview. On Windows the launcher registers a WebView2 request filter for the store host and adds `Authorization: Bearer <EG1 access token>` to the document navigation (`Store.AuthHeaderFilterAdded`, `Store.AuthHeaderDocument`, `Store.AuthHeaderSubresource`; it never overrides an `Authorization` the page set itself). When the header lands it emits `store-auth-injected-event`. The page also reads the token and user through `ue.launcher.getaccesstoken` (`bridge_get_access_token`) and `ue.common.getsignedinuser` (`bridge_get_signed_in_user`). `bridge_get_client_version` advertises client version `19.0.0` and API versions `purchase`, `signin`, `layout` = `1.0.0`; the store gates its purchase flow on `apiversions.purchase`.

Staff builds can load the EGS v2 store behind Cloudflare Access instead (`egsZeroTrust` setting, `egs_zero_trust` command, popup `egs-zero-trust-signin` to `epicgamesinc.cloudflareaccess.com`, `CF_Authorization` cookie).

## Steps

1. User clicks Get / Buy. The store calls `window.ue.webmarketplace.requestpurchase([{ offernamespace, offerid, ... }])` (all casings and `RequestPurchaseV2` map to the same function) or `requestpurchasecart(cart)`.
2. The bridge invokes `bridge_request_purchase` (`{ offers }`) or `bridge_request_purchase_cart` (`{ cart }`); the store awaits one Promise.
3. Native tries [Quick Purchase](../../EpicGames/OrderProcessorService/Orders/QuickPurchase.md) (`Checkout.QuickPurchaseRequested`). If the order completes, the result goes straight back to the store.
4. If the order needs checkout (`Checkout.QuickPurchaseNeedsCheckout`, e.g. numeric error `2007` for subscriptions), the launcher opens the single-instance `checkout-overlay` webview on the [Checkout Page](../../EpicGamesStore/Purchase/Checkout.md) with `showNavigation=true`, `highlightColor`, `locale` and one `offers` value per line offer. `checkout-overlay-visibility-event` tells the shell to dim.
5. The checkout page ends with `window.ue.purchaseflow.requestclose(reason)`; the overlay bridge calls `bridge_checkout_complete` (`{ reason }`: `WasSuccessful`, `UserCanceled`, `PurchaseFailed`, `LoadFailure`). Outcome codes logged: `succeeded`, `user_canceled`, `user_canceled_nav_away`, `failed`.
6. The Promise from step 2 resolves; on success the launcher refreshes the library, adds an optimistic tile from the offer art (`Post-purchase offer art resolved`) and emits `Store.PurchaseCompleted`.
7. If the checkout ended without success, a short late-grant watch keeps polling ownership (`Purchase granted after its checkout ended without success; refreshing the library` / `No late grant seen after the checkout ended`).

`bridge_open_native_library` (`{ offerId, sandboxId, sort, url }`) lets the store jump to the owned title in the native library (`open-native-library-event`).

Fab purchases use Fab's own in-page checkout (`fab.com/payment/web/purchase?offers=...`) and do not go through this flow.
