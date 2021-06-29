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

# Create a new price rule
new_price_rule = {
  "price_rule": {
    "title": "StoreCreditForAll-test",
    "target_type": "line_item",
    "target_selection": "all",
    "allocation_method": "across",
    "value_type": "fixed_amount",
    "value": "-0.01",
    "customer_selection": "all",
    "starts_at": "2017-01-19T17:59:10Z",
    "usage_limit": 1
  }
}
headers = {'content-type': 'application/json'}

request_post = requests.post(url=price_rule_url, data=json.dumps(new_price_rule), headers= headers)

response_data = request_post.json()

print ("New price rule id is: ") 

print(response_data["price_rule"]["id"]) 

#print(response_data.text)