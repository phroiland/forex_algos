#!/usr/bin/env python
import math

class CandlePrinter(object):
    def __init__(self):
        """
        self.width = {
            'time' : 19,
            'type' : 4,
            'price' : 8,
            'volume' : 6,
        }
        # setattr(self.width, "time", 19)
        self.time_width = 19
        """
    def print_header(self):
        """
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
        """
    def print_candle(self, candle):
        """
        try:
            time = str(
                datetime.strptime(
                    candle.time,
                    "%Y-%m-%dT%H:%M:%S.000000000Z"
                )
            )
        except:
            time = candle.time.split(".")[0]
        """
        time = candle.time
        
        for price in ["mid","bid", "ask"]:
            c = getattr(candle, price, None)

            if c is None: continue
                
            return "({}) {}/{}".format(
                time,
                c.o,
                c.c
            )
    
    def mid_string(self, candle):
        for price in ["mid","bid", "ask"]:
            c = getattr(candle, price, None)

            if c is None: continue
        
            mid = ((c.o + c.c)/2)
            if math.isnan(float(mid)) != True:
                return "{}".format(mid)
            else: continue
        
    def time_value(self, candle):
        return "{} {}".format(
            candle.time[0:10],
            candle.time[11:19]
        )

    def time_string(self, candle):
        return "{}".format(
            candle.time[11:19]
        )   
    
    def date_string(self, candle):
        return "{}".format(
            candle.time[0:10]
        )

    
        
        
