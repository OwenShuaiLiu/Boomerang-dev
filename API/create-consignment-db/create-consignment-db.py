from flask import Flask
from flask import request 
from flask import Response
from flask import abort
import pymysql
import json
import requests


app = Flask(__name__)

#Connect with database
cursor = None

def get_db_connection():
  global cursor

  if not cursor:
    db = pymysql.connect(
        host = 'boomerangdbtest.cj1wllzm2a1h.us-west-1.rds.amazonaws.com', 
        user = 'boomerang', 
        passwd = 'boomerang', 
        db = 'boomerangDBTEST', 
        port = 3306)
    cursor = db.cursor()
  return cursor

#create a new consignment
@app.route('/create_consignment', methods=["POST"])
def create_consignment():

	if request.headers['Content-Type'] == 'application/json':
    		arguments = request.get_json()

	#transaction request data
	tran_request = arguments.get("Consignment request no.")
	tran_date = arguments.get("createdTime")

	#item data
	product_brand = arguments.get("brand")
	product_category = arguments.get("category")
	product_usage = arguments.get("usage")
	product_description = arguments.get("description")
	product_weight = float(arguments.get("weight"))
	item_no = arguments.get("item_no")

	#user data
	user_name = arguments.get("name")
	user_email_addr = arguments.get("email_addr")
	user_phone = arguments.get("phone")
	user_addr_1 = arguments.get("addr_1")
	user_addr_2 = arguments.get("addr_2")
	user_city = arguments.get("city")
	user_state = arguments.get("state")
	user_country = arguments.get("country")
	user_zip_code = arguments.get("zip_code")
	user_no = arguments.get("user_no")

	#transaction data
	compensation_type = arguments.get("compensation_type")
	product_repair = arguments.get("repair")

	#create a new consignment request
	cursor_tran_request = get_db_connection()
	cursor_tran_request.execute("INSERT INTO consignment_requests (consignment_request_no, date) VALUES (%s, %s)", ([tran_request], [tran_date]))
	cursor_tran_request.execute("commit")

	#create a new user
	cursor_user = get_db_connection()
	cursor_user.execute("INSERT INTO users (name, email_addr, phone, addr_1, addr_2, city, zip_code, state, consignment_request_no, user_no) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ([user_name], [user_email_addr], [user_phone], [user_addr_1], [user_addr_2], [user_city], [user_zip_code], [user_state], [tran_request], [user_no]))
	cursor_user.execute("commit")

	#create a new item
	cursor_product = get_db_connection()
	cursor_product.execute("INSERT INTO items (brand, usage_condition, category, description, status, consignment_request_no, item_no) VALUES (%s, %s, %s, %s, %s, %s, %s)", ([product_brand], [product_usage], [product_category], [product_description], ["initiated"], [tran_request], [item_no]))
	cursor_product.execute("commit")

	#create a new consignment transaction
	cursor_resale_trans = get_db_connection()
	cursor_resale_trans.execute("INSERT INTO consign_trans (item_no, user_no, compensation_type, repair_needed, consignment_request_no) VALUES (%s, %s, %s, %s, %s)", ([item_no], [user_no], [compensation_type], [product_repair], [tran_request]))
	cursor_resale_trans.execute("commit")

	return "success", 201

if __name__ == '__main__':
    
    app.run(host='0.0.0.0')