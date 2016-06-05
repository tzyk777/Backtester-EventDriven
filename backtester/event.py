import logging
logger = logging.getLogger('__main__')


class Event(object):
    pass


class MarketEvent(Event):
    def __init__(self):
        self.type = 'Market'


class SignalEvent(Event):
    def __init__(self, symbol, datetime, signal_type):
        self.type = 'Signal'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type


class OrderEvent(Event):
    def __init__(self, symbol, order_type, quantity, direction):
        self.type = 'Order'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        logger.info("Order: symbol={symbol}, Type={type}, Quantity={quantity}, Direction={direction}".format(
            symbol=self.symbol,
            type=self.type,
            quantity=self.quantity,
            direction=self.direction
        ))


class FillEvent(Event):
    def __init__(self, timeindex, symbol, exchange, quantity, direction, fill_cost, commission=None):
        """
        :param timeindex:
        :param symbol:
        :param exchange:
        :param quantity:
        :param direction:
        :param fill_cost:
        :param commission:
        :return:
        """
        self.type = 'Fill'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        if commission is None:
            self.commission = self.calculate_ib_commission()
        else:
            self.commission = commission

    def calculate_ib_commission(self):
        if self.quantity <= 500:
            full_cost = max(1.3, 0.013 * self.quantity)
        else:
            full_cost = max(1.3, 0.008 * self.quantity)
        full_cost = min(full_cost, 0.5 / 100.0 * self.quantity * self.fill_cost)
        return full_cost

