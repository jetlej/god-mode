import requests
import json
import time
import datetime
import os
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/14fa7483b0f04fda84abe10f54a721e1'))

# MEKK's
token_contract_address = '0x9a534628b4062e123ce7ee2222ec20b86e16ca8f'
testTokenID = 1
loop = True

web3ContractAddress = Web3.toChecksumAddress(token_contract_address)
etherScanApi = 'https://api.etherscan.io/api?module=contract&action=getabi&address=' + token_contract_address + '&apikey=A78HVGKSAG4PAZGGFFV7YRV4I2Y21NYWGF'
r = requests.get(etherScanApi, timeout=10)
ABI = json.loads(r.text)
ABI = ABI["result"]
#print(ABI)

contract = w3.eth.contract(web3ContractAddress, abi=ABI)
tokenURI = contract.functions.tokenURI(testTokenID).call()
print(tokenURI)

if loop == True:
  initValue = tokenURI
  newValue = initValue
  while newValue == initValue:
      print("Not yet")
      time.sleep(30)
      try:
        tokenURI = contract.functions.tokenURI(testTokenID).call()
        #print(tokenURI)
        if not 'Error' in tokenURI:
            newValue = tokenURI
      except Exception as e:
        print(e)

  print('--------------')
  print('ALERT: TokenURI function Updated!')
  print(datetime.datetime.now())
  print(newValue)
  os.system("afplay ../alert.wav") 
