import requests
import json

newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}

url='http://54.201.190.33:5000/confirm_consignment'
key={"api_key": "boomerang2020v1"}
t = json.dumps(key)
x = requests.post(url, data = t, headers=newHeaders)

