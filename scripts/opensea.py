import requests
import json


token_contract_address = '0x34b4df75a17f8b3a6eff6bba477d39d701f5e92c'

ids = []
openseaApi = 'https://api.opensea.io/api/v1/asset/' + token_contract_address + '/'

for id in ids:
  r = requests.get(openseaApi + str(id), timeout=10)
  data = r.text
  data = json.loads(data)
  #print(data)
  owner = data["owner"]["address"]
  print('owner', owner)
  for order in data["orders"]:
    if order["maker"]["address"] == owner:
      price = int(order["base_price"]) / 1000000000000000000
      print(id, price)
