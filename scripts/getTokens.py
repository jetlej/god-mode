import requests
import threading
import os
import time
import math

url_stub = "https://api.gevols.com/token/"
tokenCount = 8887

threadCount = 50
tokensPerThread = math.ceil(tokenCount / threadCount)
print('tokensPerThread', tokensPerThread)
#url_stub = "https://api.themekaverse.com/meka/"

def makeFolds():
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
            if x * y <= tokenCount:
                county+=1
                targetStack.append(url_stub + str(county))
        stack.append(targetStack)
    return stack

makeFolds()
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
print('completed :)')