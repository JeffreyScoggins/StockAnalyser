#!/usr/bin/env python3
import sys
import json
import urllib.request as ur
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


ticker = input ('Enter stock ticker\n')
url = "https://cdn.cboe.com/api/global/delayed_quotes/options/"+ticker.upper()+".json" #pulls options JSON data from CBOE for desired stock ticker

data = ur.urlopen(url).read() #Pulls JSON data form URL
datajson = json.loads(data.decode('utf-8')) #Converts to python dictionary
stockData = datajson["data"] #SubDirectory
optionsData = stockData["options"] #Subdirectory

counteven = 0
countodd = 1
deltaSumCurrent = 1.0
deltaSumPrevious = 1.0
deltaNeutral = 0.0
deltaNeutralStrike = ""

for x in range(int(len(optionsData)/2)):
    greekData = optionsData[counteven] #Subdirectory
    greekDataCall = optionsData[counteven]
    greekDataCallDelta = greekDataCall['delta']
    greekDataPut = optionsData[countodd]
    greekDataPutDelta = greekDataPut['delta']

    deltaSumCurrent = float(greekDataPutDelta) + float(greekDataCallDelta)
    if deltaSumCurrent < 0:
        deltaSumCurrent * -1.0
    print ('Delta Sum Current')
    print (deltaSumCurrent)
    print ('Delta Sum Previous')
    print (deltaSumPrevious)
    if deltaSumCurrent < deltaSumPrevious:
        deltaNeutral = float(greekData['delta'])
        deltaSumPrevious = float(greekData['delta'])
        deltaNeutralStrike = greekData['option']
    deltaSumPrevious = deltaSumCurrent
    counteven += 2
    countodd += 2
print("Delta Neutral: ")
print(deltaNeutralStrike)
print(deltaNeutral)

count = 0
gammaPrevious = 0.0
gammaMax = 0.0
gammaMaxStrike = ""
for x in optionsData:
    greekData = optionsData[count] #Subdirectory
    if float(greekData['gamma']) > gammaPrevious:
        gammaMax = float(greekData['gamma'])
        gammaPrevious = float(greekData['gamma'])
        gammaMaxStrike = greekData['option']
    count += 1
print("Gamma Max: ")
print (gammaMaxStrike)
print(gammaMax)

    


        
