import requests
import time 
import datetime
import threading
import operator
import os
import math
import json
import ast
from pathlib import Path
import pandas as pd
import shutil
infuraIpfsSecret = '75bfdb23290093c4c4132437ddd0053b'
infuraIpfsId = '1zG2q22hA21WrgpRrW2lBXe6FXC'

test = True;

if test == False: 
    waitForUpdate = True
    skipScrape = False
    tokenCount = 10000
    threadCount = 50
    openSeaLimit = 500
    countBlanks = False

else: 
    waitForUpdate = False
    skipScrape = False
    tokenCount = 10000
    threadCount = 50
    openSeaLimit = 500
    countBlanks = False

keywords = ["Rare", "rare", "Legendary", "legendary", "Special", "special"]
ipfs = False
url_suffix = ''

collection = 'partydegens'
url_stub = 'https://api.partydegenerates.com/degenerates/'
token_contract_address = '0x4be3223f8708ca6b30d1e8b8926cf281ec83e770'

#collection = 'headdao'
#url_stub = 'https://whispering-fortress-75639.herokuapp.com/fetch/metadata/'
#token_contract_address = '0xf62c6a8e7bcdc96cda11bd765b40afa9ffc19ab9'

#collection = 'junglefreaks'
#url_stub = 'ipfs://QmZCsdZ616bmjqrGM44MggF4CjVaTmVMa7baLG55WgGHCR/0000'
#token_contract_address = '0x7e6bc952d4b4bd814853301bee48e99891424de0'

# Metasaurs
#url_stub = "https://api.metasaurs.com/metadata/"
#url_suffix = '.json'
#token_contract_address = '0xf7143ba42d40eaeb49b88dac0067e54af042e963'

# Galactic Apes
#url_stub = 'https://galacticapes.mypinata.cloud/ipfs/QmcX6g2xXiFP5j1iAfXREuP9EucRRpuMCAnoYaVYjtrJeK/'
#token_contract_address = '0x12d2d1bed91c24f878f37e66bd829ce7197e4d14'

# Mekaverse
#url_stub = "https://api.themekaverse.com/meka/"
#url_suffix = ''
#token_contract_address = '0x9a534628b4062e123ce7ee2222ec20b86e16ca8f'

# DystoPunks V2
#url_stub = 'ipfs://QmUBZpfqwzZxw9pQB6RykMpetW2X5xxVhSHm1TyYCZmGV2/'
#token_contract_address = '0xbea8123277142de42571f1fac045225a1d347977'

# GEVOLS
#url_stub = "https://api.gevols.com/token/"
#token_contract_address = '0x34b4df75a17f8b3a6eff6bba477d39d701f5e92c'

# Cool Cats
#url_stub = 'https://api.coolcatsnft.com/cat/'
#token_contract_address = '0x1a92f7381b9f03921564a437210bb9396471050c'

# BAYC (IPFS)
#collection = 'bayc'
#url_stub = 'ipfs://QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/'
#token_contract_address = '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d'

# Anonymice
#url_stub = MUST LOOP THROUGH ETHERSCAN, THEN CONVERT FROM BASE64
#token_contract_address = '0xbad6186E92002E312078b5a1dAfd5ddf63d3f731'

# Humanoids
#url_stub = 'https://raw.githubusercontent.com/TheHumanoids/metadata/main/'
#token_contract_address = '0x3a5051566b2241285be871f650c445a88a970edd'

# SVS
#url_stub = 'ipfs://bafybeic26wp7ck2bsjhjm5pcdigxqebnthqrmugsygxj5fov2r2qwhxyqu/'
#token_contract_address = '0x219b8ab790decc32444a6600971c7c3718252539'

# Lazy Lions (IPFS)
#url_stub = 'https://www.lazylionsnft.com/api/'
#token_contract_address = '0x8943c7bac1914c9a7aba750bf2b6b09fd21037e0'


if 'ipfs://' in url_stub:
    ipfs = True
    split = url_stub.split('://')
    url_stub = split[1]

#quit()

if skipScrape == False:
    if os.path.isfile("exports/" + collection + "/tokens.csv"):
        os.remove("exports/" + collection + "/tokens.csv")
    if os.path.isfile("exports/" + collection + "/counts.csv"):
        os.remove("exports/" + collection + "/counts.csv")
    try:
        shutil.rmtree("exports/" + collection + "/errors/")
    except OSError as e:
        print(e.strerror)
    try:
        shutil.rmtree("exports/" + collection + "/loot/")
    except OSError as e:
        print(e.strerror)

