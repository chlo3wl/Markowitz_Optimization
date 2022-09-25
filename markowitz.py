import numpy as np
import pandas as pd
import pandas_datareader.data as wb
import datetime 
from datetime import date
import random
import itertools
from random import sample
from constants import * 

# Define function to get markowitz optimized weights for list of tickers. 
def get_weights(tickers):
    end = date.today()
    start = end - datetime.timedelta(days=365)

    f = wb.DataReader(tickers, 'yahoo', start, end)
    f = f['Adj Close']
    rf = 0.05

    p_ret = [] 
    p_vol = [] 
    p_weights = []
    p_SR = []

    num_assets = len(f.columns)
    num_portfolios = 10000

    logReturns = np.log(f/f.shift(1))
    mu = logReturns.mean()*250
    cov = logReturns.cov()*250
    corr = logReturns.corr()

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights/np.sum(weights)
        p_weights.append(weights)
        returns = np.dot(weights, mu)  
        p_ret.append(returns)
        var = np.dot(weights.T, np.dot(cov, weights))
        sd = np.sqrt(var)
        p_vol.append(sd)
        SR = (returns-rf)/sd
        p_SR.append(SR)

    data = {'Returns':p_ret, 'Volatility':p_vol, 'Sharpe-Ratio':p_SR}

    for counter, symbol in enumerate(f.columns.tolist()):
        data[symbol] = [w[counter] for w in p_weights]

    portfolios  = pd.DataFrame(data)

    optimal_risky_portfolio = portfolios.iloc[portfolios['Sharpe-Ratio'].idxmax()]
    optimal_risky_portfolio = optimal_risky_portfolio.iloc[3:].reset_index()
    stock_list = list(zip(optimal_risky_portfolio.iloc[:, 0], optimal_risky_portfolio.iloc[:, 1].round(4)))
    
    return stock_list


# Define function to get random markowitz portfolio for risk preference.
def get_stocks_given_risk_tolerance(risk_tolerance):
    end = date.today()
    start = end - datetime.timedelta(days=365)
    
    all_symbols = ['MMM', 'AOS', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADM', 'ADBE', 'ADP', 'AAP', 'AES', 'AFL', 
                   'A', 'AIG', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 
                   'MO', 'AMZN', 'AMCR', 'AMD', 'AEE', 'AAL', 'AEP', 'AXP', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 
                   'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ANET', 'AIZ', 
                   'T', 'ATO', 'ADSK', 'AZO', 'AVB', 'AVY', 'BKR', 'BALL', 'BAC', 'BBWI', 'BAX', 'BDX', 'WRB', 
                   'BBY', 'BIO', 'TECH', 'BIIB', 'BLK', 'BK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 
                   'AVGO', 'BR', 'BRO', 'CHRW', 'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 
                   'CARR', 'CTLT', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'CNC', 'CNP', 'CDAY', 'CERN', 'CF', 'CRL', 
                   'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 
                   'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'ED', 'STZ', 'CEG', 
                   'COO', 'CPRT', 'GLW', 'CTVA', 'COST', 'CTRA', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 
                   'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DISH', 'DIS', 'DG', 'DLTR',
                   'D', 'DPZ', 'DOV', 'DOW', 'DTE', 'DUK', 'DRE', 'DD', 'DXC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX',
                   'EW', 'EA', 'EMR', 'ENPH', 'ETR', 'EOG', 'EPAM', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ETSY', 
                   'RE', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS', 'FAST', 'FRT', 'FDX', 
                   'FITB', 'FRC', 'FE', 'FIS', 'FISV', 'FLT', 'FMC', 'F', 'FTNT', 'FTV', 'FBHS', 'FOXA', 'FOX', 
                   'BEN', 'FCX', 'AJG', 'GRMN', 'IT', 'GE', 'GNRC', 'GD', 'GIS', 'GPC', 'GILD', 'GL', 'GPN', 'GM', 
                   'GS', 'GWW', 'HAL', 'HIG', 'HAS', 'HCA', 'PEAK', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 
                   'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUM', 'HII', 'HBAN', 'IEX', 'IDXX', 'ITW', 'ILMN', 
                   'INCY', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IPGP', 'IQV', 
                   'IRM', 'JBHT', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 
                   'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN', 'LLY', 'LNC', 'LIN', 'LYV', 
                   'LKQ', 'LMT', 'L', 'LOW', 'LUMN', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 
                   'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'FB', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 
                   'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 
                   'NDAQ', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NDSN', 'NSC', 
                   'NTRS', 'NOC', 'NLOK', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC',
                   'OKE', 'ORCL', 'OGN', 'OTIS', 'PCAR', 'PKG', 'PARA', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PENN', 'PNR', 
                   'PEP', 'PKI', 'PFE', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 
                   'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX',
                   'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 
                   'SBAC', 'SLB', 'STX', 'SEE', 'SRE', 'NOW', 'SHW', 'SBNY', 'SPG', 'SWKS', 'SJM', 'SNA', 'SEDG',
                   'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STE', 'SYK', 'SIVB', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 
                   'TTWO', 'TPR', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO', 
                   'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TWTR', 'TYL', 'TSN', 'USB', 'UDR', 'ULTA', 'UAA', 'UA', 
                   'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UHS', 'VLO', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VFC', 
                   'VTRS', 'V', 'VNO', 'VMC', 'WAB', 'WMT', 'WBA', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 
                   'WDC', 'WRK', 'WY', 'WHR', 'WMB', 'WTW', 'WYNN', 'XEL', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']

    dstocks = sample(all_symbols, 10)
    
    f = wb.DataReader(dstocks, 'yahoo', start, end)['Adj Close']

    combinations = list(itertools.combinations(dstocks, 10))

    combinationslist = []

    for i in combinations:
        combinationslist.append(list(i))

    for i in combinationslist:
    
        p_ret = [] 
        p_vol = [] 
        p_weights = []
        p_SR = []

        num_portfolios = 10000

        logReturns = np.log(f/f.shift(1))
        mu = logReturns.mean()*250
        cov = logReturns.cov()*250
        corr = logReturns.corr()

        for portfolio in range(num_portfolios):
            n = len(i)
            weights = [random.random() for e in range(n)]
            weights = weights/np.sum(weights)
            p_weights.append(weights)
            returns = np.dot(weights, mu) 
            p_ret.append(returns)
            var = np.dot(weights.T, np.dot(cov, weights))
            sd = np.sqrt(var)
            sd = round(sd, 2)
            p_vol.append(sd)
            SR = (returns-rf)/sd
            p_SR.append(SR)

        data = {'Returns':p_ret, 'Volatility':p_vol, 'Sharpe-Ratio':p_SR}

        for counter, symbol in enumerate(f.columns.tolist()):
            data[symbol] = [w[counter] for w in p_weights]
        
        portfolios  = pd.DataFrame(data)
        
        portfolios = portfolios[portfolios['Volatility'] <= risk_tolerance]
        portfolios = portfolios[portfolios["Sharpe-Ratio"] == portfolios["Sharpe-Ratio"].max()]
        portfolios = portfolios.transpose().reset_index()
        
        portfolios = portfolios.iloc[3:]
        stock_list = list(zip(portfolios.iloc[:, 0], portfolios.iloc[:, 1].round(4)))
        
        return stock_list