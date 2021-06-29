from flask import Flask
from flask import request 
from flask import Response
from flask import abort
import pymysql
import json
import easypost
import requests

# verify authentication
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

# send email
boomerang_email = "owen.shuai.liu@berkeley.edu" # only for testing purpose
def send_notification(email, subject, content):
    return requests.post(f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages",
                         auth=("api", MAILGUN_API_KEY),
                         data={"from": f"Boomerang {boomerang_email}", "to": [email], "subject": subject,
                                "text": content})

def get_products():
    
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


def lambda_handler(event, context):
    # TODO implement

	return {
			'statusCode': 200,
			'body': get_products()
		}