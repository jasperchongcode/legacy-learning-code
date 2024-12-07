import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import plotly.offline as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import seaborn as sns

pyo.init_notebook_mode(connected=True)

pd.options.plotting.backend = 'plotly'

import statsmodels
from statsmodels.tsa.stattools import coint
from statsmodels.distributions.empirical_distribution import ECDF
from statsmodels.distributions.copula.api import (
    CopulaDistribution, GumbelCopula, IndependenceCopula)
# just set the seed for the random number generator
np.random.seed(107)

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

import matplotlib.pyplot as plt



class strategy():
    def __init__(self) -> None:
        pass
        self.copula = None
        self.theta = None
        self.

    def run():
        pass

    def 