#quit()


if waitForUpdate:
    if (ipfs):
        params = (('arg', url_stub + '1'),)
        r = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params, auth=(infuraIpfsId,infuraIpfsSecret))
    else: 
        r = requests.get(url_stub + '1' + url_suffix, timeout=10)
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
        if (ipfs):
            params = (('arg', url_stub + '1'),)
            r = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params, auth=(infuraIpfsId,infuraIpfsSecret))
        else:
            r = requests.get(url_stub + '1' + url_suffix + '?v=' + str(cache), timeout=10)
        #print(r.text)
        if not 'Error' in r.text:
            newValue = r.text
      except Exception as e:
        print(e)

    print('--------------')
    print('MILESTONE: TokenURI Updated!')
    print(datetime.datetime.now())
    print(newValue)
    os.system("afplay alert.wav") 


if skipScrape == False:
    tokensPerThread = math.ceil(tokenCount / threadCount)
    errorIds = []

    def makeFolders():
        try:
            os.mkdir("exports")
        except:
            pass

        try:
            os.mkdir("exports/" + collection)
        except:
            pass

        try:
            os.mkdir("exports/" + collection + "/loot")
        except:
            pass

        try:
            os.mkdir("exports/" + collection + "/errors")
        except:
            pass

    def getThread(targetStack):
        for item in targetStack:
            url = item["url"]
            tokenId = item["id"]
            try:
                if (ipfs):
                    params = (('arg', url),)
                    r = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params, auth=(infuraIpfsId,infuraIpfsSecret))
                else: 
                    r = requests.get(url,timeout=10)
                with open("exports/" + collection + "/loot/" + tokenId +".json","w" ) as f:
                    f.write(r.text)
                    f.flush()

            except Exception as e:
                #print e
                with open("exports/" + collection + "/errors/" + tokenId + ".txt","w") as f:
                    f.write("Error for this => " + tokenId + "\n")
                    f.write(str(e))

    def generate_stack(url_stub):
        #Create 10 list/arrays of 1000 urls (contained in a list/array) to feed into threads
        stack = []
        count = 0
        for x in range(0, threadCount):
            targetStack = []
            for y in range(0, tokensPerThread):
                count+=1
                targetStack.append({"url": url_stub + str(count) + url_suffix, "id": str(count)})
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

folder = "exports/" + collection + "/loot/"
fstack = [folder + fname for fname in os.listdir(folder)]
dict = {}
total = 0
result = []
errors = []
columnOrder = ['rank', 'id', 'score', 'price', 'score/price', 'link', 'image']
for file in fstack:
    with open(file, "r") as f:
        try:
            data = json.load(f)
            tokenId = Path(f.name)
            image = ''
            if "image" in data:
                image = data["image"]
            else:
                image = data["image_url"]
            if 'ipfs://' in image:
                split = image.split('://')
                image = 'https://ipfs.infura.io:5001/api/v0/cat?arg=' + split[1]

            obj = {"id": tokenId.stem, "image": image, "price": '', "score/price": ''}
            if "attributes" in data:
                for trait in data["attributes"]:
                    #print(trait)
                    if not str(trait["trait_type"]) in columnOrder:
                        columnOrder.append(str(trait["trait_type"]))
                        columnOrder.append(str(trait["trait_type"]) + ' ##')
                    label = trait["trait_type"]
                    obj[label] = trait["value"]
                    if trait["value"] in keywords:
                        print('https://opensea.io/assets/0x9a534628b4062e123ce7ee2222ec20b86e16ca8f/' + tokenId.stem)
                #print(obj)
            result.append(obj)
        except Exception as e:
            #print('Skipped ' + f.name)
            #print(e)
            errors.append(f.name)


#print(errors)


# Add in 'Blank' values
if countBlanks == True:
    i = 0
    for row in result:
        for c in columnOrder:
            if not c in ['rank', 'id', 'score', 'score %', 'price', 'score/price', 'link', 'image']:
                if not '##' in c:
                    if not c in row:
                        result[i][c] = 'BLANK'
        i += 1


# Count the total traits
counts = {}
for row in result:
    for attr, value in row.items():
        if not attr in ['id', 'image', 'price', 'score/price']:
            if not attr in counts:
                counts[attr] = {}
            if not value in counts[attr]:
                counts[attr][value] = 1
            else:
                counts[attr][value] = counts[attr][value] + 1

