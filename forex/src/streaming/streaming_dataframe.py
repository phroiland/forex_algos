#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 16:06:26 2017

@author: johnfroiland
"""
from datetime import datetime
from view import mid_string

df = pd.DataFrame([])
minuteData = pd.DataFrame([])
open_instrument = pd.DataFrame({'Instrument':[None]})
open_units = pd.DataFrame({'Units':[None]})
open_long = pd.DataFrame({'Long':[None]})
open_short = pd.DataFrame({'Short':[None]})
trade_id = pd.DataFrame({'Trade ID':[0]})
positions = pd.DataFrame([])
positions = pd.concat([open_instrument,open_units,open_long,open_short,
                       trade_id],axis=1, join='outer')


class Traffic(self, data):
    
    
    
    
    def streaming_dataframe():
        now = datetime.now()
        df5 = pd.DataFrame({'Time':[now]})
        df6 = pd.DataFrame({'Mid':[float(mid_string(msg))]})
        df7 = pd.concat([df5,df6], axis=1, join='inner')
        df7 = df7.set_index(['Time'])
        df7.index = pd.to_datetime(df7.index, unit='s')
        df = df.append(df7)
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
            minuteData['Account'] = .01*-100000
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
                sell = abs(minuteData['Lot Size'][-1])
                print sell
                units = sell.astype('str')
                print units
                currency = currency_string(msg)
                positions['Trade ID'] += 1
                tradeid = '@' + positions.iloc[0]['Trade ID'].astype('str')
                trade_response = api.order.market(
                    account_id,
                    tradeid=tradeid,
                    instrument=currency,
                    units=units
                )
                #print trade_response
                positions['Instrument'] = currency_string(msg)
                positions['Units'] = minuteData['Low'][-1]
                positions['Short'] = None
                #print('**********************************')
                #print('STOP')
                #print('**********************************')
                #
                # Process the response
                #
                print("Response: {} ({})".format(
                        trade_response.status,trade_response.reason))
                positions['Trade ID']
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
                positions['Trade ID'] += 1
                tradeid = '@' + positions.iloc[0]['Trade ID'].astype('str')
                trade_response = api.order.market(
                    account_id,
                    tradeid=tradeid,
                    instrument=currency,
                    units=units
                )
                #print trade_response
                positions['Instrument'] = currency_string(msg)
                positions['Units'] = minuteData['Lot Size'][-1]
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
                sell = abs(minuteData['Lot Size'][-1])
                print sell
                units = sell.astype('str')
                print units
                currency = currency_string(msg)
                positions['Trade ID'] += 1
                tradeid = '@' + positions.iloc[0]['Trade ID'].astype('str')
                trade_response = api.order.market(
                    account_id,
                    tradeid=tradeid,
                    instrument=currency,
                    units=units
                )
                #print trade_response
                positions['Instrument'] = currency_string(msg)
                positions['Units'] = minuteData['Lot Size'][-1]
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
                positions['Trade ID'] += 1
                tradeid = '@' + positions.iloc[0]['Trade ID'].astype('str')
                trade_response = api.order.market(
                    account_id,
                    tradeid=tradeid,
                    instrument=currency,
                    units=units
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
                
            positions = positions[['Instrument','Units','Long','Short','Trade ID']]
            print positions
            #with open('Backtest.csv', 'a') as f:
                #positions.to_csv(f, index=False, header=False, sep=',')
                #positions['Stop'] = 0
                
                
if __name__ == "__main__":
    main()
