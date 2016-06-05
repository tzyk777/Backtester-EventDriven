import logging
from datetime import datetime as dt

from backtester.event import OrderEvent


def entry_point():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('backtester-{:%Y%m%d-%H%M%S}.log'.format(dt.now()))
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s.%(msecs)03d;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.info('Started')
    OrderEvent('APPL', 'Buy', 123, 'Long').print_order()

if __name__ == '__main__':
    entry_point()