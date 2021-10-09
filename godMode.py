import requests
import time
import threading
import os
import math
import json
import ast
from pathlib import Path
import pandas as pd

if os.path.isfile("tokens.csv"):
    os.remove("tokens.csv")
if os.path.isfile("errors/"):
    os.remove("errors/")
if os.path.isfile("loot/"):
    os.remove("loot/")

infuraIpfsSecret = '75bfdb23290093c4c4132437ddd0053b'
infuraIpfsId = '1zG2q22hA21WrgpRrW2lBXe6FXC'

# Get the tokenURI from https://checkmynft.com/
ipfs = False
base64 = 0
useEtherscan = 0
waitForUpdate = False
skipScrape = True
tokenCount = 9999
openSeaLimit = 0

# Mekk's
#url_stub = "https://api.themekaverse.com/meka/"
#token_contract_address = '0x9a534628b4062e123ce7ee2222ec20b86e16ca8f'

# GEVOLS
#url_stub = "https://api.gevols.com/token/"
#token_contract_address = '0x34b4df75a17f8b3a6eff6bba477d39d701f5e92c'

# Cool Cats
url_stub = 'https://api.coolcatsnft.com/cat/'
token_contract_address = '0x1a92f7381b9f03921564a437210bb9396471050c'

# BAYC (IPFS)
#url_stub = 'ipfs://QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/'
#token_contract_address = '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d'

# Lazy Lions (IPFS)
#url_stub = 'https://www.lazylionsnft.com/api/'
#token_contract_address = '0x8943c7bac1914c9a7aba750bf2b6b09fd21037e0'


if 'ipfs://' in url_stub:
    ipfs = True
    split = url_stub.split('://')
    url_stub = split[1]

#quit()




if waitForUpdate:
  r = requests.get(url_stub + '1?v=1', timeout=10)
  initValue = r.text
  print(initValue)
  newValue = initValue

  cache = 1
  #while cache < 3:
  while newValue == initValue:
      cache = cache + 1
      print("Not yet")
      time.sleep(10)
      try:
        r = requests.get(url_stub + '1?v=' + str(cache), timeout=10)
        newValue = r.text
      except Exception as e:
        print(e)

  print('--------------')
  print('MILESTONE: TokenURI Updated!')
  print(newValue)
  os.system("afplay alert.wav") 


if not skipScrape:

    threadCount = 50
    tokensPerThread = math.ceil(tokenCount / threadCount)

    def makeFolders():
        try:
            os.mkdir("loot")
        except:
            pass

        try:
            os.mkdir("errors")
        except:
            pass

    def getThread(targetStack):
        for url in targetStack:
            # print 'this is url => ',url
            fname = str(url.split("/").pop())
            try:
                if (ipfs):
                    params = (('arg', url),)
                    r = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params, auth=(infuraIpfsId,infuraIpfsSecret))
                else: 
                    r = requests.get(url,timeout=10)
                with open("loot/" + fname +".json","w" ) as f:
                    f.write(r.text)
                    f.flush()

            except Exception as e:
                #print e
                with open("errors/" + fname + ".txt","w") as f:
                    f.write("Error for this => " + fname + "\n")
                    f.write(str(e))

    def generate_stack(url_stub):
        #Create 10 list/arrays of 1000 urls (contained in a list/array) to feed into threads
        stack = []
        county = 0
        for x in range(0, threadCount):
            targetStack = []
            for y in range(0, tokensPerThread):
                county+=1
                targetStack.append(url_stub + str(county))
            stack.append(targetStack)
        return stack

    makeFolders()
    stack = generate_stack(url_stub)
    threadStack = []
    for targets in stack:
        t = threading.Thread(target=getThread,args=([targets]))
        threadStack.append(t)
        t.start()


    tstamp = time.time()
    while True:
        t_temp = []
        for t in threadStack:
            check = t.is_alive()
            if check:
                t_temp.append(t)
        threadStack = t_temp
        if not threadStack:
            break
        time.sleep(10)
        print('elapsed time => ' + str(time.time() - tstamp))
    print('elapsed time => ' + str(time.time() - tstamp))
    print('MILESTONE: tokenURIs Download Complete')






# Get all the individual tokenURI's and merge them into one JSON object

folder = "loot/"
fstack = [folder + fname for fname in os.listdir(folder)]
dict = {}
total = 0
result = []
for file in fstack:
    with open(file, "r") as f:
        try:
            data = json.load(f)
            tokenId = Path(f.name)
            
            image = data["image"]
            if 'ipfs://' in image:
                split = image.split('://')
                image = 'https://ipfs.infura.io:5001/api/v0/cat?arg=' + split[1]

            obj = {"id": tokenId.stem, "image": image}
            for trait in data["attributes"]:
                #print(trait)
                label = trait["trait_type"]
                obj[label] = trait["value"]
            #print(obj)
            result.append(obj)
        except Exception as e:
            print(e)
            print('skipped one')


# Count the total traits
counts = {}
for row in result:
    for attr, value in row.items():
        if attr != 'id':
            if not attr in counts:
                counts[attr] = {}
            if not value in counts[attr]:
                counts[attr][value] = 1
            else:
                counts[attr][value] = counts[attr][value] + 1

#print('--------')
#print(counts)

#cf = pd.json_normalize(counts)
#cf.to_csv('counts.csv', index=False, encoding='utf-8')
#print('MILESTONE: Counts CSV Created')


# Get rarity score for each token
tokens = []
for row in list(result):
    tokenObj = row
    multiplyScore = 1
    sumScore = 0 
    for attr, value in list(row.items()):    
        if attr != 'id':
            count = counts[attr][value]
            #tokenObj[attr] = str(value) + ' - ' + str(count)
            tokenObj[str(attr) + ' #'] = count
            sumScore = sumScore + count
            score = count / tokenCount
            multiplyScore = multiplyScore * score
    tokenObj['Score - %'] = multiplyScore
    tokenObj['Score - Sum'] = sumScore
    tokenObj['link'] = 'https://opensea.io/assets/' + token_contract_address + '/' + row['id']
    tokens.append(tokenObj)

#print('--------')
#print(tokens)


# Sort them by rarity score, and get OpenSea prices for the top 200
sortedTokens = sorted(tokens, key=lambda x: x["Score - Sum"])

i = 0
openseaApi = 'https://api.opensea.io/api/v1/asset/' + token_contract_address + '/'

for row in sortedTokens:
    if i > openSeaLimit:
      break
    # get the price

    price = 0
    try:
        r = requests.get(openseaApi + str(row["id"]), timeout=10)
        data = r.text
        data = json.loads(data)
        #print(data)
        owner = data["owner"]["address"]
        print('owner', owner)
        for order in data["orders"]:
            if order["maker"]["address"] == owner:
                price = int(order["base_price"]) / 1000000000000000000
                print(price)
                sortedTokens[i]["price"] = price
                break
    except Exception as e:
        print('Error with OpenSea API')
        print(e)
    if price == 0:
        print('Not for sale')
    i = i + 1

# Print as JSON, can remove
#with open("tokens.json", "w") as outfile:
#     json.dump(result, outfile)

# Export JSON to CSV
df = pd.json_normalize(sortedTokens)
df.to_csv('tokens.csv', index=False, encoding='utf-8')

print('MILESTONE: Tokens CSV Created')

