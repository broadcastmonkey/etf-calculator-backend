from PIL import Image
import scipy.optimize as sco
import pypfopt
import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt

import json

# %matplotlib inline
# Creating a list of Stock Tickers
ETF = ['SCHI', 'SPBO', 'SCHJ', 'VCSH', 'QGRO', 'WCLD',
       'SMOG', 'XLE', 'ERTH', 'SPYD', 'VALQ', 'IVLU', 'EFV']
pf_data = pd.DataFrame()
# Pulling closing price
for stock in ETF:
    pf_data[stock] = wb.DataReader(
        stock, data_source='yahoo', start='2008-1-1')['Adj Close']
num_stocks = len(ETF)

pf_data.to_pickle('../data/ETF_DATA.pickle')
