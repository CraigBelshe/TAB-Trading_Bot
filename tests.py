from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock
from unittest.mock import create_autospec


from order_manager import OrderManager


class UnitTest(TestCase):
    def test_get_signature(self):
        om = OrderManager('btcusd')
        # om.api_key = Mock(return_value='abcdefghijklmnopqrstuvwxyz123456')
        # print(om.api_key, 'hi')
        # om.customer_id = Mock(return_value='abcd1234')
        # om.nonce = Mock(return_value='1563871382')
        om.api_secret = MagicMock(return_value='123456abcdefghijklmnopqrstuvwxyz')
        om.message = MagicMock(
            return_value=(bytes('1563871382abcd1234abcdefghijklmnopqrstuvwxyz123456', encoding='utf8')), autospec=True)
        print(om.message.call_args, 'h')
        result = om.get_signature()
        print(result, 'bye')
        self.assertDictEqual(result, {'key': 'abcdefghijklmnopqrstuvwxyz123456', 'signature': '9DC68A39801E6BD3DFE33BDDE050FA75CE2242FB7C86F51613F9BEC2BF754F55', 'nonce': '1563871382'})

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
