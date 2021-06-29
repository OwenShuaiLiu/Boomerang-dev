import shopify
import requests
import json

API_KEY = "833fd488c5447c36b3f18caaec0df410"
PASSWORD = "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"
SHOP_NAME = "boomerangdev"

shop_url = "https://%s:%s@%s.myshopify.com/admin" % (API_KEY, PASSWORD, SHOP_NAME)

shopify.ShopifyResource.set_site(shop_url)
shop = shopify.Shop.current()

product_url = shop_url + "/api/2020-04/products.json"

# Get all products
requestget = requests.get(url=product_url)

response_data = requestget.json()

print(response_data)

product_data = response_data["products"]

for data in product_data:
  print(str(data["id"]) + ' ' + str(data["title"]))