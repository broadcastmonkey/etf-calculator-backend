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
import sys
import os
import json

pf_data = pd.read_pickle('./data/ETF_DATA.pickle')


def optimal_portfolio(score, portfolio_value):
    # Set bounds
    if score == 0:
        min_bonds = 0
        min_growth = 0
        min_value = 0
        risk_aversion_coeff = 1

    if score <= 10:
        min_bonds = 0.5
        min_growth = 0
        min_value = 0
        risk_aversion_coeff = 6

    if score > 10 and score <= 15:
        min_bonds = 0.4
        min_growth = 0.2
        min_value = 0.4
        risk_aversion_coeff = 5

    if score > 15 and score <= 20:
        min_bonds = 0.4
        min_growth = 0.2
        min_value = 0.4
        risk_aversion_coeff = 4

    if score > 20 and score <= 30:
        min_bonds = 0.3
        min_growth = 0.2
        min_value = 0.4
        risk_aversion_coeff = 3

    if score > 30 and score <= 34:
        min_bonds = 0.3
        min_growth = 0.2
        min_value = 0.4
        risk_aversion_coeff = 2

    if score > 34:
        min_bonds = 0.2
        min_growth = 0.3
        min_value = 0.4
        risk_aversion_coeff = 1

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(pf_data)
    S = risk_models.sample_cov(pf_data)
    ef = EfficientFrontier(mu, S)
    ef.add_objective(objective_functions.L2_reg)
    ef.add_constraint(lambda w: w[pf_data.columns.get_indexer(['SCHI'])]+w[pf_data.columns.get_indexer(
        ['SPBO'])]+w[pf_data.columns.get_indexer(['SCHJ'])]+w[pf_data.columns.get_indexer(['VCSH'])] >= min_bonds)
    ef.add_constraint(lambda w: w[pf_data.columns.get_indexer(['QGRO'])]+w[pf_data.columns.get_indexer(['WCLD'])]+w[pf_data.columns.get_indexer(
        ['SMOG'])]+w[pf_data.columns.get_indexer(['ERTH'])]+w[pf_data.columns.get_indexer(['CLOU'])] >= min_growth)
    ef.add_constraint(lambda w: w[pf_data.columns.get_indexer(['XLE'])]+w[pf_data.columns.get_indexer(['SPYD'])]+w[pf_data.columns.get_indexer(
        ['VALQ'])]+w[pf_data.columns.get_indexer(['IVLU'])]+w[pf_data.columns.get_indexer(['EFV'])] >= min_value)

    raw_weights = ef.max_quadratic_utility(
        risk_aversion=risk_aversion_coeff, market_neutral=False)
    cleaned_weights = ef.clean_weights()

    ret = ef.portfolio_performance(verbose=False, risk_free_rate=0.0271)
    # print(ret)
    latest_prices = get_latest_prices(pf_data)

    da = DiscreteAllocation(cleaned_weights, latest_prices,
                            total_portfolio_value=portfolio_value)
    allocation, leftover = da.greedy_portfolio()

    #print("Amount of ETF's:", allocation)
    #print("Remaining Cash: ${:.2f}".format(leftover))

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = allocation.keys()
    sizes = allocation.values()

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')

    plt.savefig('./images/diagram_'+str(score)+'.png')

    data = {
        'allocation': allocation,
        'leftover': leftover,
        'annualised_return': round(ret[0]*100, 2),
        'annualised_volatality': round(ret[1]*100, 2),
        'sharpe_ratio': round(ret[2], 3)
    }
    # "Allocation " + str(res), 'Annualised Return ' + str(round(ret, 2)), 'Annualised Volatility ' + str(round(vol, 2)), 'Sharpe Ratio ' + str(round(sharpe_r, 3))
    return json.dumps(data)


score = int(sys.argv[1])
portfolio_value = int(sys.argv[2])

print(optimal_portfolio(score, portfolio_value))


sys.exit(os.EX_OK)
