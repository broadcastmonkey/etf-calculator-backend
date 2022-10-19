import pypfopt
import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import numpy as np
from pandas_datareader import data, wb
import datetime
import scipy.optimize as sco
from scipy import stats
import matplotlib.pyplot as plt
from pypfopt import plotting
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import copy
from pypfopt import objective_functions

import json
# Creating a list of Stock Tickers
tickers = ['SCHI', 'SPBO', 'SCHJ', 'VCSH', 'QGRO', 'WCLD',
           'SMOG', 'ERTH', 'CLOU', 'XLE', 'SPYD', 'VALQ', 'IVLU', 'EFV']

pf_data = pd.DataFrame()
# Pulling closing price

for ticker in tickers:
    pf_data[ticker] = data.DataReader(
        ticker, data_source='yahoo', start='2010-1-1')['Adj Close']


pf_data.to_pickle('./data/ETF_DATA.pickle')

plot = (pf_data / pf_data.iloc[0] * 100).plot(figsize=(10, 5))
plot.legend(bbox_to_anchor=(1, 1))
plt.savefig('./images/etf_chart.png')
