# Instructions

## Install 
1. Open Terminal and navigate to this folder
2. Run `pip3 install -r /path/to/requirements.txt`

## 1. Find the contract address & token URI for the NFT collection
1. Go to the collection on OpenSea, and click on one of the NFT's
2. Look at the URL, and copy the long string after '/assets/' (make sure to not include the following slash, or the number after it). This is the contract address.
3. Go to Etherscan.com and paste the contract address into the search bar
4. Click on the 'Contract' tab
5. Click 'Read Contract'
6. Scroll down to the tokenURI function, click it, enter '1' in the input field, and click submit
7. The result is the tokenURI, which can take many forms...
a) **URL** (eg. `https://api.themekaverse.com/meka/1`)
*Copy the link but REMOVE the 1 at the end, after the last slash*
b) **IPFS Link** (eg. `ipfs://QmUBZpfqwzZxw9pQB6RykMpetW2X5xxVhSHmZmGV/`)
*Copy the link but REMOVE the 1 at the end, after the last slash*
c) **IPFS Cloud Service Link** (eg. `https://gateway.pinata.cloud/ipfs/QmUBZpfqwzZxw9pQB6RykMpetW2X5xxVhSHm1TyYCZmGV2/1)`
*Copy the long string in the URL, and insert it into this format:* `ipfs://QmUBZpfqwzZxw9pQB6RykMpetW2X5xxVhSHm1TyYCZmGV2/`
c) **Base64 Code** (started with `base64`, then a bunch of random code)
*Code is not ready for this yet*
d) **JSON object**  (readable token data, surrounded by brackets)
*God Mode is not ready for this yet*
8. Move to the next step!!!

## 2. Run God Mode
1. Open `godMode.py` and switch out the `token_contract_address` and `url_stub` for your chosen NFT collection
2. Run `python3 godMode.py`
3. If it works, it will spit out `tokens.csv` in this folder
4. Go to the [Google Sheets template](https://docs.google.com/spreadsheets/d/1mjYXERwns5dLtBHYh2GT3BZ_MZFL_dXJ1Yk50AWOElc/edit?usp=sharing), and make a duplicate
5. Select the cell that says 'this', then go File > Import > 