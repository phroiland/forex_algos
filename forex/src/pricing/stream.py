#!/usr/bin/env python

import csv
import pandas as pd
import gc
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.max_columns', 0)
import argparse
import common.config
import common.args
import v20
from view import currency_string,time_string,bid_string,ask_string
from view import mid_string,price_to_string,date_string,time_value
from view import print_order_create_response_transactions   
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def main():
    """
    Stream the prices for a list of Instruments for the active Account.
    """
    print "------ System online -------", datetime.now()
    latest_price_time = (datetime.utcnow() - timedelta(seconds=15)).isoformat('T')+'Z'

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

    # api.set_convert_decimal_number_to_native(False)

    # api.set_stream_timeout(3)

    #
    # Subscribe to the pricing stream
    #
    response = api.pricing.stream(
        account_id,
        snapshot=args.snapshot,
        instruments=",".join(args.instrument),
    )

    """
    # Open/create a file for CURRENT DATE to append data to.
    date = datetime.now().date()
    csvFile = open('%s.csv' % date, 'a')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["Currency", "Time", "Bid", "Ask"])
    csvFile2 = open('%s_OHLC.csv' % date, 'a')
    csvWriter2 = csv.writer(csvFile2)
    csvWriter2.writerow(["Currency", "Time", "Open", "High", "Low", "Close", "20 Period High", "20 Period Low"])
    """

    # DataFrames for storage and computation
    time_string_data = pd.DataFrame([])
    time_delta = pd.DataFrame([])
    df = pd.DataFrame([])
    # Constant time start
    start = datetime.now()
    #df1 = pd.DataFrame({'TimeS':[start]})
    minute = pd.DataFrame([])
    minuteData = pd.DataFrame([])
    #
    # Print out each price as it is receive
    #       
    for msg_type, msg in response.parts():
        if msg_type == "pricing.Heartbeat" and args.show_heartbeats:
            print heartbeat_to_string(msg)
        elif msg_type == "pricing.Price":
            
            now = datetime.now()
            time_hash = str(now)
            time_hash = time_hash[17:19]
            timeD = now - start

            df5 = pd.DataFrame({'Time':[now]})
            #df4 = pd.DataFrame({'Bid': [bid_string(msg)]})
            #df5 = pd.DataFrame({'Ask': [ask_string(msg)]})
            df6 = pd.DataFrame({'Mid':[float(mid_string(msg))]})
            df7 = pd.concat([df5, df6], axis=1, join='inner')
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
            minuteData['10 High Close'] = minuteData['Close'][-10:-1].max()
            minuteData['10 Low Close'] = minuteData['Close'][-10:-1].min()
            minuteData['HL'] = minuteData['High']-minuteData['Low']
            minuteData['HC'] = minuteData['High']-minuteData['Close']
            minuteData['CL'] = minuteData['Close']-minuteData['Low']
            minuteData['True Range'] = minuteData[['HL','HC','CL']].max(axis=1).round(5)
            minuteData['N'] = minuteData.rolling('1min', 1)['True Range'].mean().round(5)
            minuteData['$Volatility'] = minuteData['N']*minuteData['Close']*100
            minuteData['Account'] = .01*100000
            minuteData['Lot Size'] = minuteData['Account']/minuteData['$Volatility']
            minuteData['Lot Size'] = minuteData['Lot Size'].round(0)

            minuteData = minuteData[['Open','High','Low','Close',
                        '10 High Close','10 Low Close','True Range',
                        'N','$Volatility','Lot Size']]
            print minuteData, '\n\n', "Rows in minuteData: ", minuteData.shape[0]
            print "Rows in df: ", df.shape[0]
            
            if minuteData.shape[0] > 60:
                minuteData.dropna()
                gc.collect()

            if df.shape[0] > 200:
                df.dropna()
                gc.collect()

            time_seconds = str(timeD)[5:7]
            time_ms = str(timeD)[8:]
            timeD = float(time_seconds + '.' + time_ms)
            
            if minuteData.shape[0] > 1:
                #Test to place otders
                if minuteData['High'][-1] > minuteData['10 High Close'][-1]:
                    long_open = minuteData['High']
                
                    lot_size = minuteData['Lot Size']
                    response = api.order.market(
                        account_id,
                        # Harcode for testing purposes only, stream.py will have the variable for instrument
                        instrument=",".join(args.instrument),
                        units=lot_size)
                    
                    print('**********************************')
                    print("Response: {} ({})".format(response.status, response.reason))
                    print("")
                    print_order_create_response_transactions(response)
                    print('**********************************')
                
                elif minuteData['Low'][-1] < minuteData['10 Low Close'][-1]:
                    short_open = minuteData['Low']
                    
                    lot_size = minuteData['Lot Size']* -1
                    response = api.order.market(
                        account_id,
                        # Harcode for testing purposes only, stream.py will have the variable for instrument
                        instrument=",".join(args.instrument),
                        units=lot_size)
                    
                    print('**********************************')
                    print("Response: {} ({})".format(response.status, response.reason))
                    print("")
                    print_order_create_response_transactions(response)
                    print('**********************************')

                else:
                    print(response.reason)

            """
            csvWriter.writerow([currency_string(msg), time_string(msg), bid_string(msg), ask_string(msg)])
            csvWriter2.writerow([currency_string(msg), time_string(msg), openCol2, highCol2, lowCol2, closeCol2])
            svWriter2.writerow([currency_string(msg), time_string(msg)])
            ends = datetime.strptime(time_value(msg), '%Y-%m-%d %H:%M:%S')
            diff = relativedelta(time_string_data['Time'], ends)
            """

    #csvFile.close()
    #csvFile2.close()

if __name__ == "__main__":
    main()
