import requests
import time

# Get the tokenURI from https://checkmynft.com/
url_stub = "https://api.themekaverse.com/meka/"
r = requests.get(url_stub + '1', timeout=10)
initValue = r.text
print(initValue)
newValue = initValue

while newValue == initValue:
    print("Not yet")
    time.sleep(10)
    try:
      r = requests.get(url_stub + '1', timeout=10)
      newValue = r.text
    except Exception as e:
      print(e)

print('--------------')
print('DONE!')
print(newValue)