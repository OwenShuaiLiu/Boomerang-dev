from flask import Flask
from flask import request 
from flask import Response
from flask import abort
import MySQLdb
import json
import easypost
import requests

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Boomerang!')
    }

known_good_keys = [
    "abc",
    "def",
    "boomerang"
]

def verify_key(key):
    return key in known_good_keys

easypost.api_key = 'EZTK3596379d680b46709cb5e8874248b080PDrwLRMZdNk1TfSH0BrnDg'
MAILGUN_DOMAIN_NAME = "sandbox5ca83b8ea32441feb50691cda4bde532.mailgun.org"
MAILGUN_API_KEY = "key-e284f40bf62b78c3fcd79fb5076b235f"


app = Flask(__name__)

#Connect with database
cursor = None

def get_db_connection():
  global cursor

  if not cursor:
    db = MySQLdb.connect(
        host = 'boomerangdbtest.cj1wllzm2a1h.us-west-1.rds.amazonaws.com', 
        user = 'boomerang', 
        passwd = 'boomerang', 
        db = 'boomerangDBTEST', 
        port = 3306)
    cursor = db.cursor()
  return cursor


boomerang_email = "owen.shuai.liu@berkeley.edu" # only for testing purpose
def send_notification(email, subject, content):
    return requests.post(f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages",
                         auth=("api", MAILGUN_API_KEY),
                         data={"from": f"Boomerang {boomerang_email}", "to": [email], "subject": subject,
                                "text": content})

@app.route('/', methods = ["GET"])
def hello_world():

	return "Hello Boomerang!", 200


#request a new resale
@app.route('/request_consignment', methods=["POST"])
def request_resale():

	if request.headers['Content-Type'] == 'application/json':
    		arguments = request.get_json()

	if not verify_key(arguments.get("api_key")):
    		return "Error: api key not authorized", 401

	#product data
	product_brand = arguments.get("brand")
	product_category = arguments.get("category")
	product_usage = arguments.get("usage")
	product_description = arguments.get("description")
	product_weight = float(arguments.get("weight"))

	#transaction data
	compensation_type = arguments.get("compensation_type")
	product_repair = arguments.get("repair")

	#user data
	user_email_addr = arguments.get("email_addr")
	user_phone = arguments.get("phone")
	user_addr_1 = arguments.get("addr_1")
	user_addr_2 = arguments.get("addr_2")
	user_city = arguments.get("city")
	user_state = arguments.get("state")
	user_country = arguments.get("country")
	user_zip_code = arguments.get("zip_code")


    #insert a new user
	cursor_user = get_db_connection()
	cursor_user.execute("INSERT INTO users (email_addr, phone, addr_1, addr_2, city, zip_code, state) VALUES (%s, %s, %s, %s, %s, %s, %s)", ([user_email_addr], [user_phone], [user_addr_1], [user_addr_2], [user_city], [user_zip_code], [user_state]))
	cursor_user.execute("commit")
	cursor_user.execute("select * from users where email_addr = %s and phone = %s", ([user_email_addr], [user_phone]))
	data = cursor_user.fetchall()
	cursor_user.execute("commit")
	for row in data:
    		user_id = row[0]
	
    #insert a new product
	cursor_product = get_db_connection()
	cursor_product.execute("INSERT INTO products (brand, usage_status, category, description, status) VALUES (%s, %s, %s, %s, %s)", ([product_brand], [product_usage], [product_category], [product_description], ["initiated"]))
	cursor_product.execute("commit")
	cursor_product.execute("select * from products where description = %s", [product_description])
	data = cursor_product.fetchall()
	cursor_product.execute("commit")
	for row in data:
    		product_id = row[0]


    #insert a new resale transaction
	cursor_resale_trans = get_db_connection()
	cursor_resale_trans.execute("INSERT INTO consign_trans (product_id, user_id, compensation_type, repair_needed) VALUES (%s, %s, %s, %s)", ([product_id], [user_id], [compensation_type], [product_repair]))
	cursor_resale_trans.execute("commit")

    #get price
	cursor_get_price = get_db_connection()

    #sql = "select * from products_pricing where brand=%s and category=%s and usage=%s and compensation_type=%s"
    #val = ([product_brand], [product_category], [product_usage], [compensation_type])
	sql = "select * from products_pricing where brand=%s and category=%s"
	val = ([product_brand], [product_category])
	cursor_get_price.execute(sql, val)
	data = cursor_get_price.fetchall()

	if compensation_type == "cash":
    		for row in data:
    				product_price = row[5]
	elif compensation_type == "credit":
    		for row in data:
    				product_price = row[6]
	cursor_get_price.execute("commit")

    #create shipment
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
    },
    #customs_info=customs_info
    )

	shipment.buy(rate = shipment.lowest_rate())
    #print(shipment.tracking_code)
    #print(shipment.postage_label.label_url)

    #email confirmation letter to user
	send_to = user_email_addr
	subject = "Thanks for choosing Boomerang!"
    #text = shipment.tracking_code
	text = "Please use the following shipping label:" + ' ' + shipment.postage_label.label_url + '\n' + "You will receive the foolowing amount once your product is sold: USD " + ' ' + str(product_price)


	r = send_notification(send_to, subject, text)
	r.raise_for_status()
	return "success", 201

