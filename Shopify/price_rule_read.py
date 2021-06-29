import shopify 
import requests
import json

API_KEY = "833fd488c5447c36b3f18caaec0df410"
PASSWORD = "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"
SHOP_NAME = "boomerangdev"

shop_url = "https://%s:%s@%s.myshopify.com/admin" % (API_KEY, PASSWORD, SHOP_NAME)

shopify.ShopifyResource.set_site(shop_url)
shop = shopify.Shop.current()

price_rule_url = shop_url + "/api/2020-04/price_rules.json"

# Get all price rules id
request_get = requests.get(url=price_rule_url)

response_data = request_get.json()

#print(response_data.text)

price_rule_data = response_data["price_rules"]

for data in price_rule_data:
  print(data["id"])