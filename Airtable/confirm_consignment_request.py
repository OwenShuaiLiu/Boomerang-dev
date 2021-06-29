from airtable import Airtable
import re
import json
import requests

import random 
import string 

import easypost
import requests

easypost.api_key = 'EZTK3596379d680b46709cb5e8874248b080PDrwLRMZdNk1TfSH0BrnDg'
MAILGUN_DOMAIN_NAME = "sandbox5ca83b8ea32441feb50691cda4bde532.mailgun.org"
MAILGUN_API_KEY = "key-e284f40bf62b78c3fcd79fb5076b235f"

boomerang_email = "owen.shuai.liu@berkeley.edu" # only for testing purpose
def send_notification(email, subject, content):
    return requests.post(f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages",
                         auth=("api", MAILGUN_API_KEY),
                         data={"from": f"Boomerang {boomerang_email}", "to": [email], "subject": subject,
                                "text": content})

def generate_shipping_label(user_email_addr, user_addr_1,user_addr_2, user_city, user_state, user_zip_code, user_phone, product_weight):
    shipment = easypost.Shipment.create(
        to_address={
            "name": 'Boomerang',
            "street1": '2530A Piedmont Avenue',
            "city": 'Berkeley',
            "state": 'CA',
            "zip": '94704',
            "country": 'US',
            "phone": '4153334444',
            "email": 'paullaverne@berkeley.edu'
        },
        from_address={
            "name": user_email_addr,
            "street1": user_addr_1,
            "street2": user_addr_2,
            "city": user_city,
            "state": user_state,
            "zip": user_zip_code,
            "country": 'US',
            "phone": user_phone,
            "email": user_email_addr
        },
        parcel={
            "length": 20.2,
            "width": 10.9,
            "height": 5,
            "weight": product_weight * 16
        }
    )
    shipment.buy(rate = shipment.lowest_rate())
    return shipment

def generate_item_no():  
	# Generate a random string 
	# with 32 characters. 
	item_no ='item' + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
	# print the random 
	# string of length 32 
	return item_no

def generate_user_no():  
	# Generate a random string 
	# with 8 characters. 
	user_no = 'user' + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
	# print the random 
	# string of length 8
	return user_no

def generate_trans_no():  
	# Generate a random string 
	# with 16 characters. 
	trans_no = 'trans' + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
	# print the random 
	# string of length 16
	return trans_no


# read response from airtable
airtable = Airtable('appIk8SiAeeLxVI3C', 'Consignment requests', api_key='keyoeqwCB4RoJUAtB')
airtable_item = Airtable('appIk8SiAeeLxVI3C', 'Items', api_key='keyoeqwCB4RoJUAtB')
airtable_customer = Airtable('appIk8SiAeeLxVI3C', 'Customers', api_key='keyoeqwCB4RoJUAtB')
airtable_consign_transction = Airtable('appIk8SiAeeLxVI3C', 'Consignment transactions', api_key='keyoeqwCB4RoJUAtB')

data = airtable.get_all()
print(data)

def get_item_list(request):
    item_list=[]
    fields = request['fields']
    if fields:
        for i in range(1,11):
            item={}
            for key in fields:
                if str(i) in key and "category" in key:
                    item['category'] = fields[key][0]
                elif str(i) in key and "description" in key:
                    item['description'] = fields[key]
                elif str(i) in key and "payout" in key:
                    item['compensation_type'] = fields[key][0]
            if item:
                item['Consignment request no'] = fields['Consignment request no.']
                item['createdTime'] = request['createdTime']
                item['brand'] = fields['Brand']
                item['phone'] = ''
                item['email_addr'] = fields['Email address']
                item['addr_1'] = fields['Address line 1']
                item['addr_2'] = ''
                item['city'] = fields['City']
                item['weight'] = 1
                item['state'] = fields['State']
                item['country'] = "US"
                item['zip_code'] = fields['Zip code']
                item['repair'] = 0
                item_list.append(item)
    return item_list


# confirm a request, may contain one or multiple items
def confirm_request(new_request):
    url = 'http://localhost:5000/request_consignment'

    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    x = requests.post(url, data = new_request, headers=newHeaders)

    print(x.text)

# confirm all requests
for request in data:
    if request and request['fields']['Status'] == "Requested":
        item_list = get_item_list(request)
        user_no = generate_user_no()
        for item in item_list:
            item['api_key']= "boomerang"
            item['user_no'] = user_no 
            item['item_no'] = generate_item_no()
            item['trans_no'] = generate_trans_no()

            #create a new item in Airtable
            record_item = {'Item no.': item['item_no'], 'Brand': item['brand'], 'Category': item['category'], 'Description': item['description'], 'Consignment request no.': item['Consignment request no'], 'Status': 'Created'}
            airtable_item.insert(record_item)

            #create a new customer in Airtable
            record_customer = {'Customer no.': item['user_no'], 'Email address':  item['email_addr'], 'Shipping address': item['addr_1'], 'City': item['city'], 'State': item['state'], 'Zip code': item['zip_code'], 'Consignment request no.': item['Consignment request no'], 'Status': 'Created'}
            airtable_customer.insert(record_customer)

            #create a new Consignment transaction in Airtable
            record_transaction = {'Consignment transaction no.': item['trans_no'], 'Customer no.': item['user_no'], 'Item no.': item['item_no'], 'Payout type': item['compensation_type'], 'Consignment request no.': item['Consignment request no'], 'Status': 'Created'}
            airtable_consign_transction.insert(record_transaction)

            #create a new item, a new user, and a new transaction in database
            t = json.dumps(item)
            confirm_request(t)
        
        record = airtable.match('Consignment request no.', item_list[0]['Consignment request no'])
        fields = {'Status': 'Confirmed'}
        airtable.update(record['id'], fields)
        shipment = generate_shipping_label(item_list[0]['email_addr'], item_list[0]['addr_1'], item_list[0]['addr_2'], item_list[0]['city'], item_list[0]['state'], item_list[0]['zip_code'], item_list[0]['phone'], item_list[0]['weight'])
        label_url = shipment.postage_label.label_url

        #email confirmation letter to user
        send_to = item_list[0]['email_addr']
        subject = "Thanks for choosing Boomerang!"
        #text = shipment.tracking_code
        text = "Your consignment requesthas been confirmed. Please use the following shipping label:" + ' ' + label_url + '\n' + "You will receive payment once your product is sold."

        r = send_notification(send_to, subject, text)
        r.raise_for_status()
