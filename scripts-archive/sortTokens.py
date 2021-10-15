# -*- coding: utf-8 -*-
import os
import json
import ast
from pathlib import Path
import pandas as pd
import requests

# Get all the individual tokenURI's and merge them into one JSON object

# Mekk's
#token_contract_address = '0x9a534628b4062e123ce7ee2222ec20b86e16ca8f'
# GEVOLS
token_contract_address = '0x34b4df75a17f8b3a6eff6bba477d39d701f5e92c'
tokenCount = 8887

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
            obj = {"id": tokenId.stem}
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

cf = pd.json_normalize(counts)
cf.to_csv('counts.csv', index=False, encoding='utf-8')
print('Counts CSV Created')


# Get rarity score for each token
tokens = []
for row in result:
    for attr, value in row.items():
        totalScore = 1 
        if attr != 'id':
            count = counts[attr][value]
            score = count / tokenCount   
            if score > 0:
                totalScore = totalScore * score
    tokenObj = row
    tokenObj['score'] = totalScore
    tokenObj['link'] = 'https://opensea.io/assets/' + token_contract_address + '/' + row['id']
    tokens.append(tokenObj)

#print('--------')
#print(tokens)


# Sort them by rarity score, and get OpenSea prices for the top 200
sortedTokens = sorted(tokens, key=lambda x: x["score"])

i = 0
limit = 5
openseaApi = 'https://api.opensea.io/api/v1/asset/' + token_contract_address + '/'

for row in sortedTokens:
    if i > limit:
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

print('Tokens CSV Created')

