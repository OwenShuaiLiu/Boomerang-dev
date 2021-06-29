import shopify
import requests
import json
from datetime import datetime
from datetime import timedelta 

from airtable import Airtable

# read response from airtable
airtable_item = Airtable('appIk8SiAeeLxVI3C', 'Items', api_key='keyoeqwCB4RoJUAtB')
#print(data)

API_KEY = "833fd488c5447c36b3f18caaec0df410"
PASSWORD = "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"
SHOP_NAME = "boomerangdev"

shop_url = "https://%s:%s@%s.myshopify.com/admin" % (API_KEY, PASSWORD, SHOP_NAME)

shopify.ShopifyResource.set_site(shop_url)
shop = shopify.Shop.current()

dateTimeObj = datetime.now() - timedelta(days=60)
dateStr = dateTimeObj.strftime("%Y-%b-%d")

order_url = shop_url + "/api/2020-04/orders.json?" + "financial_status=paid"+ "&created_at_min=" + dateStr + "T00:00:00-04:00"


headers = {'content-type': 'application/json'}
order_get = requests.get(url=order_url, headers= headers)
order_data = order_get.json()

#print ("New orders are: ") 
#print(order_data) 

orders = order_data["orders"]

#print(orders)

for order in orders:
    print(order['line_items'][0])
    title = order['line_items'][0]['title']
    vendor = order['line_items'][0]['vendor']
    product_id = order['line_items'][0]['product_id']
    #print(product_id)
    quantity = order['line_items'][0]['quantity']

    record = {"Status": "sold"}
    airtable_item.update_by_field('SKU', product_id, record)

