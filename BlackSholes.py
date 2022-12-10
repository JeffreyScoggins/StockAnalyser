'''
S​ is the stock price
K is the strike price
r is the risk-free interest rate
σ represents the underlying volatility
T is time in years (1 month = 0.083 years)
'''
import numpy as np
from scipy.stats import norm

def BlackScholesPrice(S, K, r, sigma, T, callPut):

    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))

    d2 = d1 - sigma*np.sqrt(T)

    try:
        if callPut == 0:
            price = S*norm.cdf(d1,0,1) - K*np.exp(-r*T)*norm.cdf(d2,0,1)
        elif callPut == 1:
            price = K*np.exp(-r*T)*norm.cdf(-d2,0,1) - S*norm.cdf(-d1,0,1)
    except:
        return OverflowError






def BlackScholes(S, K, r, sigma, T, callPut):

    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    td1=d1 
    td2=d2
   
    try:
        if callPut == 0:
            option.call.price=S * ss.norm.cdf(td1) - K * np.exp(-r * T) * ss.norm.cdf(td2)
        elif callPut == 1:
            option.put.price=K * np.exp(-r * T) * ss.norm.cdf(-td2) - S0 * ss.norm.cdf(-td1)
    except:
        return OverflowError

    try:  
        if callPut == 0:
            option.call.delta=ss.norm.cdf(td1)
        elif callPut == 1:
            option.put.delta=ss.norm.cdf(td1)-1
    except:
        return OverflowError
    
    
    NPrime=((2*np.pi)**(-1/2))*np.exp(-0.5*(td1)**2)
    option.call.gamma=(NPrime/(S*sigma*T**(1/2)))
    option.put.gamma=option.call.gamma
    
    try:
        if callPut == 0:
            option.call.theta=(NPrime)*(-S*sigma*0.5/np.sqrt(T))-r*K * np.exp(-r * T) * ss.norm.cdf(td2)
        elif callPut == 1:
            option.put.theta=(NPrime)*(-S*sigma*0.5/np.sqrt(T))+r*K * np.exp(-r * T) * ss.norm.cdf(-td2)
    except:
        return OverflowError
        
    return option