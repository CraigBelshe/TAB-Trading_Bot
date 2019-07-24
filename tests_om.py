from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import create_autospec
from time import time
from freezegun import freeze_time

from order_manager import OrderManager


class UnitTest(TestCase):
    @freeze_time("2019-07-23T08:43:02+00:00")
    @patch("settings.CUSTOMER_ID", 'abcd1234')
    @patch("settings.API_KEY", 'abcdefghijklmnopqrstuvwxyz123456')
    @patch("settings.API_SECRET", '123456abcdefghijklnopqrstuvwxyz')
    def test_get_signature(self):
        om = OrderManager('btcusd')
        self.assertDictEqual(om.get_signature(), {'key': 'abcdefghijklmnopqrstuvwxyz123456', 'signature': '7728462B38496C189AFAED03A0C51FAB7D2358FA0FE1995C976FF755E794489D', 'nonce': '1563871382'})

    def test_get_balance(self):
        om = OrderManager('btcusd')
        om.account = MagicMock(
            return_value={'btc_available': '0.00083900', 'btc_balance': '0.00284200', 'btc_reserved': '0.00200300',
                          'fee': 0.25, 'usd_available': '1.00', 'usd_balance': '1.00', 'usd_reserved': '0.00'})
        result = om.get_balance()
        self.assertDictEqual(result, {'balance': '0.00284200', 'available': '0.00083900', 'reserved': '0.00200300',
                                      'usd_available': '1.00'})


if __name__ == '__main__':
    main()
