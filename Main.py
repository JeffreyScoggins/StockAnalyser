#!/usr/bin/env python3
import sys
import json
import urllib.request as ur
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import OptionsParse as op
from urllib.error import HTTPError

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

    op.deltaNeutral(stockData, charLen)
    op.gammaNeutral(stockData, charLen)
    op.gammaMax(stockData, charLen)