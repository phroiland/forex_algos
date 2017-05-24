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

'''if currency == 'DEXUSEU':
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
	print "Please enter a valid currency pair."'''

#currency analysis
#currency = currency.dropna()

#analyze risk
closing_df = DataReader(fred_currencies, 'fred', start, end)
fred_ret = closing_df.pct_change()
rets = fred_ret.dropna()
area = np.pi*20
plt.scatter(rets.mean(),rets.std(),s=area)
plt.xlabel('Expected Return')
plt.ylabel('Risk')

days = 365
dt = 1/days
mu = rets.mean()[currency]
sigma = rets.std()[currency]

def monte_carlo(start_price, days, mu, sigma):
    price = np.zeros(days)
    price[0] = start_price
    
    shock = np.zeros(days)
    drift = np.zeros(days)
    
    for x in xrange(1, days):
        shock[x] = np.random.normal(loc = mu*dt, scale = sigma*np.sqrt(dt))
        
        drift[x] = mu*dt
        
        price[x] = price[x-1] + (price[x-1]*(drift[x] + shock[x]))
    
    return price

start_price = raw_input('Enter last price: ')
start_price = float(start_price)

for run in xrange(50):
    plt.plot(monte_carlo(start_price, days, mu, sigma))
plt.xlabel('Days')
plt.ylabel('Price')
plt.title('Monte Carlo Analysis for %s' %str(currency))


runs = 10000

simulations = np.zeros(runs)
for run in xrange(runs):
    simulations[run] = monte_carlo(start_price, days, mu, sigma)[days-1]

q = np.percentile(simulations, 25)
plt.hist(simulations, bins = 200)
plt.figtext(0.6,0.8, s = 'Start Price: $%.5f' % start_price)
plt.figtext(0.6,0.7,'Mean final price: $%.5f' % simulations.mean())
plt.figtext(0.6,0.6, 'Var(0.99): $%.5f' % (start_price-q,))
plt.figtext(0.15,0.6,'q(0.99): $%.5f' % q)
plt.axvline(x=q, linewidth = 4, color = 'r')
plt.title(u'Final Price Distribution for EURUSD after %s Days' % days, weight = 'bold')

print '\nLast Price: 	%.5f' % start_price
print 'Mean Price: 	%.5f' % simulations.mean()
print 'q  (0.99) : 	%.5f' % q
print 'Var(0.99) : 	%.5f' % (start_price-q,)

#final_plot = plt.hist(simulations,bins = 200)
#final_plot = final_plot.get_figure()
#final_plot.savefig('final_plot.png')