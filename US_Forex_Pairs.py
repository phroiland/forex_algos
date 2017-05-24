
from __future__ import division
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
#allows us to read stock info from google, yahoo, etc.
from pandas.io.data import DataReader
#timestamps
from datetime import datetime
from pylab import figure, axes, pie, title, show

fred_currencies = ['DEXUSEU', 'DEXUSAL', 'DEXUSUK', 'DEXCAUS', 'DEXSZUS', 'DEXJPUS']

end = datetime.now()

start = datetime(end.year - 2, end.month, end.day)

for currency in fred_currencies:
    #make currencies global to call as its own dataframe
    globals()[currency] = DataReader(currency, 'fred', start, end)

print '\nUse the following list to input selected currency pair\n'
print 'Enter EURUSD as DEXUSEU\nEnter AUDUSD as DEXUSAL\nEnter GBPUSD as DEXUSUK\nEnter USDCAD as DEXCAUS\nEnter USDCHF as DEXSZUS\nEnter USDJPY as DEXJPUS\n'

currency = raw_input("Enter Currency Pair: ")

if currency == 'DEXUSEU':
	currency = DEXUSEU.dropna()
	currency.rename(columns = {'DEXUSEU':'Close'}, inplace = True)
elif currency == 'DEXUSAL':
	currency = DEXUSAL.dropna()
	currency.rename(columns = {'DEXUSAL':'Close'}, inplace = True)
elif currency == 'DEXUSUK':
	currency = DEXUSUK.dropna()
	currency.rename(columns = {'DEXUSUK':'Close'}, inplace = True)
elif currency == 'DEXCAUS':
	currency = DEXCAUS.dropna()
	currency.rename(columns = {'DEXCAUS':'Close'}, inplace = True)
elif currency == 'DEXSZUS':
	currency = DEXSZUS.dropna()
	currency.rename(columns = {'DEXSZUS':'Close'}, inplace = True)
elif currency == 'DEXJPUS':
	currency = DEXJPUS.dropna()
	currency.rename(columns = {'DEXJPUS':'Close'}, inplace = True)
else:
	print "Please enter a valid currency pair."

#currency analysis
currency = currency.dropna()
	
print '\nDaily Close Snapshot\n\n', currency.head()
print '\n', 'Description\n\n', currency.describe()
	
currencyfig = currency.plot(legend=True, figsize=(10,4))
currencyfig = currencyfig.get_figure()
currencyfig.savefig('currencyfig.png')
	
MA_day = [10, 20, 50]
	
for MA in MA_day:
    column_name = 'MA for %s days' %(str(MA))
    currency[column_name] = pd.rolling_mean(currency['Close'], MA)
	
currencyfig2 = currency[[0,1,2,3]].plot(subplots=False, figsize=(10,4))
currencyfig2 = currencyfig2.get_figure()
currencyfig2.savefig('currencyfig2.png')
	
currency.loc[:, ('Daily Return')] = currency[[0]].pct_change()
	
currencyfig3 = currency[[4]].plot(figsize=(10,4), legend=True, linestyle='--', marker='o')
currencyfig3 = currencyfig3.get_figure()
currencyfig3.savefig('currencyfig3.png')
	
currencyfig4 = sns.distplot(currency[['Daily Return']].dropna(), color='purple')
currencyfig4 = currencyfig4.get_figure()
currencyfig4.savefig('currencyfig4.png')


closing_df = DataReader(fred_currencies, 'fred', start, end)
print '\nDaily Close Snapshot'
print '\n', closing_df.head()

fred_ret = closing_df.pct_change()
print '\nDaily Return Snapshot\n'
print '\n', fred_ret.head()

print "\nSee how currency pairs correlate...\n"

currency1 = raw_input("Enter Currency 1: ")
if currency1 == 'DEXUSEU':
	currency1 = fred_ret[['DEXUSEU']].dropna()
	currency1.rename(columns = {'DEXUSEU':'Return'}, inplace = True)
elif currency1 == 'DEXUSAL':
	currency1 = fred_ret[['DEXUSAL']].dropna()
	currency1.rename(columns = {'DEXUSAL':'Return'}, inplace = True)
elif currency1 == 'DEXUSUK':
	currency1 = fred_ret[['DEXUSUK']].dropna()
	currency1.rename(columns = {'DEXUSUK':'Return'}, inplace = True)
elif currency1 == 'DEXCAUS':
	currency1 = fred_ret[['DEXCAUS']].dropna()
	currency1.rename(columns = {'DEXCAUS':'Return'}, inplace = True)
elif currency1 == 'DEXSZUS':
	currency1 = fred_ret[['DEXSZUS']].dropna()
	currency1.rename(columns = {'DEXSZUS':'Return'}, inplace = True)
else:
	currency1 = fred_ret[['DEXJPUS']].dropna()
	currency1.rename(columns = {'DEXJPUS':'Return'}, inplace = True)

currency2 = raw_input("Enter Currency 2: ")
if currency2 == 'DEXUSEU':
	currency2 = fred_ret[['DEXUSEU']].dropna()
	currency2.rename(columns = {'DEXUSEU':'Return'}, inplace = True)
elif currency2 == 'DEXUSAL':
	currency2 = fred_ret[['DEXUSAL']].dropna()
	currency2.rename(columns = {'DEXUSAL':'Return'}, inplace = True)
elif currency2 == 'DEXUSUK':
	currency2 = fred_ret[['DEXUSUK']].dropna()
	currency2.rename(columns = {'DEXUSUK':'Return'}, inplace = True)
elif currency2 == 'DEXCAUS':
	currency2 = fred_ret[['DEXCAUS']].dropna()
	currency2.rename(columns = {'DEXCAUS':'Return'}, inplace = True)
elif currency2 == 'DEXSZUS':
	currency2 = fred_ret[['DEXSZUS']].dropna()
	currency2.rename(columns = {'DEXSZUS':'Return'}, inplace = True)
else:
	currency2 = fred_ret[['DEXJPUS']].dropna()
	currency2.rename(columns = {'DEXJPUS':'Return'}, inplace = True)
	
currency1 = pd.DataFrame(currency1, columns=['Return'])
currency2 = pd.DataFrame(currency2, columns=['Return'])


# plot
# ========================================   
corr_plot = sns.jointplot(x=currency1.Return, y=currency2.Return, color='r')

corr_plot.x = currency1.Return
corr_plot.y = currency2.Return
corr_plot.plot_joint(plt.scatter, marker='x', c='b', s=50)

corr_plot.savefig('corr_plot.png')

ret_plot1 = sns.distplot(currency1[['Return']].dropna(), bins=100, color='purple')
ret_plot1.savefig('ret_plot1.png')

ret_plot2 = sns.distplot(currency2[['Return']].dropna(), bins=100, color='purple')
ret_plot2.savefig('ret_plot2.png')

pairplots = sns.pairplot(fred_ret.dropna())
pairplots.savefig('pairplots.png')

returns_fig = sns.PairGrid(fred_ret.dropna())
returns_fig.map_upper(plt.scatter, color='purple')
returns_fig.map_lower(sns.kdeplot, cmap = 'cool')
returns_fig.map_diag(plt.hist, bins=30)
returns_fig.savefig('returns_fig.png')