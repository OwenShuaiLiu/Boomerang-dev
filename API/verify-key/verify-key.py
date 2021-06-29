from flask import Flask
from flask import request 
from flask import Response
from flask import abort
import json
import requests

known_good_keys = [
    "boomerang2020v1",
    "boomerang2020v2",
    "boomerang2020v3"
]

app = Flask(__name__)

@app.route('/verify_key', methods=["POST"])
def verify_key():

    if request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()

    key = arguments.get("api_key")
    if key in known_good_keys:
        return json.dumps({"result": "yes"})
    else: 
        return json.dumps({"result": "no"})

if __name__ == '__main__':
    app.run(host='0.0.0.0')