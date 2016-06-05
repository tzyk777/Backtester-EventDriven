import datetime as dt
import logging
import os
import queue
from abc import ABCMeta, abstractclassmethod
from collections import namedtuple

import pandas as pd

from backtester.event import MarketEvent

logger = logging.getLogger('__main__')


DataBar = namedtuple('DataBar', ['date', 'close', 'volume', 'open', 'high', 'low'])


class DataHandler(object):
    __metaclass__ = ABCMeta

    @abstractclassmethod
    def get_latest_bars(self, symbol, N=1):
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractclassmethod
    def update_bars(self):
        raise NotImplementedError("Should Implement update_bars()")


class HistoricCSVDataHandler(DataHandler):
    def __init__(self, events, csv_dir, symbol_list):
        """
        :param events:
        :param csv_dir:
        :param symbol_list:
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True

        self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        comb_index = None
        for s in self.symbol_list:
            self.symbol_data[s] = pd.io.parsers.read_csv(
                os.path.join(self.csv_dir, '%s.csv' % s),
                header=0,
                index_col=0,
                names=DataBar._fields
            )
            if comb_index is None:
                comb_index = self.symbol_data[s].index
            else:
                comb_index.union(self.symbol_data[s].index)

            self.latest_symbol_data[s] = []

        for s in self.symbol_list:
            self.symbol_data[s] = self.symbol_data[s].reindex(index=comb_index, method='pad').iterrows()

    def _get_new_bar(self, symbol):
        for b in self.symbol_data[symbol]:
            yield DataBar(
                date=dt.datetime.strptime(b[0], '%Y/%m/%d'),
                close=b[1][0],
                volume=b[1][1],
                open=b[1][2],
                high=b[1][3],
                low=b[1][4]
                )

    def get_latest_bars(self, symbol, N=1):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            logger.error("The symbol is not available in the historical data set")
        else:
            return bars_list[-N:]

    def update_bars(self):
        for s in self.symbol_list:
            try:
                bar = next(self._get_new_bar(s))
            except StopIteration:
                logger.error("Reached end of data for symbol {}".format(s))
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
        self.events.put(MarketEvent())


if __name__ == '__main__':
    events = queue.Queue()
    handler = HistoricCSVDataHandler(events, r"D:\programming\backtester\data", ['AAPL'])
    print(handler.symbol_data)
    print(handler.latest_symbol_data)
    handler.update_bars()
    print(handler.latest_symbol_data)
    print(handler.get_latest_bars('AAPL'))

