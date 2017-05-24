#!/usr/bin/env python

import argparse
import pandas as pd
import common.config
import common.args
from view import CandlePrinter
from datetime import datetime

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

    date_format = "%Y-%m-%d %H:%M:%S"

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

    account_id = args.config.active_account

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

    price = "mid"

    if args.mid:
        kwargs["price"] = "M" + kwargs.get("price", "")
        price = "mid"

    if args.bid:
        kwargs["price"] = "B" + kwargs.get("price", "")
        price = "bid"

    if args.ask:
        kwargs["price"] = "A" + kwargs.get("price", "")
        price = "ask"

    #
    # Fetch the candles
    #
    response = api.instrument.candles(args.instrument, **kwargs)

    if response.status != 200:
        print(response)
        print(response.body)
        return

    print("Instrument: {}".format(response.get("instrument", 200)))
    print("Granularity: {}".format(response.get("granularity", 200)))

    printer = CandlePrinter()

    candles = response.get("candles", 200)
    
    df = pd.DataFrame([])
    df_out = pd.DataFrame([])
    
    for candle in response.get("candles", 200):

        df1 = pd.DataFrame({'Time':[printer.print_time(candle)]})
        df2 = pd.DataFrame({'Open':[float(printer.print_open(candle))]})
        df3 = pd.DataFrame({'High':[float(printer.print_high(candle))]})
        df4 = pd.DataFrame({'Low':[float(printer.print_low(candle))]})
        df5 = pd.DataFrame({'Close':[float(printer.print_close(candle))]})
        
        df_out = pd.concat([df1, df2, df3, df4, df5], axis=1, join='inner')
        df = df.append(df_out)
        
        df['20-High'] = df['Close'].rolling(20, min_periods=20).max()
        df['20-Low'] = df['Close'].rolling(20, min_periods=20).min()
        df['HL'] = df['High']-df['Low']
        df['HC'] = df['High']-df['Close']
        df['CL'] = df['Close']-df['Low']
        df['True Range'] = df[['HL','HC','CL']].max(axis=1)
        df['N'] = df['True Range'].rolling(20,20).mean().round(5)
        df['$Volatility'] = df['N']*df['Close']*100
        df['Account'] = .01*100000
        df['Lot Size'] = df['Account']/df['$Volatility']
        df['Lot Size'] = df['Lot Size'].round(0)
        
        
    #df = df.dropna()
    df = df[['Time','Open','High','Low','Close','20-High','20-Low','True Range','N', '$Volatility', 'Lot Size']]
    print df

if __name__ == "__main__":
    main()

