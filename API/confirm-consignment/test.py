from airtable import Airtable
from flask import Flask
from flask import request 
from flask import Response
from flask import abort
import json
import easypost
import requests
import uuid


URL_VERITY_KEY = 'http://34.217.194.57:5000/verify_key'
URL_SEND_NOTIFICATION = 'http://34.219.206.232:5000/send_notification'
URL_CREATE_SHIPMENT = 'http://34.217.50.139:5000/create_shipment'
URL_CREATE_CONSIGNMENT = 'http://34.211.153.71:5000/create_consignment'

#generate ids
def generate_item_no():  
    item_no ='item' + str(uuid.uuid4())
    return item_no

def generate_user_no():  
    user_no = 'user' + str(uuid.uuid4())
    return user_no

def generate_trans_no():  
    trans_no = 'trans' + str(uuid.uuid4())
    return trans_no


#read all requests and return a list of items per request
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
                item['name'] = fields['Name']
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


# verify api key
def verify_api_key(key):
    url = URL_VERITY_KEY

    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    data = {}
    data["api_key"] = key
    t = json.dumps(data)
    x = requests.post(url, data = t, headers=newHeaders)
    t= json.loads(x.text)
    t= str(t['result'])
    print(t)

    return t

# send notification
def send_notification(send_to, subject, content):
    url = URL_SEND_NOTIFICATION

    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    data = {}
    data["email"] = send_to
    data["subject"] = subject
    data["content"] = content
    t = json.dumps(data)
    x = requests.post(url, data = t, headers=newHeaders)

    return x

# create shipment
def create_shipment(item):
    url = URL_CREATE_SHIPMENT

    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    t = json.dumps(item)
    x = requests.post(url, data = t, headers=newHeaders)

    return x


# create a consignment transaction (item, user, transaction) in database
def create_consignment_db(new_request):
    url = URL_CREATE_CONSIGNMENT

    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    x = requests.post(url, data = new_request, headers=newHeaders)

    return x


# read response from airtable
airtable = Airtable('appIk8SiAeeLxVI3C', 'Consignment requests', api_key='keyoeqwCB4RoJUAtB')
airtable_item = Airtable('appIk8SiAeeLxVI3C', 'Items', api_key='keyoeqwCB4RoJUAtB')
airtable_customer = Airtable('appIk8SiAeeLxVI3C', 'Customers', api_key='keyoeqwCB4RoJUAtB')
airtable_consign_transction = Airtable('appIk8SiAeeLxVI3C', 'Consignment transactions', api_key='keyoeqwCB4RoJUAtB')

data = airtable.get_all()
print(data)

# confirm all requests
for reque in data:
    #processed requested ones, ignore confimed ones
    if reque and reque['fields']['Status'] == "Requested":
        #get a list of items in a request
        item_list = get_item_list(reque)
        #one user number for multiple transactions
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
            record_customer = {'Customer no.': item['user_no'], 'Name': item['name'], 'Email address':  item['email_addr'], 'Shipping address': item['addr_1'], 'City': item['city'], 'State': item['state'], 'Zip code': item['zip_code'], 'Consignment request no.': item['Consignment request no'], 'Status': 'Created'}
            airtable_customer.insert(record_customer)

            #create a new Consignment transaction in Airtable
            record_transaction = {'Consignment transaction no.': item['trans_no'], 'Customer no.': item['user_no'], 'Item no.': item['item_no'], 'Payout type': item['compensation_type'], 'Consignment request no.': item['Consignment request no'], 'Status': 'Created'}
            airtable_consign_transction.insert(record_transaction)

            #create a new item, a new user, and a new transaction in database
            t = json.dumps(item)
            create_consignment_db(t)
        
        # update status of the request in airtable
        record = airtable.match('Consignment request no.', item_list[0]['Consignment request no'])
        fields = {'Status': 'Confirmed'}
        airtable.update(record['id'], fields)

        #create a shipping label
        label_url = create_shipment(item_list[0])

        #send an email confirmation letter to user, one email per request (multiple items)
        send_to = item_list[0]['email_addr']
        subject = "Thanks for choosing Boomerang!"
        #text = shipment.tracking_code
        content = "Your consignment requesthas been confirmed. Please use the following shipping label:" + ' ' + label_url.text + '\n' + "You will receive payment once your product is sold."
        r = send_notification(send_to, subject, content)
        r.raise_for_status()