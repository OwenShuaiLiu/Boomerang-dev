from flask import Flask
from flask import request 
from flask import Response
from flask import abort
import json
import requests

app = Flask(__name__)

#MAILGUN_DOMAIN_NAME = "sandbox5ca83b8ea32441feb50691cda4bde532.mailgun.org"
#MAILGUN_API_KEY = "key-e284f40bf62b78c3fcd79fb5076b235f"

MAILGUN_DOMAIN_NAME = "support.boomerang.fashion"
MAILGUN_API_KEY = "1cf9a5ab0f7d0884fe152be08f1dd6d2-1b6eb03d-5afa41c4"

boomerang_email = "support@boomerang.fashion"

#request a new consignment
@app.route('/send_notification', methods=["POST"])
def send_notification():
    if request.headers['Content-Type'] == 'application/json':
            arguments = request.get_json()

    email = arguments.get("email")
    subject = arguments.get("subject")
    content = arguments.get("content")
    
    if email and subject and content:
        requests.post(f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages", auth=("api", MAILGUN_API_KEY), data={"from": f"Boomerang {boomerang_email}", "to": [email], "subject": subject, "text": content})
        return "success", 201

    # needs error handling (email address verification, delivery status check)


if __name__ == '__main__':
    app.run(host='0.0.0.0')