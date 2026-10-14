## Store Content Service - Content: Product Mapping

Namespace to store slug map. `get_store_product_art` (`{ namespace }`) uses it to find the product page of a library title (`eglv2_lib::api::store_content`, cached in `cache/<env>/product-mapping-cache.json`; 1283 entries at the time of writing).

URL: https://store-content.ak.epicgames.com/api/content/productmapping \
Method: GET \
Auth Required: No

---

_Example Response_

```json
{
  "fn": "fortnite",
  "crab": "satisfactory",
  "min": "hades",
  "ark": "ark"
}
```