#List product on brand website
@app.route('/shop', methods = ["POST"])
def get_products():
	if request.headers['Content-Type'] == 'application/json':
    		arguments = request.get_json()

	if not verify_key(arguments.get("api_key")):
    		return "Error: api key not authorized", 401

	sql = "SELECT * FROM products where status = 'listed'"
	cursor = get_db_connection()
	cursor.execute(sql)

	data = cursor.fetchall()
	print(data)

	response_msg = list()

	for row in data:
		response_msg_link = dict()
		response_msg_link["product_id"] = row[0]
		response_msg_link["brand"] = row[1]
		response_msg_link["product_title"] = row[2]
		response_msg_link["description"] = row[3]
		response_msg_link["status"] = row[4]
		response_msg_link["category"] = row[5]
		response_msg_link["usage_status"] = row[6]
		response_msg_link["size"] = row[7]
		response_msg_link["color"] = row[8]
		response_msg_link["picture"] = row[9]
		response_msg.append(response_msg_link)

	return json.dumps(response_msg), 200

#List a product
@app.route('/list', methods = ['PUT'])
def list_product():
    
	if request.headers['Content-Type'] == 'application/json':
    		arguments = request.get_json()

	if not verify_key(arguments.get("api_key")):
    		return "Error: api key not authorized", 401
	
	product_identity = arguments.get("product_id")
	title = arguments.get("product_title")
	product_picture = arguments.get("picture")
	product_size = arguments.get("size")
	product_color = arguments.get("color")
	product_description = arguments.get("description")
	product_status = "listed"

	cursor = get_db_connection()

	cursor.execute ("""
	UPDATE products
	SET status=%s, product_title=%s, picture=%s, size=%s, description=%s
	WHERE product_id=%s
	""", (product_status, title, product_picture, product_size, product_description, int(product_identity)))
	cursor.execute("commit")

	return "Success", 201

#verify a product
@app.route('/qualitycheck', methods=["PUT"])
def verify():

    data = request.get_json()
    product_identity = data.get("product_id")
    product_brand = data.get("brand")
    product_description = data.get("description")
    product_category = data.get("category")
    product_repair_needed = data.get("repair_needed")
    product_usage_status = data.get("usage_status")
    product_status = "verified"

    #update products table
    cursor_product = get_db_connection()
    sql = "UPDATE products SET brand=%s, description=%s, category=%s, usage_status=%s, status=%s WHERE product_id=%s"
    val = (product_brand, product_description, product_category, product_usage_status, product_status, int(product_identity))
    cursor_product.execute(sql, val)

    cursor_product.execute("commit")

    #update products pricing table
    #cursor_pricing = get_db_connection()
    #cursor_pricing.execute(f"UPDATE products_pricing SET brand = {product_brand}, category = {product_category}, usage_status = {product_usage_status}, repair_needed = {product_repair_needed} WHERE product_id = {int(product_identity)}")
    #cursor_pricing.execute("commit")

    #email confirmation letter to user

    cursor_verify_2 = get_db_connection()
    cursor_verify_2.execute("select * from users where user_id = (select product_id from consign_trans where product_id = %s)", [int(product_identity)])
    data = cursor_verify_2.fetchall()
    cursor_verify_2.execute("commit")
    for row in data:
        send_to = row[1]
        compensation_type = row[3]
        text = "We have received your product! We will pay you once it is sold."
        repair_needed= row[4]

        #send_to = user_email_addr
        subject = "Thanks for choosing Boomerang!"
        r = requests.post(
		    f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages",
		    auth=("api", MAILGUN_API_KEY),
		    data={"from": f"Boomerang <mailgun@{MAILGUN_DOMAIN_NAME}>",
			    "to": send_to,
			    "subject": subject,
			    "text": text})
        r.raise_for_status()

    return "success", 201


