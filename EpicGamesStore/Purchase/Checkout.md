## Epic Games Store - Purchase: Checkout Page

Checkout page loaded into the `checkout-overlay` webview by `bridge_request_purchase` / `bridge_request_purchase_cart` when quick purchase does not apply. The overlay is single-instance; the launcher injects a purchase bridge (`window.ue.purchaseflow.requestclose`) and waits for `bridge_checkout_complete`. See [Purchase](../../Launcher/Flows/Purchase.md).

URL: https://launcher.store.epicgames.com/purchase \
Method: GET \
Auth Required: Yes (store session set from the EG1 token; without one `loading purchase page unauthenticated (will 400)`)

## Query Parameters
`showNavigation`: `true` <br/>
`highlightColor`: Accent colour <br/>
`locale`: UI locale <br/>
`offers`: One per line offer, `{quantity}-{namespace}-{offerId}-{x}-{y}`. `{x}` and `{y}` come from two optional line-offer fields and are empty when unset (which fields was not resolved) <br/>

Outcomes reported to the launcher: `succeeded`, `user_canceled`, `user_canceled_nav_away`, `failed` (store vocabulary `WasSuccessful`, `UserCanceled`, `PurchaseFailed`, `LoadFailure`).
