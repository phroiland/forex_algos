#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 03:09:23 2017

@author: johnfroiland
"""

#!/usr/bin/env python
import csv
import pandas as pd
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.max_columns', 0)
import argparse
import common.config
import common.args
from view_backtest import CandlePrinter 
#currency_string,time_string,bid_string,ask_string,mid_string,price_to_string,date_string,time_value
from datetime import datetime, timedelta

def main():
    """
    Create an API context, and use it to fetch candles for an instrument.

    The configuration for the context is parsed from the config file provided
    as an argumentV
    """

    parser = argparse.ArgumentParser()

    #
    # The config object is initialized by the argument parser, and contains
    # the REST APID host, port, accountID, etc.
    #
    common.config.add_argument(parser)

    parser.add_argument(
        "instrument",
        type=common.args.instrument,
        help="The instrument to get candles for"
    )

    parser.add_argument(
        "--mid", 
        action='store_true',
        help="Get midpoint-based candles"
    )

    parser.add_argument(
        "--bid", 
        action='store_true',
        help="Get bid-based candles"
    )

    parser.add_argument(
        "--ask", 
        action='store_true',
        help="Get ask-based candles"
    )

    parser.add_argument(
        "--smooth", 
        action='store_true',
        help="'Smooth' the candles"
    )

    parser.set_defaults(mid=False, bid=False, ask=False)

    parser.add_argument(
        "--granularity",
        default=None,
        help="The candles granularity to fetch"
    )

    parser.add_argument(
        "--count",
        default=None,
        help="The number of candles to fetch"
    )

    parser.add_argument(
        "--from-time",
        default=None,
        type=common.args.date_time(),
        help="The start date for the candles to be fetched. Format is 'YYYY-MM-DD HH:MM:SS'"
    )

    parser.add_argument(
        "--to-time",
        default=None,
        type=common.args.date_time(),
        help="The end date for the candles to be fetched. Format is 'YYYY-MM-DD HH:MM:SS'"
    )

    parser.add_argument(
        "--alignment-timezone",
        default=None,
        help="The timezone to used for aligning daily candles"
    )

    args = parser.parse_args()
    #
    # The v20 config object creates the v20.Context for us based on the
    # contents of the config file.
    #
    api = args.config.create_context()

    kwargs = {}

    if args.granularity is not None:
        kwargs["granularity"] = args.granularity

    if args.smooth is not None:
        kwargs["smooth"] = args.smooth

    if args.count is not None:
        kwargs["count"] = args.count

    if args.from_time is not None:
        kwargs["fromTime"] = api.datetime_to_str(args.from_time)

    if args.to_time is not None:
        kwargs["toTime"] = api.datetime_to_str(args.to_time)

    if args.alignment_timezone is not None:
        kwargs["alignmentTimezone"] = args.alignment_timezone

    candle = "mid"

    if args.mid:
        kwargs["price"] = "M" + kwargs.get("price", "")
        candle = "mid"

    if args.bid:
        kwargs["price"] = "B" + kwargs.get("price", "")
        candle = "bid"

    if args.ask:
        kwargs["price"] = "A" + kwargs.get("price", "")
        candle = "ask"
    
    #
    # Fetch the candles
    #
    response = api.instrument.candles(args.instrument, **kwargs)

    if response.status != 200:
        print(response)
        print(response.body)
        return
    instrument = response.get("instrument", 200)
    printer = CandlePrinter()
    
    # DataFrames for storage and computation
    #time_string_data = pd.DataFrame([])
    #time_delta = pd.DataFrame([])
    df = pd.DataFrame([])
    # Constant time start
    #start = datetime.now()
    #df1 = pd.DataFrame({'TimeS':[start]})
    #minute = pd.DataFrame([])
    minuteData = pd.DataFrame([])
    open_long = pd.DataFrame({'Long':[None]})
    open_short = pd.DataFrame({'Short':[None]})
    stop_loss = pd.DataFrame({'Stop':[None]})
    total_pips = pd.DataFrame({'Pips':[None]})
    positions = pd.DataFrame([])
    positions = pd.concat([open_long, open_short, stop_loss, total_pips], axis=1, join='outer')
    #print positions     
    
    # Open/create a file to append data to.
    
    #headers = ["Long", "Short", "Stop", "Pips"]
    for candle in response.get("candles", 200):
        print instrument, printer.print_candle(candle)
        
        
        
        # DataFrames for storage and computation
        #time_string_data = pd.DataFrame([])
        #time_delta = pd.DataFrame([])
        #df = pd.DataFrame([])
        # Constant time start
        #start = "2017-05-25 21:00:00"
        #df1 = pd.DataFrame({'TimeS':[start]})
        #minute = pd.DataFrame([])
        minuteData = pd.DataFrame([])
        #
        # Print out each price as it is receive
        #
        """       
        for msg_type, msg in response.parts():
            
            if msg_type == "pricing.Heartbeat" and args.show_heartbeats:
                print heartbeat_to_string(msg)
            
            if msg_type == "pricing.Price":
        """
        now = datetime.strptime(printer.time_value(candle), "%Y-%m-%d %H:%M:%S")
        #print now
        """
        time_hash = str(now)
        time_hash = time_hash[17:19]
        timeD = now - start
        """
        
        
        df5 = pd.DataFrame({'Time':[now]})
        #df4 = pd.DataFrame({'Bid': [bid_string(msg)]})
        #df5 = pd.DataFrame({'Ask': [ask_string(msg)]})
        df6 = pd.DataFrame({'Mid':[float(printer.mid_string(candle))]})
        df7 = pd.concat([df5,df6], axis=1, join='inner')
        df7 = df7.set_index(['Time'])
        df7.index = pd.to_datetime(df7.index, unit='s')
        df = df.append(df7)
        xx = df.to_period(freq="s")
        
        #openCol = pd.DataFrame(xx.Mid)
        openCol2 = xx.resample("min").first()
        
        #highCol = pd.DataFrame(xx.Mid)
        highCol2 = xx.resample("min").max()

        #lowCol = pd.DataFrame(xx.Mid)
        lowCol2 = xx.resample("min").min()

        #closeCol = pd.DataFrame(xx.Mid)
        closeCol2 = xx.resample("min").last()
        
        minuteData = pd.concat([openCol2,highCol2,lowCol2,closeCol2], axis=1, join='inner')
        minuteData['Open'] = openCol2.round(5)
        minuteData['High'] = highCol2.round(5)
        minuteData['Low'] = lowCol2.round(5)
        minuteData['Close'] = closeCol2.round(5)
        minuteData['20 High Close'] = minuteData['Close'].rolling(20).max()
        minuteData['20 Low Close'] = minuteData['Close'].rolling(20).min()
        minuteData['10 High Close'] = minuteData['Close'].rolling(10).max()
        minuteData['10 Low Close'] = minuteData['Close'].rolling(10).min()
        minuteData['HL'] = minuteData['High']-minuteData['Low']
        minuteData['HC'] = minuteData['High']-minuteData['Close']
        minuteData['CL'] = minuteData['Close']-minuteData['Low']
        minuteData['True Range'] = minuteData[['HL','HC','CL']].max(axis=1).round(5)
        minuteData['N'] = minuteData.rolling('1min', 20)['True Range'].mean().round(5)
        minuteData['$Volatility'] = minuteData['N']*minuteData['Close']*100
        minuteData['Account'] = .01*100000
        minuteData['Lot Size'] = minuteData['Account']/minuteData['$Volatility']
        minuteData['Lot Size'] = minuteData['Lot Size'].round(0)
        
        minuteData = minuteData[['Open','High','Low','Close','20 High Close',
                    '10 High Close','20 Low Close','10 Low Close','True Range',
                    'N','$Volatility','Lot Size']]
        
        #print minuteData, '\n\n' 
        print "Rows in minuteData: ", minuteData.shape[0]
        print "Rows in df: ", df.shape[0]
        
        """
        time_seconds = str(timeD)[5:7]
        time_ms = str(timeD)[8:]
        timeD = float(time_seconds + '.' + time_ms)
        """
        
        if (
                minuteData.shape[0] > 20 and \
                minuteData['High'][-1] > minuteData['20 High Close'][-2] and \
                positions.iloc[0]['Short'] != None
            ):
            positions['Stop'] = minuteData['High'][-1]
            positions['Pips'] = positions['Short'] - positions['Stop']
            positions['Short'] = None
            print('**********************************')
            print('STOP')
            print('**********************************')
        elif (
                minuteData.shape[0] > 20 and \
                minuteData['High'][-1] > minuteData['20 High Close'][-2] and \
                positions.iloc[0]['Long'] == None
            ):
            positions['Long'] = minuteData['High'][-1]
            print('**********************************')
            print(positions['Long'][0], minuteData['20 High Close'][-2])
            print('LONG')
            print('**********************************')
        elif (
                minuteData.shape[0] > 20 and \
                minuteData['Low'][-1] < minuteData['20 Low Close'][-2] and \
                positions.iloc[0]['Long'] != None
            ):
            positions['Stop'] = minuteData['Low'][-1]
            positions['Pips'] = positions['Stop'] - positions['Long'] 
            positions['Long'] = None
            print('**********************************')
            print('STOP')
            print('**********************************')
        elif (
                minuteData.shape[0] > 20 and \
                minuteData['Low'][-1] < minuteData['20 Low Close'][-2] and \
                positions.iloc[0]['Short'] == None
            ):
            positions['Short'] = minuteData['Low'][-1]
            print('**********************************')
            print(positions['Short'][0], minuteData['20 Low Close'][-2])
            print("SHORT")
            print('**********************************')
       
        with open('Backtest.csv', 'a') as f:
            positions.to_csv(f, index=False, header=False, sep=',')
            positions['Stop'] = 0
            positions['Pips'] = 0
    

if __name__ == "__main__":
    main()
