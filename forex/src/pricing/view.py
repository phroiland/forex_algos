def currency_string(price):
	return "{}".format(
		price.instrument
	)

def time_value(price):
	return "{} {}".format(
		price.time[0:10],
		price.time[11:19]
	)

def time_string(price):
	return "{}".format(
		price.time[11:19]
	)

def date_string(price):
	return "{}".format(
		price.time[0:10]
	)

def bid_string(price):
	return "{}".format(
		price.bids[0].price
	)

def ask_string(price):
    return "{}".format(
        price.asks[0].price     
    )

def mid_string(price):
	mid = (price.asks[0].price + price.bids[0].price)/2
	return "{}".format(mid)

def heartbeat_to_string(heartbeat):
    return "HEARTBEAT ({})".format(
        heartbeat.time
    )

def price_to_string(price):
    return "{} ({}) {}/{}".format(
        price.instrument,
        price.time,
        price.bids[0].price,
        price.asks[0].price
    )