from qttp.tools.exception_handlers import exception_handler_01

import ccxt

class Apis:
    def __init__(self, access, secret, market, log=True):
        self.api.apiKey = access
        self.api.secret = secret
        self.market = market
        self.log = log

    @exception_handler_01
    def tickers(self):
        tickers = self.api.fetchTickers()
        return tickers

    @exception_handler_01
    def limit_buy(self, amount, price):
        market = self.__market_name_change()
        buy = self.api.create_order(symbol=market, type="limit",
                                    side="buy", amount=amount, price=price)
        return buy

    @exception_handler_01
    def limit_sell(self, amount, price):
        market = self.__market_name_change()
        sell = self.api.create_order(symbol=market, type="limit",
                                    side="sell", amount=amount, price=price)
        return sell

    @exception_handler_01
    def market_buy(self, amount, price=None):
        market = self.__market_name_change()
        buy = self.api.create_order(symbol=market, type="market",
                                    side="buy", amount=amount, price=price)
        return buy

    @exception_handler_01
    def market_sell(self, amount, price=None):
        market = self.__market_name_change()
        sell = self.api.create_order(symbol=market, type="market",
                                    side="sell", amount=amount, price=price)
        return sell

    @exception_handler_01
    def ask_price(self, num):
        market = self.__market_name_change()
        ask_price = self.api.fetchOrderBook(market)['asks'][num][0]
        return ask_price

    @exception_handler_01
    def bid_price(self, num):
        market = self.__market_name_change()
        return self.api.fetchOrderBook(market)['bids'][num][0]

    @exception_handler_01
    def ask_prices(self):
        market = self.__market_name_change()
        return self.api.fetchOrderBook(market, limit=100)['asks']

    @exception_handler_01
    def bid_prices(self):
        market = self.__market_name_change()
        return self.api.fetchOrderBook(market, limit=100)['bids']

    @exception_handler_01
    def order_list(self):
        return self.api.fetchOpenOrders()

    @exception_handler_01
    def cancel_all(self):
        market = self.__market_name_change()
        self.api.cancel_all_orders(market)
        return "Executed"

    def exchange_name(self):
        return str(self.api)

    def __market_name_change(self):
        if str(self.api) == "Upbit":
            market = self.market[4:] + "/" + self.market[:3]

        elif str(self.api) == "Bybit":
            market = self.market[:3] + "/" + self.market[-3:]

        else:
            market = self.market

        return market

class BybitApi(Apis):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.bybit()
        super().__init__(*args, **kwargs)

        symbol = {"symbol": self.market}
        self.position = self.api.private_get_position_list(symbol)
        self.account = self.api.private_get_wallet_balance()

    @exception_handler_01
    def avg_price(self):
        avg_price = self.position['result']['entry_price']
        return avg_price

    @exception_handler_01
    def size(self):
        size = self.position['result']['size']
        return size

    @exception_handler_01
    def equity(self):
        return self.account['result'][self.market[:3]]['equity']

class DeribitApi(Apis):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.deribit()
        super().__init__(*args, **kwargs)
        instrument_name = {'instrument_name' : self.market,}
        currency = {'currency' : self.market[:3]}
        self.position = self.api.private_get_get_position(instrument_name)
        self.account = self.api.private_get_get_account_summary(currency)

    @exception_handler_01
    def avg_price(self):
        avg_price = self.position['result']['average_price']
        return avg_price

    @exception_handler_01
    def size(self):
        size = self.position['result']['size']
        return size

    @exception_handler_01
    def equity(self):
        return self.account['result']['equity']

class UpbitApi(Apis):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.upbit()
        super().__init__(*args, **kwargs)
        self.__account()

    @exception_handler_01
    def avg_price(self):
        return self.u_avg_price

    @exception_handler_01
    def size(self):
        return self.u_size

    @exception_handler_01
    def equity(self):
        return self.u_equity_total

    @exception_handler_01
    def krw_balance(self):
        return self.krw_bal

    @exception_handler_01
    def krw_locked(self):
        return self.krw_lock

    @exception_handler_01
    def account_info(self):
        return self.account

    @exception_handler_01
    def cancel_all(self):
        order_ids = self.__order_ids()
        for order_id in order_ids:
            self.api.cancel_order(order_id)
        return "Executed"

    @exception_handler_01
    def cancel_order(self, order_id):
        self.api.cancel_order(order_id)

    def __order_ids(self):
        try:
            orders = self.api.fetchOpenOrders()
            order_ids = [order['info']['uuid'] for order in orders]

        except IndexError as e:
            order_ids = []

        return order_ids

    def __account(self):
        account = self.api.private_get_accounts()

        u_equity_total = 0
        u_avg_price = 0
        u_size = 0

        for equity in account:
            if equity['currency'] == 'KRW':
                krw_balance = float(equity['balance'])
                krw_locked = float(equity['locked'])
                u_equity_total = u_equity_total + float(equity['locked'])
                u_equity_total = u_equity_total + float(equity['balance'])
            else:
                avg_buy = float(equity["avg_buy_price"])
                balance = float(equity['balance'])
                locked = float(equity['locked'])
                u_equity_total = u_equity_total + (avg_buy * balance) + (avg_buy * locked)

            if equity['currency'] == self.market[4:]:
                u_avg_price = equity["avg_buy_price"]
                u_size = equity["balance"]

        self.account = account
        self.krw_bal = krw_balance
        self.krw_lock = krw_locked
        self.u_equity_total = float(u_equity_total)
        self.u_avg_price = float(u_avg_price)
        self.u_size = float(u_size)

class CoinoneApi(Apis):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.coinone()
        super().__init__(*args, **kwargs)
        # print(self.api.fetch_balance())
