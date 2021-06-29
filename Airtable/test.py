from airtable import Airtable
import re
import json
import requests

# read response from airtable
airtable = Airtable('appIk8SiAeeLxVI3C', 'Consignment requests', api_key='keyoeqwCB4RoJUAtB')

data = airtable.get_all()
print(data)