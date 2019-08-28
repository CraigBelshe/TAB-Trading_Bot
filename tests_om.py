from unittest import TestCase
from unittest import main

from unittest.mock import patch
from freezegun import freeze_time

from order_manager import OrderManager



class UnitTest(TestCase):

    @freeze_time('2019-07-23T08:43:02+00:00')
    @patch('settings.CUSTOMER_ID', 'abcd1234')
    @patch('settings.API_KEY', 'abcdefghijklmnopqrstuvwxyz123456')
    @patch('settings.API_SECRET', '123456abcdefghijklnopqrstuvwxyz')
    def test_get_signature(self):
        om = OrderManager('btcusd')
        self.assertDictEqual(om._OrderManager__get_signature(),
                             {'key': 'abcdefghijklmnopqrstuvwxyz123456',
                              'signature': '7728462B38496C189AFAED03A0C51FAB7D2358FA0FE1995C976FF755E794489D',
                              'nonce': '1563871382'})


if __name__ == '__main__':
    main()
