from flask import Flask
from flask import request 
from flask import Response
from flask import abort
from flask import jsonify
#import jsonpickle

import json
import requests

import easypost

easypost.api_key = 'EZAK35b0cd3c664944bcac801897af82af4c2TadDMm8yKVzpONQOa9WEA'


app = Flask(__name__)

#create a shippment
@app.route('/create_shipment', methods=["POST"])
def create_shipment():
    if request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()

    user_email_addr = arguments.get("email_addr")
    user_addr_1 = arguments.get("addr_1")
    user_addr_2 = arguments.get("addr_2")
    user_city = arguments.get("city")
    user_state = arguments.get("state")
    user_zip_code = arguments.get("zip_code")
    user_phone = arguments.get("phone")
    product_weight = float(arguments.get("weight"))

    to_address = easypost.Address.create(
        verify=["delivery"],
        street1="2110 HASTE ST APT 425",
        street2="",
        city="Berkeley",
        state="CA",
        zip="94704-2084",
        country="US",
        company="Boomerang Recommerce",
        phone= '6692819516',
        email= 'support@boomerang.fashion'
    )  

    from_address = easypost.Address.create(
        verify=["delivery"],
        street1=user_addr_1,
        street2=user_addr_2,
        city=user_city,
        state=user_state,
        zip=user_zip_code,
        country="US",
        phone= user_phone,
        email= user_email_addr
    )  
    shipment = easypost.Shipment.create(
        to_address =  to_address,
        from_address = from_address,
        parcel={
            "length": 20.2,
            "width": 10.9,
            "height": 5,
            "weight": product_weight * 16
        }
    )
    shipment.buy(rate = shipment.lowest_rate())

    
    #data = jsonpickle.encode(shipment)
    #return data

    label_tracker = {}
    label_tracker["label"]=shipment["postage_label"]["label_url"]
    label_tracker["tracker"]=shipment["tracker"]["public_url"]
    label_tracker["tracking_code"]=shipment["tracker"]["tracking_code"]
    data = json.dumps(label_tracker)
    
    return data


if __name__ == '__main__':

    app.run(host='0.0.0.0')

