#!/usr/bin/env python

import pandas as pd
from datetime import datetime

class CandlePrinter(object):
    def __init__(self):
        self.width = {
            'time' : 8,
            'type' : 8,
            'price' : 8,
            'volume' : 8,
        }
        # setattr(self.width, "time", 19)
        self.time_width = 8


    def print_header(self):
        
        print("{:<{width[time]}} {:<{width[type]}} {:<{width[price]}} {:<{width[price]}} {:<{width[price]}} {:<{width[price]}} {:<{width[volume]}}".format(
            "Time",
            "Type",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            width=self.width
        ))

        print("{} {} {} {} {} {} {}".format(
            "=" * self.width['time'],
            "=" * self.width['type'],
            "=" * self.width['price'],
            "=" * self.width['price'],
            "=" * self.width['price'],
            "=" * self.width['price'],
            "=" * self.width['volume']
        ))

        volume = ""
        time = ""
    
    def print_columns(self):
        
        return (
            "Time",
            "Open",
            "High",
            "Low",
            "Close",
        )

    def print_candle(self, candle):
        try:
            time = str(datetime.strptime(candle.time,"%Y-%m-%dT%H:%M:%S.000000000Z"))
        except:
            time = candle.time.split(".")[0]

        volume = candle.volume

        for price in ["mid", "bid", "ask"]:
            c = getattr(candle, price, None)

            if c is None:
                continue
            
            print("{:>{width[time]}} {:>{width[type]}} {:>{width[price]}} {:>{width[price]}} {:>{width[price]}} {:>{width[price]}} {:>{width[volume]}}".format(
                time,
                price,
                c.o,
                c.h,
                c.l,
                c.c,
                volume,
                width=self.width
            ))
            
            volume = ""
            time = ""

    def print_time(self, candle):
        try:
            time = str(datetime.strptime(candle.time,"%Y-%m-%dT%H:%M:%S.000000000Z").time())
        except:
            time = candle.time.split(".")[0]

        volume = candle.volume

        for price in ["mid", "bid", "ask"]:
            c = getattr(candle, price, None)

            if c is None:
                continue
            
            return "{:>{width[time]}}".format(
                time,
                width=self.width
            )
            
            volume = ""
            time = ""

    def print_open(self, candle):
        for price in ["mid", "bid", "ask"]:
            c = getattr(candle, price, None)

            if c is None:
                continue
            
            return "{:>{width[price]}}".format(
                c.o,
                width=self.width
            )
            
            volume = ""
            time = ""

    def print_high(self, candle):
        for price in ["mid", "bid", "ask"]:
            c = getattr(candle, price, None)

            if c is None:
                continue
            
            return "{:>{width[price]}}".format(
                c.h,
                width=self.width
            )
            
            volume = ""
            time = ""

    def print_low(self, candle):
        for price in ["mid", "bid", "ask"]:
            c = getattr(candle, price, None)

            if c is None:
                continue
            
            return "{:>{width[price]}}".format(
                c.l,
                width=self.width
            )
            
            volume = ""
            time = ""

    def print_close(self, candle):
        for price in ["mid", "bid", "ask"]:
            c = getattr(candle, price, None)

            if c is None:
                continue
            
            return "{:>{width[price]}}".format(
                c.c,
                width=self.width
            )
            
            volume = ""
            time = ""
