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

#Delta Neutal is the lowest difference between puts and calls of the same strike. This function takes the calls[even] and puts[odd] and subtracts the values
#Since Put delta is always negative, the data is added together to find the diffence. The strike with the smallest difference is the delta neutral strike.
#Takes optionsData lenght as int as arg. Divided by 2 due to counting by evens/odds. OutOfBounds error occurs otherwise
#greekData is a subdirectory that contains each individual options stike data greekDataXXXXXDelta contains the delta value for each options strike

counteven = 0 #add 2 to keep even
countodd = 1 #add 2 to keep odd
deltaSumCurrent = 1.0 #1.0 as options delta should never be above 1.0
deltaSumPrevious = 1.0 
deltaNeutral = 0.0 
strike = ""
deltaNeutralStrike = ""
for x in range(int(len(optionsData)/2)):
    greekData = optionsData[counteven] #Subdirectory
    greekDataCall = optionsData[counteven]
    greekDataCallDelta = greekDataCall['delta']
    greekDataPut = optionsData[countodd]
    greekDataPutDelta = greekDataPut['delta']
    strike = greekData['option']
    deltaSumCurrent = float(greekDataPutDelta) + float(greekDataCallDelta) 
    abs(deltaSumCurrent)
    print("Call")
    print(greekDataCallDelta)
    print("Put")
    print(greekDataPutDelta)
    print("Delta Sum")
    print(deltaSumCurrent)
    if deltaSumCurrent < deltaSumPrevious: 
        deltaNeutral = float(greekData['delta'])
        deltaSumPrevious = float(greekData['delta'])
        deltaNeutralStrike = greekData['option']
        deltaSumPrevious = deltaSumCurrent
        deltaNeutralStrike = strike
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

    


        
