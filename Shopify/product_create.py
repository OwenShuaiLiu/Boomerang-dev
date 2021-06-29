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

# Create a new product
new_product ={ 
    "product": { 
        "title": "Cal Bears Classic Primary Tri-Blend T-Shirt - Navy Blue", 
        "body_html": "<strong>Cal Bears T-Shirt!</strong>", 
        "vendor": "Cal", 
        "product_type": "T-Shirt", 
        "tags": ["Vintage","T-Shirt"],
        "variants": [
            {
                "inventory_quantity": 100,
                "option1": "Pink",
                "price": 29.99
            }
        ],
        "images": [{"src": "https://s3.us-west-2.amazonaws.com/brand-product-image/thumb.aspx.jpeg"}, {"src": "https://s3.us-west-2.amazonaws.com/brand-product-image/thumb.aspx-2.jpeg"}, {"src": "https://s3.us-west-2.amazonaws.com/brand-product-image/thumb.aspx-3.jpeg"}, {"src": "https://s3.us-west-2.amazonaws.com/brand-product-image/thumb.aspx-4.jpeg"}, {"src": "https://s3.us-west-2.amazonaws.com/brand-product-image/thumb.aspx-5.jpeg"}]
        }
    }
headers = {'content-type': 'application/json'}
request_post = requests.post(url=product_url, data=json.dumps(new_product), headers= headers)
response_data = request_post.json()

print ("New product id is: ") 

print(response_data["product"]["id"]) 