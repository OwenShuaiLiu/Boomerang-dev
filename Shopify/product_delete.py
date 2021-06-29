import shopify
import requests
import json

API_KEY = "833fd488c5447c36b3f18caaec0df410"
PASSWORD = "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"
SHOP_NAME = "boomerangdev"
product_id = "5041798840451"

shop_url = "https://%s:%s@%s.myshopify.com/admin" % (API_KEY, PASSWORD, SHOP_NAME)

shopify.ShopifyResource.set_site(shop_url)
shop = shopify.Shop.current()

# delete a product
product_url = shop_url + "/api/2020-04/products/"+ product_id + ".json"

request_delete = requests.delete(url=product_url)

print(request_delete)