countsFlat = []
for label, attributes in counts.items():
    for attr, value in attributes.items():
        countsFlat.append({"attribute": str(label) + ' - ' + str(attr), "count": value})

sortedCounts = sorted(countsFlat, key=lambda x: x["count"])
cf = pd.json_normalize(sortedCounts)
cf.to_csv("exports/" + collection + "/counts.csv", index=False, encoding='utf-8')
print('MILESTONE: Counts CSV Created')


# Get rarity score for each token
tokens = []
maxScore = 0
minScore = 100000000
for row in list(result):
    tokenObj = row
    score = 0 
    for attr, value in list(row.items()):    
         if not attr in ['id', 'image', 'price', 'score/price']:
            count = counts[attr][value]
            #tokenObj[attr] = str(value) + ' - ' + str(count)
            tokenObj[str(attr) + ' ##'] = count
            traitRarity = count / tokenCount
            score = score + (1 / traitRarity)
            
            if score > maxScore:
                maxScore = score
            if score < minScore:
                minScore = score

    tokenObj['score'] = score
    tokenObj['link'] = 'https://opensea.io/assets/' + token_contract_address + '/' + row['id']
    tokens.append(tokenObj)

i = 0
for token in list(tokens):
    score = token["score"]
    absoluteScore = score / (maxScore - minScore + 0.0000000001) * 100
    absoluteScore = float("{:.2f}".format(absoluteScore))
    tokens[i]["score"] = absoluteScore
    i += 1

# Sort them by rarity score, and get OpenSea prices for the top 200
sortedTokens = sorted(tokens, key=lambda x: x["score"], reverse=True)

# Add a 'rank' field + empty price fields
i = 0
for row in list(sortedTokens):
    sortedTokens[i]["rank"] = i + 1
    sortedTokens[i]["score/price"] = 0
    i += 1

openseaApi = 'https://api.opensea.io/api/v1/asset/' + token_contract_address + '/'
threadCount = 50
tokensPerThread = math.ceil(openSeaLimit / threadCount)
openseaErrors = []

def getThread(targetStack):
    for link in targetStack:
        url = link["url"]
        index = link["index"]
        buyUrl = link["buyUrl"]
        #print(url, 'url')
        # print 'this is url => ',url
        # id = str(url.split('asset/' + token_contract_address + '/').pop())
        try:
            r = requests.get(url, timeout=10)
            data = r.text
            data = json.loads(data)
            if "owner" in data:
                owner = data["owner"]["address"]
                for order in data["orders"]:
                    if order["maker"]["address"] == owner:
                        price = int(order["base_price"]) / 1000000000000000000
                        # print(price)
                        sortedTokens[index]["price"] = price
                        sortedTokens[index]["score/price"] = float("{:.1f}".format(sortedTokens[index]["score"] / price))
                        print('#' + str(index) + ' - ' + str(price) + ' ETH - ' + buyUrl)
                        break

        except Exception as e:
            print('OpenSea scrape error: ' + str(e))
            #openseaErrors.append(url)


def generate_stack():
    #Create 10 list/arrays of 1000 urls (contained in a list/array) to feed into threads
    stack = []
    count = 0
    for x in range(0, threadCount):
        targetStack = []
        for y in range(0, tokensPerThread):
            count+=1
            #targetStack.append(openseaApi + str(sortedTokens[count]["id"]))
            targetStack.append({"url": openseaApi + str(sortedTokens[count]["id"]), "index": count, "buyUrl": 'https://opensea.io/assets/' + str(token_contract_address) + '/' + str(sortedTokens[count]["id"]) })
        stack.append(targetStack)
    return stack

stack = generate_stack()
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
print('MILESTONE: OpenSea Prices Complete')

# Order by price, then by rarity
#sortedTokens = sorted(tokens, key=lambda x: x["price"], reverse=True)
#sortedTokens = sorted(sortedTokens, key=lambda x: (x["score/price"], x["score"]), reverse=True)
sortedTokens = sorted(sortedTokens, key = operator.itemgetter("score/price"), reverse=True)

# Export JSON to CSV
df = pd.json_normalize(sortedTokens)
df_reorder = df[columnOrder]
df_reorder.to_csv("exports/" + collection + "/tokens.csv", index=True, encoding='utf-8')
#print('MILESTONE: Tokens CSV Sorted')



print('DONE!!!!!')
