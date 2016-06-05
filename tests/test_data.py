import unittest
from unittest.mock import Mock, patch, call, MagicMock
import queue
import os

from backtester import DataHandler, HistoricCSVDataHandler, DataBar


class TestHistoricCSVDataHandler(unittest.TestCase):
    def setUp(self):
        self.events = queue.Queue()
        self.csv_dir = r"D:\Path\To\File"
        self.symbol_list = ['AAPL']
        with patch('backtester.HistoricCSVDataHandler._open_convert_csv_files') as open:
            self.open = open
            self.handler = HistoricCSVDataHandler(self.events, self.csv_dir, self.symbol_list)

    def test_members_are_set(self):
        handler = self.handler
        self.assertIsInstance(handler, DataHandler)
        self.assertEqual(handler.events, self.events)
        self.assertEqual(handler.csv_dir, self.csv_dir)
        self.assertEqual(handler.symbol_list, self.symbol_list)

        self.assertEqual(handler.symbol_data, {})
        self.assertEqual(handler.latest_symbol_data, {})
        self.assertTrue(handler.continue_backtest)

        self.assertTrue(self.open.called)

    @patch('backtester.data.pd.io.parsers.read_csv')
    def test_open_convert_csv_files(self, read_pd):
        handler = self.handler
        read_pd.return_value = mock_read = MagicMock()
        mock_read.index = 'INDEX'
        handler._open_convert_csv_files()
        calls = [
            call(os.path.join(handler.csv_dir, '{}.csv'.format(self.symbol_list[0])), header=0, index_col=0,
                 names=DataBar._fields),
            call().reindex(index='INDEX', method='pad'),
            call().reindex().iterrows()
        ]
        self.assertIn(calls, read_pd.mock_calls)

        self.assertEqual(handler.latest_symbol_data[handler.symbol_list[0]], [])






