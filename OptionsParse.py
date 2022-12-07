#!/usr/bin/env python3
import sys
import json
import urllib.request as ur
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


ticker = input ('Enter stock ticker\n')
url = "https://cdn.cboe.com/api/global/delayed_quotes/options/"+ticker.upper()+".json"

data = ur.urlopen(url).read() #Pulls JSON data form URL
datajson = json.loads(data.decode('utf-8')) #Converts to python dictionary
stockData = datajson["data"] #SubDirectory
optionsData = stockData["options"] #Subdirectory

counteven = 0
countodd = 1
deltaSumCurrent = 1.0
deltaSumPrevious = 0.0
deltaNeutral = 0.0
deltaNeutralStrike = ""

for x in optionsData:
    greekData = optionsData[counteven] #Subdirectory
    greekDataCall = optionsData[counteven]
    greekDataPut= optionsData[countodd]
    callDelta = greekDataCall #Calls stored in even numbered buckets
    putDelta = greekDataPut #Puts stored in odd numbered buckets
    deltaSumCurrent = callDelta - putDelta
    if deltaSumCurrent < 0:
        deltaSumCurrent * -1
    if deltaSumCurrent < deltaSumPrevious:
        deltaNeutral = float(greekData['delta'])
        deltaSumPrevious = float(greekData['delta'])
        deltaNeutralStrike = greekData['option']
    deltaSumPrevious = deltaSumCurrent
    counteven += 1
    countodd += 1
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

    


        
