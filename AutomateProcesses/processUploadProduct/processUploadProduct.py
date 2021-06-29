import shopify
import requests
import json
from datetime import datetime
from datetime import timedelta 

from airtable import Airtable

# read response from airtable
airtable_item = Airtable('appIk8SiAeeLxVI3C', 'Items', api_key='keyoeqwCB4RoJUAtB')
data = airtable_item.get_all(formula="FIND('cleaned - to be uploaded', {Status})=1")

print(data)

for item in data:
    if item['fields']['Brand name'] == "boomerangdev":
        API_KEY = "833fd488c5447c36b3f18caaec0df410"
        PASSWORD = "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"
        SHOP_NAME = "boomerangdev"

        shop_url = "https://%s:%s@%s.myshopify.com/admin" % (API_KEY, PASSWORD, SHOP_NAME)

        shopify.ShopifyResource.set_site(shop_url)
        shop = shopify.Shop.current()

        product_url = shop_url + "/api/2020-04/products.json"

        # Create a new product
        new_product ={ 
            "product": { 
                "title": item['fields']['Title'], 
                "body_html": "<strong>{item['fields']['Title']}</strong>", 
                "vendor": item['fields']['Brand name'], 
                "product_type": item['fields']['Category'],
                "tags": ["Vintage", item['fields']['Category']],
                "variants": [
                    {
                        "inventory_quantity": 1,
                        "price": item['fields']['Selling price'],
                        "sku": item['fields']['SKU']
                    }
                ],
                "images": [{"src": item['fields']['Shop pictures'][0]['url']}]
                }
            }

        headers = {'content-type': 'application/json'}
        request_post = requests.post(url=product_url, data=json.dumps(new_product), headers= headers)
        response_data = request_post.json()

        print ("New product is: ") 

        print(response_data) 