#!/usr/bin/env python3
import sys
import json
import urllib.request as ur
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from urllib.error import HTTPError

def deltaNeutral(stockData):
    #Delta Neutal is the lowest difference between puts and calls of the same strike. This function takes the calls[even] and puts[odd] and subtracts the values
    #Since Put delta is always negative, the data is added together to find the diffence. The strike with the smallest difference is the delta neutral strike.
    #Takes optionsData lenght as int as arg. Divided by 2 due to counting by evens/odds. OutOfBounds error occurs otherwise
    #greekData is a subdirectory that contains each individual options stike data greekDataXXXXXDelta contains the delta value for each options strike

    optionsData = stockData["options"] #Subdirectory
    counteven = 0 #add 2 to keep even
    countodd = 1 #add 2 to keep odd
    deltaSumCurrent = 0.0 #1.0 as options delta should never be above 1.0
    deltaSumPrevious = 0.0 
    deltaNeutral = 0.0 
    deltaStrike = ""
    deltaNeutralStrike = ""
    for x in range(int(len(optionsData)/2)):

        greekData = optionsData[counteven] #Subdirectory
        greekDataCall = optionsData[counteven]
        greekDataCallDelta = greekDataCall['delta']
        greekDataPut = optionsData[countodd]
        greekDataPutDelta = greekDataPut['delta']
        deltaStrike = greekData['option']
        OICall = greekDataCall['open_interest']
        OIPut = greekDataPut['open_interest']
        deltaOICall = OICall * greekDataCallDelta
        deltaOIPut = OIPut * greekDataPutDelta
        deltaSumCurrent = deltaOICall + deltaOIPut #deltaOIPut should always be negative so number is added to find difference
        if deltaSumCurrent < 0.0:
            deltaSumCurrent = deltaSumCurrent * -1
        if deltaSumCurrent > deltaSumPrevious: 
            deltaNeutral = greekData['delta']
            deltaSumPrevious = greekData['delta']
            deltaNeutralStrike = greekData['option']
            deltaSumPrevious = deltaSumCurrent
            deltaNeutralStrike = deltaStrike
            deltaNeutralStrikeOG = deltaStrike
        counteven += 2
        countodd += 2
    if deltaStrike[charLen + 12] !='0': #x.xx
        deltaNeutralStrike = deltaStrike[charLen + 3] + deltaStrike[charLen + 4] + '/' + deltaStrike[charLen + 5] + deltaStrike[charLen + 6] + '/' + deltaStrike[charLen + 1] + deltaStrike[charLen + 2] + '  $' + deltaStrike[charLen + 12] + "." + deltaStrike[charLen + 13] + deltaStrike[charLen + 14]
    elif deltaStrike[charLen + 11] !='0': #xx.xx
        deltaNeutralStrike = deltaStrike[charLen + 3] + deltaStrike[charLen + 4] + '/' + deltaStrike[charLen + 5] + deltaStrike[charLen + 6] + '/' + deltaStrike[charLen + 1] + deltaStrike[charLen + 2] + '  $' + deltaStrike[charLen + 11] + deltaStrike[charLen + 12] + "." + deltaStrike[charLen + 13] + deltaStrike[charLen + 14]
    elif deltaStrike[charLen + 10] !='0':#xxx.xx
        deltaNeutralStrike = deltaStrike[charLen + 3] + deltaStrike[charLen + 4] + '/' + deltaStrike[charLen + 5] + deltaStrike[charLen + 6] + '/' + deltaStrike[charLen + 1] + deltaStrike[charLen + 2] + '  $' + deltaStrike[charLen + 10] + deltaStrike[charLen + 11] + deltaStrike[charLen + 12] + '.' + deltaStrike[charLen +13] + deltaStrike[charLen + 14]
    else: #xxxx.xx
        deltaNeutralStrike = deltaStrike[charLen + 3] + deltaStrike[charLen + 4] + '/' + deltaStrike[charLen + 5] + deltaStrike[charLen + 6] + '/' + deltaStrike[charLen + 1] + deltaStrike[charLen + 2] + '  $' + deltaStrike[charLen + 9] + deltaStrike[charLen + 10] + deltaStrike[charLen + 11] + deltaStrike[charLen + 12] + '.' + deltaStrike[charLen +13] + deltaStrike[charLen + 14]
    print("Delta Neutral:")
    print(deltaNeutralStrike)

