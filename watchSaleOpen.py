import requests
import json
import time
import datetime
import os
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/14fa7483b0f04fda84abe10f54a721e1'))

# Jungle Freaks
token_contract_address = '0x7e6bc952d4b4bd814853301bee48e99891424de0'
testTokenID = 1
loop = True

web3ContractAddress = Web3.toChecksumAddress(token_contract_address)
etherScanApi = 'https://api.etherscan.io/api?module=contract&action=getabi&address=' + token_contract_address + '&apikey=A78HVGKSAG4PAZGGFFV7YRV4I2Y21NYWGF'
r = requests.get(etherScanApi, timeout=10)
ABI = json.loads(r.text)
ABI = ABI["result"]
#print(ABI)

contract = w3.eth.contract(web3ContractAddress, abi=ABI)
tokenURI = contract.functions.saleOpen().call()
print(tokenURI)

if loop == True:
  initValue = tokenURI
  newValue = initValue
  while newValue == initValue:
      print("Not yet")
      time.sleep(3)
      try:
        tokenURI = contract.functions.saleOpen().call()
        newValue = tokenURI
      except Exception as e:
        print(e)

  print('--------------')
  print('ALERT: Sale Open!1!')
  print(datetime.datetime.now())
  print(newValue)
  os.system("afplay alert.wav") 
