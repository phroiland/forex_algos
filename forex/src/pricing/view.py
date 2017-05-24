
import common.view


def print_orders_map(orders_map):
    """
    Print a map of Order Summaries in table format.
    Args:
        orders_map: The map of id->Order to print
    """

    print_orders(
        sorted(
            orders_map.values(),
            key=lambda o: o.id
        )
    )


def print_orders(orders):
    """
    Print a collection or Orders in table format.
    Args:
        orders: The list or Orders to print
    """

    #
    # Mapping from Order type to human-readable name
    #
    order_names = {
        "STOP" : "Stop",
        "LIMIT" : "Limit",
        "MARKET" : "Market",
        "MARKET_IF_TOUCHED" : "Entry",
        "ONE_CANCELS_ALL" : "One Cancels All",
        "TAKE_PROFIT" : "Take Profit",
        "STOP_LOSS" : "Stop Loss",
        "TRAILING_STOP_LOSS" : "Trailing Stop Loss"
    }

    #
    # Print the Orders in a table with their ID, type, state, and summary
    #
    common.view.print_collection(
        "{} Orders".format(len(orders)),
        orders,
        [
            ("ID", lambda o: o.id),
            ("Type", lambda o: order_names.get(o.type, o.type)),
            ("State", lambda o: o.state),
            ("Summary", lambda o: o.summary()),
        ]
    )

    print("")


def print_order_create_response_transactions(response):
    """
    Print out the transactions found in the order create response
    """

    common.view.print_response_entity(
        response, None,
        "Order Create",
        "orderCreateTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Long Order Create",
        "longOrderCreateTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Short Order Create",
        "shortOrderCreateTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Order Fill",
        "orderFillTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Long Order Fill",
        "longOrderFillTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Short Order Fill",
        "shortOrderFillTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Order Cancel",
        "orderCancelTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Long Order Cancel",
        "longOrderCancelTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Short Order Cancel",
        "shortOrderCancelTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Order Reissue",
        "orderReissueTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Order Reject",
        "orderRejectTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Order Reissue Reject",
        "orderReissueRejectTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Replacing Order Cancel", 
        "replacingOrderCancelTransaction"
    )

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