def gammaNeutral(stockData):
    optionsData = stockData["options"] #Subdirectory
    counteven = 0 #add 2 to keep even
    countodd = 1 #add 2 to keep odd
    gammaSumCurrent = 1.0 #1.0 as options delta should never be above 1.0
    gammaSumPrevious = 1.0 
    gamma = 0.0 
    strike = ""
    gammaNeutralStrike = ""
    for x in range(int(len(optionsData)/2)):

        greekData = optionsData[counteven] #Subdirect
        greekDataCall = optionsData[counteven]
        greekDataCallDelta = greekDataCall['gamma']
        greekDataPut = optionsData[countodd]
        greekDataPutDelta = greekDataPut['gamma']
        strike = greekData['option']
        OICall = greekDataCall['open_interest']
        OIPut = greekDataPut['open_interest']
        gammaOICall = OICall * greekDataCallDelta
        gammaOIPut = OIPut * greekDataPutDelta
        gammaSumCurrent = gammaOICall + gammaOIPut
        if gammaSumCurrent > gammaSumPrevious: 
            gamma = greekData['gamma']
            gammaSumPrevious = greekData['gamma']
            gammaNeutralStrike = greekData['option']
            gammaSumPrevious = gammaSumCurrent
        counteven += 2
        countodd += 2
    if strike[charLen + 12] !='0': #x.xx
        gammaNeutralStrike = strike[charLen + 3] + strike[charLen + 4] + '/' + strike[charLen + 5] + strike[charLen + 6] + '/' + strike[charLen + 1] + strike[charLen + 2] + '  $' + strike[charLen + 12] + "." + strike[charLen + 13] + strike[charLen + 14]
    elif strike[charLen + 11] !='0': #xx.xx
        gammaNeutralStrike = strike[charLen + 3] + strike[charLen + 4] + '/' + strike[charLen + 5] + strike[charLen + 6] + '/' + strike[charLen + 1] + strike[charLen + 2] + '  $' + strike[charLen + 11] + strike[charLen + 12] + "." + strike[charLen + 13] + strike[charLen + 14]
    elif strike[charLen + 10] !='0':#xxx.xx
        gammaNeutralStrike = strike[charLen + 3] + strike[charLen + 4] + '/' + strike[charLen + 5] + strike[charLen + 6] + '/' + strike[charLen + 1] + strike[charLen + 2] + '  $' + strike[charLen + 10] + strike[charLen + 11] + strike[charLen + 12] + '.' + strike[charLen +13] + strike[charLen + 14]
    else:
        gammaNeutralStrike = strike[charLen + 3] + strike[charLen + 4] + '/' + strike[charLen + 5] + strike[charLen + 6] + '/' + strike[charLen + 1] + strike[charLen + 2] + '  $' + strike[charLen + 9] + strike[charLen + 10] + strike[charLen + 11] + strike[charLen + 12] + '.' + strike[charLen +13] + strike[charLen + 14]
    print("Gamma Neutral: ")
    print(gammaNeutralStrike)


def gammaMax(stockData):
    optionsData = stockData["options"] #Subdirectory
    count = 0
    strike = ""
    gammaMax = 0.0
    gammaMaxStrike = ""

    for x in range(300): #limited options chain to prevent end of chain outliers from skewing data
        greekData = optionsData[count] #Subdirectory
        OI = greekData['open_interest']
        gamma = greekData['gamma']
        gammaMaxTemp = (gamma + 1) * OI
        if gammaMaxTemp > gammaMax:
            gammaMax = gammaMaxTemp
            strike = greekData['option']
        count += 2
    if strike[charLen + 12] !='0': #x.xx
        gammaMaxStrike = strike[charLen + 3] + strike[charLen + 4] + '/' + strike[charLen + 5] + strike[charLen + 6] + '/' + strike[charLen + 1] + strike[charLen + 2] + '  $' + strike[charLen + 12] + "." + strike[charLen + 13] + strike[charLen + 14]
    elif strike[charLen + 11] !='0': #xx.xx
        gammaMaxStrike = strike[charLen + 3] + strike[charLen + 4] + '/' + strike[charLen + 5] + strike[charLen + 6] + '/' + strike[charLen + 1] + strike[charLen + 2] + '  $' + strike[charLen + 11] + strike[charLen + 12] + "." + strike[charLen + 13] + strike[charLen + 14]
    elif strike[charLen + 10] !='0':#xxx.xx
        gammaMaxStrike = strike[charLen + 3] + strike[charLen + 4] + '/' + strike[charLen + 5] + strike[charLen + 6] + '/' + strike[charLen + 1] + strike[charLen + 2] + '  $' + strike[charLen + 10] + strike[charLen + 11] + strike[charLen + 12] + '.' + strike[charLen +13] + strike[charLen + 14]
    else:
        gammaMaxStrike = strike[charLen + 3] + strike[charLen + 4] + '/' + strike[charLen + 5] + strike[charLen + 6] + '/' + strike[charLen + 1] + strike[charLen + 2] + '  $' + strike[charLen + 9] + strike[charLen + 10] + strike[charLen + 11] + strike[charLen + 12] + '.' + strike[charLen +13] + strike[charLen + 14]
    print('Gamma Max:')
    print(gammaMaxStrike)

while (True): #infinite loop
    try:
        ticker = input ('Enter stock ticker\n')
        url = "https://cdn.cboe.com/api/global/delayed_quotes/options/"+ticker.upper()+".json" #pulls options JSON data from CBOE for desired stock ticker
        data = ur.urlopen(url).read() #Pulls JSON data form URL 

    except HTTPError as err:
        if err.code == 403:
            print ('Invalid Entry')
            continue
    charLen = len(ticker) - 1 
    datajson = json.loads(data.decode('utf-8')) #Converts to python dictionary
    stockData = datajson["data"] #SubDirectory

    deltaNeutral(stockData)
    gammaNeutral(stockData)
    gammaMax(stockData)

    
    

                    
