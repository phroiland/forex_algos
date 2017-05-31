#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 13:30:38 2017

@author: johnfroiland
"""

#!/usr/bin/env python

import pandas as pd
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.max_columns', 0)
import argparse
import common.config
import common.args
from args import OrderArguments
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
    
    
    
    
    
    
    
    #
    # Print out each price as it is receive
    #       
    for msg_type, msg in response.parts():
        if msg_type == "pricing.Heartbeat" and args.show_heartbeats:
                print heartbeat_to_string(msg)
            
        if msg_type == "pricing.Price":
            print(price_to_string(msg))

               
if __name__ == "__main__":
    main()