#!/usr/bin/env python

import pandas as pd
from datetime import datetime

def print_comp_columns(df):
        
    return (
        "20 Period High",
        "20 Period Low",
        "True Range",
        "N",
        "$Volatility",
        "Units"
    )

def print_twenty_high(df):
    for i, row in df:
        df.itertuples()
        return (i, row)
