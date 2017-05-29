#!/usr/bin/env python

import pandas as pd
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.max_columns', 0)
import argparse
import common.config
import common.args
from view import mid_string, heartbeat_to_string, price_to_string, currency_string
from datetime import datetime
#import threading
from order_response import print_order_create_response_transactions

def main():
    
    #
    # Stream the prices for a list of Instruments for the active Account.
    #
    print "------ System online -------", datetime.now()

    parser = argparse.ArgumentParser()

    common.config.add_argument(parser)
    
    parser.add_argument(
        '--instrument', "-i",
        type=common.args.instrument,
        required=True,
        action="append",
        help="Instrument to get prices for"
    )

    parser.add_argument(
        '--snapshot',
        action="store_true",
        default=True,
        help="Request an initial snapshot"
    )

    parser.add_argument(
        '--no-snapshot',
        dest="snapshot",
        action="store_false",
        help="Do not request an initial snapshot"
    )

    parser.add_argument(
        '--show-heartbeats', "-s",
        action='store_true',
        default=False,
        help="display heartbeats"
    )

    args = parser.parse_args()

    account_id = args.config.active_account
    
    api = args.config.create_streaming_context()
    
    #
    # Subscribe to the pricing stream
    #
    
    response = api.pricing.stream(
        account_id,
        snapshot=args.snapshot,
        instruments=",".join(args.instrument),
    )
    
    """
        # Need to create two separate threads: One for the trading loop
        # and another for the market price streaming class
        
        trade_thread = threading.Thread(target=trade_response)
        price_thread = threading.Thread(target=response)
    
        # Start both threads
        print("Starting trading thread")
        trade_thread.start()
        print("Starting price streaming thread")
        price_thread.start()
    """
    """
        df: Used to track streams of pricing data as they are received.
        minuteData: Tracks df data and resamples it to OHLC every minute.
        positions: Temporarily stores prices in DataFrame when establishing or 
            closing a position. Saves to csv the trades initiated and results.
    """
    df = pd.DataFrame([])
    minuteData = pd.DataFrame([])
    open_instruments = pd.DataFrame({'Instruments':[None]})
    open_units = pd.DataFrame({'Units':[None]})
    open_long = pd.DataFrame({'Long':[None]})
    open_short = pd.DataFrame({'Short':[None]})
    stop_loss = pd.DataFrame({'Stop':[None]})
    total_pips = pd.DataFrame({'Pips':[None]})
    positions = pd.DataFrame([])
    positions = pd.concat([open_instruments,open_units,open_long,open_short,
                           stop_loss,total_pips],axis=1, join='outer')
    #
    # Print out each price as it is receive
    #       
    for msg_type, msg in response.parts():
        if msg_type == "pricing.Heartbeat" and args.show_heartbeats:
                print heartbeat_to_string(msg)
            
        if msg_type == "pricing.Price":
            print(price_to_string(msg))
            #now = datetime.strptime(printer.time_value(candle), "%Y-%m-%d %H:%M:%S")
            #print now
            now = datetime.now()
            df5 = pd.DataFrame({'Time':[now]})
            df6 = pd.DataFrame({'Mid':[float(mid_string(msg))]})
            df7 = pd.concat([df5,df6], axis=1, join='inner')
            df7 = df7.set_index(['Time'])
            df7.index = pd.to_datetime(df7.index, unit='s')
            df = df.append(df7)
            
            #
            # Resample the data to OHLC candles and indexed by Timestamp
            #
            xx = df.to_period(freq="s")
            openCol2 = xx.resample("min").first()
            highCol2 = xx.resample("min").max()
            lowCol2 = xx.resample("min").min()
            closeCol2 = xx.resample("min").last()
            minuteData = pd.concat([openCol2,highCol2,lowCol2,closeCol2],
                                   axis=1, join='inner')
            
            minuteData['Open'] = openCol2.round(5)
            minuteData['High'] = highCol2.round(5)
            minuteData['Low'] = lowCol2.round(5)
            minuteData['Close'] = closeCol2.round(5)
            minuteData['20 High Close'] = minuteData['Close'].rolling(20).max()
            minuteData['20 Low Close'] = minuteData['Close'].rolling(20).min()
            minuteData['HL'] = minuteData['High']-minuteData['Low']
            minuteData['HC'] = minuteData['High']-minuteData['Close']
            minuteData['CL'] = minuteData['Close']-minuteData['Low']
            minuteData['True Range'] = minuteData[['HL','HC','CL']].max(axis=1).round(5)
            minuteData['N'] = minuteData.rolling('1min', 20)['True Range'].mean().round(5)
            minuteData['$Volatility'] = minuteData['N']*minuteData['Close']*100
            minuteData['Account'] = .01*100000
            minuteData['Lot Size'] = minuteData['Account']/minuteData['$Volatility']
            minuteData['Lot Size'] = minuteData['Lot Size'].fillna(0.0).astype(int)
            minuteData = minuteData[['Open','High','Low','Close','20 High Close',
                        '20 Low Close','True Range',
                        'N','$Volatility','Lot Size']]
            
            #print minuteData, '\n\n' 
            print "df:",df.shape[0]," minuteData:",minuteData.shape[0]
            if (
                    minuteData.shape[0] > 20 and \
                    minuteData['High'][-1] > minuteData['20 High Close'][-2] and \
                    positions.iloc[0]['Short'] is not None
                ):
                api = args.config.create_context()
                units = minuteData['Lot Size'][-1].astype('str') 
                currency = currency_string(msg)
                side = 'sell'
                trade_response = api.order.market(
                    account_id,
                    instrument=currency,
                    units=units,
                    side=side
                )
                #print trade_response
                positions['Instrument'] = currency_string(msg)
                positions['Units'] = minuteData['Low'][-1]
                positions['Side'] = 'sell'
                positions['Stop'] = minuteData['High'][-1]
                positions['Pips'] = positions['Short'] - positions['Stop']
                positions['Short'] = None
                #print('**********************************')
                #print('STOP')
                #print('**********************************')
                #
                # Process the response
                #
                print("Response: {} ({})".format(
                        trade_response.status,trade_response.reason))

                print("")
                print_order_create_response_transactions(trade_response)
                
            elif (
                    minuteData.shape[0] > 20 and \
                    minuteData['High'][-1] > minuteData['20 High Close'][-2] and \
                    positions.iloc[0]['Long'] is None
                ):
                api = args.config.create_context()
                units = minuteData['Lot Size'][-1].astype('str') 
                currency = currency_string(msg)
                side = 'buy'
                trade_response = api.order.market(
                    account_id,
                    instrument=currency,
                    units=units,
                    side=side
                )
                #print trade_response
                positions['Instrument'] = currency_string(msg)
                positions['Units'] = minuteData['Lot Size'][-1]
                positions['Side'] = 'buy'
                positions['Long'] = minuteData['High'][-1]
                #print('**********************************')
                #print(positions['Long'][0], minuteData['20 High Close'][-2])
                #print('LONG')
                #print('**********************************')
                #
                # Process the response
                #
                print("Response: {} ({})".format(
                        trade_response.status,trade_response.reason))

                print("")
                print_order_create_response_transactions(trade_response)
                
            elif (
                    minuteData.shape[0] > 20 and \
                    minuteData['Low'][-1] < minuteData['20 Low Close'][-2] and \
                    positions.iloc[0]['Long'] is not None
                ):
                api = args.config.create_context()
                units = minuteData['Lot Size'][-1].astype('str') 
                currency = currency_string(msg)
                side = 'buy'
                trade_response = api.order.market(
                    account_id,
                    instrument=currency,
                    units=units,
                    side=side
                )
                #print trade_response
                positions['Instrument'] = currency_string(msg)
                positions['Units'] = minuteData['Lot Size'][-1]
                positions['Stop'] = minuteData['Low'][-1]
                positions['Pips'] = positions['Stop'] - positions['Long'] 
                positions['Long'] = None
                #print('**********************************')
                #print('STOP')
                #print('**********************************')
                #
                # Process the response
                #
                print("Response: {} ({})".format(
                        trade_response.status,trade_response.reason))

                print("")
                print_order_create_response_transactions(trade_response)
                
            elif (
                    minuteData.shape[0] > 20 and \
                    minuteData['Low'][-1] < minuteData['20 Low Close'][-2] and \
                    positions.iloc[0]['Short'] is None
                ):
                api = args.config.create_context()
                units = minuteData['Lot Size'][-1].astype('str') 
                currency = currency_string(msg)
                side = 'sell'
                trade_response = api.order.market(
                    account_id,
                    instrument=currency,
                    units=units,
                    side=side
                )
                #print trade_response
                positions['Instrument'] = currency_string(msg)
                positions['Units'] = minuteData['Lot Size'][-1]
                positions['Short'] = minuteData['Low'][-1]
                #print('**********************************')
                #print(positions['Short'][0], minuteData['20 Low Close'][-2])
                #print("SHORT")
                #print('**********************************')
                #
                # Process the response
                #
                print("Response: {} ({})".format(
                        trade_response.status,trade_response.reason))

                print("")
                print_order_create_response_transactions(trade_response)
                

            #with open('Backtest.csv', 'a') as f:
                #positions.to_csv(f, index=False, header=False, sep=',')
                #positions['Stop'] = 0
                #positions['Pips'] = 0
                
if __name__ == "__main__":
    main()
