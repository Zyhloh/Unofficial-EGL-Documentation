## Order Processor Service - Orders: Quick Purchase

Fast path for offers that need no payment. `bridge_request_purchase` (store `RequestPurchase`) tries it first; when the order needs a real checkout the launcher opens the `checkout-overlay`. See [Purchase](../../../Launcher/Flows/Purchase.md).

URL: https://orderprocessor-public-service-ecomprod01.ol.epicgames.com/orderprocessor/api/shared/accounts/:accountId/orders/quickPurchase \
Method: POST \
Auth Required: Yes (Bearer access token)

## Headers
`Content-Type`: application/json <br/>

## Path Parameters
`accountId`: The account id

## Body
```json
{
  "salesChannel": "Windows-Store-EGSLauncher",
  "entitlementSource": "Windows-Store-EGSLauncher",
  "returnSplitPaymentItems": false,
  "lineOffers": [
    {
      "offerId": "94b1569506b04f9f8557af611e8c5e47",
      "quantity": 1,
      "namespace": "94b1569506b04f9f8557af611e8c5e47"
    }
  ]
}
```

Field names come from `QuickPurchaseRequest` / `QuickPurchaseLineOffer`. `Windows-Store-EGSLauncher` is the only literal set on the request; using it for `entitlementSource` as well is inferred. The request log line also carries `country=`; where the country is sent was not recovered.

---

_Example Response_

```json
{
  "quickPurchaseStatus": "CHECKOUT"
}
```

Tested live (November 2026) with the body above and a plain account access token: both a weekly free game (price 0 during the promotion) and a free-to-play base game (Rocket League, base offer price 0) answered `200 {"quickPurchaseStatus":"CHECKOUT"}` and granted nothing; the library was unchanged afterwards. `CHECKOUT` tells the launcher to open the `checkout-overlay` instead. Which offers complete here without checkout was not found.

Errors are read as `OrderErrorEnvelope` (`numericErrorCode`). `2007` (subscription) routes to the checkout overlay (`quickPurchase rejected with numeric error 2007 (subscription); routing to checkout overlay`).
