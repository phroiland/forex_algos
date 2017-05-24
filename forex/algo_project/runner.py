"""
The main file that will evolve into our trading library
"""
import v20
import common.config
import common.args
from datetime import datetime, timedelta

# Not an actual access token, enter your own token.
OANDA_ACCESS_TOKEN = '$$$$$$x$xxx$$$$x$$$$xxx$$$$$$$$$-$xx$$$$$xx$$x$$x$xxx$x$$x$$$$$x$' 
# Not an actual account id, enter your account/acccess id here. 
OANDA_ACCOUNT_ID = 'xxx-xxx-xxxxxxx-xxx'

def main():
    print "------ System online -------", datetime.now()
    latest_price_time = (datetime.utcnow() - timedelta(seconds=15)).isoformat('T')+'Z'

    api = v20.Context(
            'api-fxpractice.oanda.com',
            '443',
            token=OANDA_ACCESS_TOKEN)

    response = api.pricing.get(
                    OANDA_ACCOUNT_ID,
                    # Harcode for testing purposes only, stream.py will have the variable for instrument
                    instruments='EUR_USD',
                    since=latest_price_time,
                    includeUnitsAvailable=False)

    print response.reason, latest_price_time
    
    prices = response.get("prices", 200)
    if len(prices):
        buy_price = prices[0].bids[0].price 

        print "Buy at", buy_price

        response = api.order.market(
            OANDA_ACCOUNT_ID,
            # Harcode for testing purposes only, stream.py will have the variable for instrument
            instrument='EUR_USD',
            units=5000)

        print "Trading id", response.get('orderFillTransaction').id
        print "Account Balance", response.get('orderFillTransaction').accountBalance
        print "Price", response.get('orderFillTransaction').price
        
    else:
        print response.reason

if __name__ == "__main__":
    main()
