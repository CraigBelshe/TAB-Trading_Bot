# Order Manager UnitTests are not finished, they will be added later
from unittest import skip
from unittest import TestCase
from unittest import main

# from unittest.mock import MagicMock
from unittest.mock import patch
# from unittest.mock import Mock
from freezegun import freeze_time

from order_manager import OrderManager
# from market_data import MarketDataInterface


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

    # @mock.patch('requests.post', side_effect=mocked_requests_get())
    #  @patch('requests.post')
    @skip("not complete")
    def test_get_balance(self):  # To be created later, currently do not know how to patch requests
        pass
    #     mock_post.return_value = {'btc_available': '0.00083900', 'btc_balance': '0.00284200', 'btc_reserved':
    #     '0.00200300', 'fee': '0.25', 'usd_available': '10.00', 'usd_balance': '10.00', 'usd_reserved': '0.00'}
    #     om = OrderManager('btcusd')
    #     result = om.get_balance()
    #     print(result)
    #
    #     with patch('requests.post') as mock_post:
    #         mock_post.return_value = {'btc_available': '0.00083900', 'btc_balance': '0.00284200', 'btc_reserved':
    #         '0.00200300', 'fee': '0.25', 'usd_available': '10.00', 'usd_balance': '10.00', 'usd_reserved': '0.00'}
    #         om = OrderManager('btcusd')
    #         result = om.get_balance()
    #         print(result)
    #
    #
    #      info = {'btc_available': '0.00083900', 'btc_balance': '0.00284200', 'btc_reserved': '0.00200300', 'fee':
    #      '0.25', 'usd_available': '10.00', 'usd_balance': '10.00', 'usd_reserved': '0.00'}
    #      resp = requests.post("www.someurl.com", data=json.dumps(info), headers={'Content-Type': 'application/json'})
    #      mock_post.assert_called_with("www.someurl.com", data=json.dumps(info),
    #                                       headers={'Content-Type': 'application/json'})
    #     om = OrderManager('btcusd')
    #     result = om.get_balance()
    #     result['balance'].__getitem__.return_value = '0.011'
    #     result['available'].__getitem__.return_value = '2.011'
    #     result['reserved'].__getitem__.return_value = '1.011'
    #     result['usd_available'].__getitem__.return_value = '0.1'
    #
    #
    #     responses.add(responses.g)
    #     mock_post.return_value = Mock(status_code=201, json=lambda: {'btc_available': '0.00083900', 'btc_balance':
    #     '0.00284200', 'btc_reserved': '0.00200300', 'fee': '0.25', 'usd_available': '1.00',
    #     'usd_balance': '1.00', 'usd_reserved': '0.00'})
    #     mockresponse = Mock()
    #     mock_post.json.return_value = mockresponse
    #     mockresponse.text = "{'balance': '0.00284200', 'available': '0.00083900', 'reserved':
    #     '0.00200300', 'usd_available': '10.00'}"
    #
    #
    #
    #     mock_resp = self._mock_response(content={'balance': '0.00284200', 'available':
    #     '0.00083900', 'reserved': '0.00200300',
    #                                         'usd_available': '10.00'})
    #     mock_post.json.return_value = mock_resp
    #     om = OrderManager('btcusd')
    #     result = om.get_balance()
    #     print(result)
    #     self.assertDictEqual(result, {'balance': '0.00284200', 'available': '0.00083900', 'reserved': '0.00200300',
    #                                         'usd_available': '10.00'})
    #
    # @patch('order_manager.requests.get', {'btc_available': '0.00083900', 'btc_balance': '0.00284200',
    # 'btc_reserved': '0.00200300',
    #                                      'fee': '0.25', 'usd_available': '1.00', 'usd_balance': '1.00',
    #                                      'usd_reserved': '0.00'})
    # @mock.patch('requests.post')
    # def test_get_balance(self): # this is not actually working
    #     om = OrderManager('btcusd')
    #     mock_resp = self._mock_response(content={'btc_available': '0.00083900', 'btc_balance': '0.00284200',
    #     'btc_reserved': '0.00200300',
    #                              'fee': 0.25, 'usd_available': '10.00', 'usd_balance': '10.00',
    #                              'usd_reserved': '0.00'})
    #     mock_request.return_value = mock_resp
    #
    #     data = {'btc_available': '0.00083900', 'btc_balance': '0.00284200', 'btc_reserved': '0.00200300',
    #                              'fee': '0.25', 'usd_available': '10.00', 'usd_balance':
    #                              '1.00', 'usd_reserved': '0.00'}
    #     json_data = json.dumps(data)
    #     with patch('order_manager.requests.post') as mocked:
    #         mocked.return_value = json_data
    #
    #             {'btc_available': '0.00083900', 'btc_balance': '0.00284200', 'btc_reserved': '0.00200300',
    #                              'fee': 0.25, 'usd_available': '10.00', 'usd_balance': '1.00', 'usd_reserved': '0.00'}
    #     with patch('requests.get',
    #                return_value={'btc_available': '0.00083900', 'btc_balance': '0.00284200',
    #                'btc_reserved': '0.00200300',
    #                              'fee': 0.25, 'usd_available': '10.00', 'usd_balance': '10.00',
    #                              'usd_reserved': '0.00'}):
    #         result = om.get_balance()
    #         print(result)
    #
    #     self.assertDictEqual(result, {'balance': '0.00284200', 'available': '0.00083900', 'reserved': '0.00200300',
    #                                       'usd_available': '10.00'})

    # @patch("requests.get", {'id': 1, 'datetime': 1563871382, 'type': 0, 'price': 10000, 'amount': 1})
    def test_buy(self):
        pass
        # om = OrderManager('btcusd')
        # print(om.buy(10000, 1))

    def test_sell(self):
        pass

    def test_instant_buy(self):
        pass

    def test_instant_sell(self):
        pass

    def test_cancel_all_orders(self):
        pass

    def test_cancel_order(self):
        pass

    def test_get_order_status(self):
        pass

    def test_get_open_orders(self):
        pass

    def test_get_transactions(self):
        pass

    def test_market_buy(self):
        pass

    def test_market_sell(self):
        pass


if __name__ == '__main__':
    main()
