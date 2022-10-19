import sys
import os
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
# ETF = ['SCHI', 'SPBO', 'SCHJ', 'VCSH', 'QGRO', 'WCLD',
#        'SMOG', 'XLE', 'ERTH', 'SPYD', 'VALQ', 'IVLU', 'EFV']
# pf_data = pd.DataFrame()
# # Pulling closing price
# for stock in ETF:
#     pf_data[stock] = wb.DataReader(
#         stock, data_source='yahoo', start='2008-1-1')['Adj Close']
# num_stocks = len(ETF)

pf_data = pd.read_pickle('../data/ETF_DATA.pickle')


# Questionnaire input risk_aversion_coeff linked to score
def utility_optimal_portfolio(data, risk_aversion_coeff):
    # Importing libraries
    from pypfopt import EfficientFrontier
    from pypfopt import risk_models
    from pypfopt import expected_returns
    from pypfopt import objective_functions

    # Expected Returns
    mu = expected_returns.mean_historical_return(pf_data)
    # Expected Volatility
    Sigma = risk_models.sample_cov(pf_data)
    ef = EfficientFrontier(mu, Sigma)  # setup
    ef.add_objective(objective_functions.L2_reg)  # add a secondary objective
    # find the portfolio that maximizes utility
    weights = ef.max_quadratic_utility(
        risk_aversion=risk_aversion_coeff, market_neutral=False)
    ret, vol, sharpe_r = ef.portfolio_performance(risk_free_rate=0.0389)
    # loop to iterate for values
    res = dict()
    for key in weights:
        # rounding to K using round()
        res[key] = round(weights[key], 2)

    data = {
        'allocation': res,
        'annualised_return': round(ret, 2),
        'annualised_volatality': round(vol, 2),
        'sharpe_ratio': round(sharpe_r, 3)
    }
    # "Allocation " + str(res), 'Annualised Return ' + str(round(ret, 2)), 'Annualised Volatility ' + str(round(vol, 2)), 'Sharpe Ratio ' + str(round(sharpe_r, 3))
    return json.dumps(data)


risk_factor = int(sys.argv[1])

# Aggressive Investor (score 35 and more)
a = utility_optimal_portfolio(pf_data, risk_factor)
print(a)
# Moderate Investor (score 31-34)
# b = utility_optimal_portfolio(pf_data, 2)


# Moderate Investor (score 21-30)
# c = utility_optimal_portfolio(pf_data, 3)

# print("a")
# print((a))

# print("b")
# print((b))

# print("c")
# print((c))


img = Image.new('RGB', (60, 30), color='red')
img.save('../images/diagram_'+str(risk_factor)+'.png')


sys.exit(os.EX_OK)
