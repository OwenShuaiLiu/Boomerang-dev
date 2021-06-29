import shopify 
import requests
import json

API_KEY = "e87d5ebf9038b819f2f7979bbf92f301"
PASSWORD = "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"
SHOP_NAME = "epoque-store"
price_rule_id = "650259103846"

shop_url = "https://%s:%s@%s.myshopify.com/admin" % (API_KEY, PASSWORD, SHOP_NAME)

shopify.ShopifyResource.set_site(shop_url)
shop = shopify.Shop.current()

price_rule_url = shop_url + "/api/2020-04/price_rules.json"


#create a store credit code
store_credit_url = shop_url + "/api/2020-04/price_rules/" + price_rule_id + "/discount_codes.json"
new_store_credit_code = {
  "discount_code": {
    "code": "ONECENTOFF"
  }
}

headers = {'content-type': 'application/json'}
response = requests.post(url=store_credit_url, data=json.dumps(new_store_credit_code), headers= headers)
print(response.text)