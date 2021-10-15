import requests
import time 
import datetime
import threading
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
    useEtherscan = 0
    waitForUpdate = True
    skipScrape = False
    tokenCount = 8888
    threadCount = 50
    openSeaLimit = 500
    countBlanks = False

else: 
    useEtherscan = 0
    waitForUpdate = False
    skipScrape = True
    tokenCount = 8888
    threadCount = 50
    openSeaLimit = 10
    countBlanks = True


rankByMultiply = True
url_stub = "https://api.themekaverse.com/meka/"
url_suffix = ''
token_contract_address = '0x9a534628b4062e123ce7ee2222ec20b86e16ca8f'

# Metasaurs
#url_stub = "https://api.metasaurs.com/metadata/"
#url_suffix = '.json'
#token_contract_address = '0xf7143ba42d40eaeb49b88dac0067e54af042e963'

keywords = ["Rare", "rare", "Legendary", "legendary", "Special", "special"]
ipfs = False


# Galactic Apes
#url_stub = 'https://galacticapes.mypinata.cloud/ipfs/QmcX6g2xXiFP5j1iAfXREuP9EucRRpuMCAnoYaVYjtrJeK/'
#token_contract_address = '0x12d2d1bed91c24f878f37e66bd829ce7197e4d14'

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
    if os.path.isfile("tokens.csv"):
        os.remove("tokens.csv")
    if os.path.isfile("counts.csv"):
        os.remove("counts.csv")
    try:
        shutil.rmtree('errors/')
    except OSError as e:
        print(e.strerror)
    try:
        shutil.rmtree('loot/')
    except OSError as e:
        print(e.strerror)

#quit()


if waitForUpdate:
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
                targetStack.append(url_stub + str(county) + url_suffix)
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
errors = []
columnOrder = ['id', 'combined score', 'absolute score', 'score', 'absolute % score', 'score %', 'price', 'score/price', 'link', 'image']
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
    print('Count blanks')
    i = 0
    for row in result:
        for c in columnOrder:
            if not c in ['id', 'score', 'score %', 'price', 'score/price', 'link', 'image']:
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
cf.to_csv('counts.csv', index=False, encoding='utf-8')
print('MILESTONE: Counts CSV Created')


# Get rarity score for each token
tokens = []
maxScore = 0
minScore = 100000000
maxMultiplyScore = 0
minMultiplyScore = 100000000
for row in list(result):
    tokenObj = row
    multiplyScore = 1
    sumScore = 0 
    for attr, value in list(row.items()):    
         if not attr in ['id', 'image', 'price', 'score/price']:
            count = counts[attr][value]
            #tokenObj[attr] = str(value) + ' - ' + str(count)
            tokenObj[str(attr) + ' ##'] = count
            sumScore = sumScore + count
            score = count / tokenCount
            multiplyScore = multiplyScore * score
    if sumScore > maxScore:
        maxScore = sumScore
    if sumScore < minScore:
        minScore = sumScore

    if multiplyScore > maxMultiplyScore:
        maxMultiplyScore = multiplyScore
    if multiplyScore < minMultiplyScore:
        minMultiplyScore = multiplyScore
    tokenObj['score'] = sumScore
    tokenObj['score %'] = multiplyScore
    tokenObj['link'] = 'https://opensea.io/assets/' + token_contract_address + '/' + row['id']
    tokens.append(tokenObj)


print("Min: " + str(minMultiplyScore))
print("Max: " + str(maxMultiplyScore))

# Set absolute rarity score for each token (0-100)
adjustedMax = maxScore - minScore
adjustedMultiplyMax = maxMultiplyScore - minMultiplyScore

print("Adjusted Max: " + str(adjustedMultiplyMax))

i = 0
for token in list(tokens):
    multiplyScore = token["score %"]
    absoluteMultiply = multiplyScore/ adjustedMultiplyMax * 100
    absoluteMultiplyScore = 100 - absoluteMultiply
    absoluteMultiplyScore = float("{:.2f}".format(absoluteMultiplyScore))
    tokens[i]["absolute % score"] = absoluteMultiplyScore

    if i == 0:
        print('Multiply Score: ' + str(multiplyScore))
        print('Absolute Multiply Score: ' + str(absoluteMultiplyScore))

    score = token["score"]
    absoluteScore = score / adjustedMax * 100
    absoluteScore = 100 - absoluteScore
    absoluteScore = float("{:.2f}".format(absoluteScore))
    tokens[i]["absolute score"] = absoluteScore

    tokens[i]["combined score"] = absoluteScore + absoluteMultiplyScore
    i += 1


# Sort them by rarity score, and get OpenSea prices for the top 200
sortedTokens = sorted(tokens, key=lambda x: x["score"])

openseaApi = 'https://api.opensea.io/api/v1/asset/' + token_contract_address + '/'
threadCount = 50
tokensPerThread = math.ceil(openSeaLimit / threadCount)
openseaErrors = []

def getThread(targetStack):
    for link in targetStack:
        url = link["url"]
        count = link["index"]
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
                        sortedTokens[count]["price"] = price
                        sortedTokens[count]["score/price"] = float("{:.1f}".format(sortedTokens[count]["absolute score"] / price))
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
            targetStack.append({"url": openseaApi + str(sortedTokens[count]["id"]), "index": count})
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


# Export JSON to CSV
df = pd.json_normalize(sortedTokens)
df_reorder = df[columnOrder]
df_reorder.to_csv('tokens.csv', index=True, encoding='utf-8')
#print('MILESTONE: Tokens CSV Sorted')



print('DONE!!!!!')
