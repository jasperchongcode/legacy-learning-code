import pickle

#fixing error
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
import datetime as dt
import numpy as np
import scipy.stats as stats
from tqdm import tqdm
import pyvinecopulib as pv

# for the cointegration approach
from statsmodels.tsa.stattools import coint
from statsmodels.distributions.empirical_distribution import ECDF

"""Distance approach: This approach represents the most intensively researched pairs trading framework. In the formation period, various distance metrics are leveraged to identify
comoving securities. In the trading period, simple nonparametric threshold rules are used to
trigger trading signals. The key assets of this strategy are its simplicity and its transparency,
allowing for large scale empirical applications. The main findings establish distance pairs
trading as profitable across different markets, asset classes and time frames."""

""" Cointegration approach: Here, cointegration tests are applied to identify comoving securities in a formation period. In the trading period, simple algorithms are used to generate
trading signals; the majority of them based on GGR’s threshold rule. The key benefit of these
strategies is the econometrically more reliable equilibrium relationship of identified pairs."""

class pair_selection:
    
    def __init__(self, data) -> None:
        self.data = data
        self.stocks = list(data.columns)
        self.window = 90 # lookback days

        self.get_log_returns()
        self.get_ecdf()

    def get_log_returns(self): # drops the first term
        self.log_return_data = (np.log(self.data) - np.log(self.data.shift(1)))[1:]

    def get_ecdf(self):
        self.ecdf_data = self.log_return_data.apply(lambda x: [ECDF(x)(a) for a in x])


    def kendall_tau(self, num_pairs = 100):
        """
        kendall tau
        """
        out = {}
        # def calculate_kendall_tau(S1, S2): 
        #     # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kendalltau.html#scipy-stats-kendalltau

        #     # calculate log returns and drop nan at start
        #     x = (np.log(S1) - np.log(S1.shift(1)))[1:]
        #     y = (np.log(S2) - np.log(S2.shift(1)))[1:]
        #     #print(x.head(),y.head())
        #     return stats.kendalltau(x,y)


        
        for r in tqdm(range(0, len(self.stocks))):
            for c in range(1, len(self.stocks)):
                if (self.stocks[r], self.stocks[c]) not in out.keys() and (self.stocks[c], self.stocks[r]) not in out.keys():
                    #tau = calculate_kendall_tau(self.data[self.stocks[r]], self.data[self.stocks[c]])
                    tau = stats.kendalltau(self.log_return_data[self.stocks[r]], self.log_return_data[self.stocks[c]])

                    if tau[1] <= 0.05 and (self.stocks[r] != self.stocks[c]): # if the pvalue
                        #print(self.stocks[r],self.stocks[c],'valid')
                        out[self.stocks[r], self.stocks[c]] = tau[0]
                    #print(self.stocks[r], self.stocks[c], "tau:",tau[0],"pvalue:",tau[1])

        #pair = max(out, key=out.get)
        pairs = sorted(out, key=out.get, reverse=True)[:num_pairs]

        self.pair = pairs[0]
        return pairs


    def cointegration(self):
        """
        two step cointegration
        
        """

        out = {}
        for r in tqdm(range(0, len(self.stocks))):
            for c in range(1, len(self.stocks)):
                if (self.stocks[r], self.stocks[c]) not in out.keys() and (self.stocks[c], self.stocks[r]) not in out.keys() and (self.stocks[r] != self.stocks[c]):
                    # make this log returns
                    co = coint(self.log_return_data[self.stocks[r]], self.log_return_data[self.stocks[c]])
                    if co[1] <= 0.05: # if the pvalue
                        #print(self.stocks[r],self.stocks[c],'valid')

                        # base it off p-value for now (rather than t-statistic)
                        out[self.stocks[r], self.stocks[c]] = co[1]
                    #print(self.stocks[r], self.stocks[c], "tau:",tau[0],"pvalue:",tau[1])

        # pair = min(out, key=out.get)
        # self.pair = pair
        pairs = sorted(out, key=out.get, reverse=False)#[:num_pairs]
        return pairs
    

    def correlation(self):
        """ pearson rank correlation
        """

        out = {}
        for r in tqdm(range(0, len(self.stocks))):
            for c in range(1, len(self.stocks)):
                if (self.stocks[r], self.stocks[c]) not in out.keys() and (self.stocks[c], self.stocks[r]) not in out.keys() and (self.stocks[r] != self.stocks[c]):
                    # make this log returns
                    # pearson correlation coefficient
                    co = np.corrcoef(self.log_return_data[self.stocks[r]], self.log_return_data[self.stocks[c]])
                    out[self.stocks[r], self.stocks[c]] = co[0][1]
                    #print(self.stocks[r], self.stocks[c], "tau:",tau[0],"pvalue:",tau[1])

        pair = max(out, key=out.get)
        self.pair = pair
        return pair


#! write an in depth thing that checks or creates signals each loop
# use stuff like self.buy(S1, weight), self.exit_pos() etc.
class signal_creation:
    def __init__(self) -> None:
        pass

    def backtest(self):
        pass



def get_data(stocks, start, end):
    stockData = pdr.get_data_yahoo(stocks, start, end)
    stockData = stockData['Close']
    return stockData
    
def main():

    # import the ticker list (webscraped from wikipedia)
    with open('/Users/jasperchong/PycharmProjects/Statistical Arbitrage/Copulas pair trading/data/constituents.pkl', 'rb') as f:
        tickers = pickle.load(f)

    # import the data
    # end = dt.datetime(2023, 1, 1)
    # start = dt.datetime(2020,1,1)

    # data = get_data(tickers, start, end)
    # # drop all columns with nan values
    # data = data.dropna(axis=1)

    # save the data
    # with open('/Users/jasperchong/PycharmProjects/Statistical Arbitrage/Copulas pair trading/data/data.pkl', 'wb') as f:
    #     pickle.dump(data, f)

    # import the saved data to save time
    with open('/Users/jasperchong/PycharmProjects/Statistical Arbitrage/Copulas pair trading/data/data.pkl', 'rb') as f:
        data = pickle.load(f)

    selector = pair_selection(data)

    _pair = selector.kendall_tau()
    # print(out)
    # print(max(out))
    # print(max(out), key=out.get)
    print(_pair[0], _pair[1])


if __name__ == "__main__":
    main()