# pay the consigner in cash
@app.route('/checkout', methods=['PUT'])
def pay_cash():

	if not request.json or "product_id" not in request.json:
    		abort(400)

    # 1. Update the product status in the `products` table
	product_id = request.json["product_id"]
	cursor_products = get_db_connection()
	sql = "UPDATE products SET status = 'sold' WHERE product_id = %s"
	val = (product_id,)
	cursor_products.execute(sql, val)
	cursor_products.execute("commit")
    # 2. Notify the consigner and ask if they choose to be paid via Paypal or wire transfer
    # 2.1 Get the consigner's user_id from `consign_trans` table
	sql = "SELECT user_id FROM consign_trans WHERE product_id = %s"
	cursor_consign_trans = get_db_connection()
	cursor_consign_trans.execute(sql, val)
	row = cursor_consign_trans.fetchone()
	user_id = row[0]
    # 2.2 get consigner's email address from `users` table
	sql = "SELECT email_addr FROM users WHERE user_id = %s"
	val = (user_id, )
	cursor_users = get_db_connection()
	cursor_users.execute(sql, val)
	row = cursor_users.fetchone()
	email = row[0]

    # 2.3 If the consigner chose to receive payment in cash, send an email asking for preferred payment method
	sql = "SELECT compensation_type FROM consign_trans where product_id = %s"
	val = (product_id, )
	cursor_consign_trans.execute(sql, val)
	row = cursor_consign_trans.fetchone()
	compensation_type = row[0]
	if compensation_type == 'cash':
		send_notification(email, "Your item has been sold on Boomerang",
							"Hi,\n\nAre you willing to accept payment via Paypal? If yes, please send us your PayPal account. "
							"If not, we also do wire transfer subjected to fees\n\nBest,\nBoomerang")

    # 3. ship the item to the shopper and send the shipping label to Boomerang
	name = request.json["name"]
	addr_1 = request.json["addr_1"]
	addr_2 = request.json["addr_2"]
	city = request.json["city"]
	zip_code = request.json["zip_code"]
	state = request.json["state"]

    # 3.1 create and verify addresses
	from_address = easypost.Address.create(
		verify=["delivery"],
		name = "Dr. Steve Brule",
		street1 = "179 N Harbor Dr",
		street2 = "",
		city = "Redondo Beach",
		state = "CA",
		zip = "90277",
		country = "US",
		phone = "310-808-5243"
	)
	to_address = easypost.Address.create(
		verify=["delivery"],
		name = name,
		street1 = addr_1,
		street2 = addr_2,
		city = city,
		state = state,
		zip = zip_code,
		country = "US",
	)
    # 3.2 create parcel
	sql = "SELECT weight FROM products WHERE product_id = %s"
	cursor_products.execute(sql, val)
	weight = cursor_products.fetchone()[0]
	parcel = easypost.Parcel.create(
		predefined_package="Parcel",
		weight=weight
	)

    # 3.3 create shipment
	shipment = easypost.Shipment.create(
		to_address=to_address,
		from_address=from_address,
		parcel=parcel,
		# customs_info = customs_info,
		options={'certified_mail': True}  # Certified Mail provides the sender with a mailing receipt and,
		# upon request, electronic verification that an article was delivered
		# or that a delivery attempt was made.
	)

    # 3.4 buy postage label with one of the rate objects
	shipment.buy(rate=shipment.lowest_rate())
	print(shipment.tracking_code)
	print(shipment.postage_label.label_url)

    # Insure the shipment for the value
	shipment.insure(amount=100)
	print(shipment.insurance)
	#cursor_products.close()
	#cursor_users.close()
	#cursor_consign_trans.close()

	# 3.5 email the shipping label to Boomerang
	send_notification(boomerang_email, f"Shipping Label of item {product_id } to the shopper with email: {email}",
						f"The shipping label can be found here: {shipment.postage_label.label_url}")

	return "success", 201

if __name__ == '__main__':
    app.run()


# docker build -t api_image .
# docker run --name api_server -p 5000:5000 -e FLASK_APP=api.py -dit api_image
# logs -f api_server