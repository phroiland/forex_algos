from subprocess import call

#call(["python", "candles.py", "EUR/USD", "--granularity", "M1", "--from-time", "2017-05-17 21:00:00", "--to-time", "2017-05-19 21:00:00"])

call(["python", "candles.py", "EUR/USD", "--granularity", "M1"])
