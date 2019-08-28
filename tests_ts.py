from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock
from unittest.mock import patch
from decimal import Decimal

from trading_strategy import TradingStrategy
from market_data import MarketDataInterface


class TestStrategy(TestCase):

    def test_stochastic(self):
        ts = TradingStrategy('btcusd')
        with patch.object(MarketDataInterface, 'get_all_ticker') as mock_all:
            mock_all.return_value = [(1, 'btcusd', '2019-07-16 16:42:15', 10500.89, 10609.275723, 10707.89),
                                     (25, 'btcusd', '2019-07-16 16:48:22', 10452.74, 10628.107875, 10707.33),
                                     (20, 'btcusd', '2019-07-16 16:48:10', 10452.73, 10626.9608919, 10707.38)]
            with patch.object(MarketDataInterface, 'get_ticker_data') as mock_last:
                mock_last.return_value = (25, 'btcusd', '2019-07-16 16:48:22', 10452.74, 10628.107875, 10707.33)
                self.assertAlmostEqual(Decimal(0.02076412), ts.calc_stochastic(3))

                mock_all.return_value = ([(42, 'btcusd', '2019-07-16 16:50:06', 10435.63, 10636.8643143, 10707),
                                          (70, 'btcusd', '2019-07-18 10:11:15', 9849.44, 15728.3243624, 9611.85)])
                mock_last.return_value = (70, 'btcusd', '2019-07-18 10:11:15', 9849.44, 15728.3243624, 9611.85)
                self.assertEqual(Decimal(0), ts.calc_stochastic(2))

    def test_stochastic_indicator(self):
        ts = TradingStrategy('btcusd')
        with patch.object(TradingStrategy, 'calc_stochastic'):
            MagicMock.return_value = Decimal(100)
            self.assertAlmostEqual(Decimal(-0.1), ts.stochastic_indicator(10))

            MagicMock.return_value = Decimal(0)
            self.assertAlmostEqual(Decimal(0.1), ts.stochastic_indicator(15))

            MagicMock.return_value = Decimal(60)
            self.assertEqual(Decimal(0), ts.stochastic_indicator(5))

            MagicMock.return_value = Decimal(82)
            self.assertAlmostEqual(Decimal(-0.01), ts.stochastic_indicator(100))

            MagicMock.return_value = Decimal(16)
            self.assertAlmostEqual(Decimal(0.02), ts.stochastic_indicator(2))


if __name__ == '__main__':
    main()
