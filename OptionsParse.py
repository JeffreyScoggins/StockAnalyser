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
    OICall = greekDataCall['open_interest']
    OIPut = greekDataPut['open_interest']
    deltaOICall = OICall * greekDataCallDelta
    deltaOIPut = OIPut * greekDataPutDelta
    deltaSumCurrent = deltaOICall + deltaOIPut #deltaOIPut should always be negative so number is added to find difference
    if deltaSumCurrent < deltaSumPrevious: 
        deltaNeutral = float(greekData['delta'])
        deltaSumPrevious = float(greekData['delta'])
        deltaNeutralStrike = greekData['option']
        deltaSumPrevious = deltaSumCurrent
        gammaNeutralStrike = strike
    counteven += 2
    countodd += 2
print("Delta Neutral: ")
print(deltaNeutralStrike)


counteven = 0 #add 2 to keep even
countodd = 1 #add 2 to keep odd
gammaSumCurrent = 1.0 #1.0 as options delta should never be above 1.0
gammaSumPrevious = 1.0 
gammaNeutral = 0.0 
strike = ""
gammaNeutralStrike = ""
for x in range(int(len(optionsData)/2)):

    greekData = optionsData[counteven] #Subdirectory
    greekDataCall = optionsData[counteven]
    greekDataCallDelta = greekDataCall['gamma']
    greekDataPut = optionsData[countodd]
    greekDataPutDelta = greekDataPut['gamma']
    strike = greekData['option']
    OICall = greekDataCall['open_interest']
    OIPut = greekDataPut['open_interest']
    gammaOICall = OICall * greekDataCallDelta
    gammaOIPut = OIPut * greekDataPutDelta
    gammaSumCurrent = gammaOICall - gammaOIPut
    if gammaSumCurrent < gammaSumPrevious: 
        gammaNeutral = float(greekData['gamma'])
        gammaSumPrevious = float(greekData['gamma'])
        gammaNeutralStrike = greekData['option']
        gammaSumPrevious = gammaSumCurrent
        gammaNeutralStrike = strike
    counteven += 2
    countodd += 2
print("Gamma Neutral: ")
print(gammaNeutralStrike)


count = 0
gammaPrevious = 0.0
gammaMax = 0.0
gammaMaxStrike = ""

for x in range(int(len(optionsData)/2)):
    greekData = optionsData[count] #Subdirectory
    OI = greekData['open_interest']
    gamma = greekData['gamma'] + 1
    gammaMaxTemp = OI * gamma
    if float(gammaMaxTemp) > gammaPrevious:
        gammaMax = gammaMaxTemp
        gammaPrevious = gammaMaxTemp
        gammaMaxStrike = greekData['option']
    count += 2
print("Gamma Max: ")
print (gammaMaxStrike)


    


        
