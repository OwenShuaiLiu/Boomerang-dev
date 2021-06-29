import requests
import json

def verify_api_key(key):
    url = 'http://localhost:5000/verify_key'

    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    data = {}
    data["api_key"] = key
    t = json.dumps(data)
    x = requests.post(url, data = t, headers=newHeaders)
    t= json.loads(x.text)
    t= str(t['result'])
    print(t)

    return t

if verify_api_key("boomerang2020v1") == "yes":
    print("Correct")
else:
    print("Error: api key not authorized")
    