from qttp.trading_candles import UpbitCandle

from qttp.tools.data_preprocessing import shift_data
from qttp.tools.indicator import rsi
from qttp.tools.indicator import bollinger_bands

from qttp.tools.filter import filter_spec

import numpy as np
import pandas as pd

from plotly.offline import plot
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

class BackTest:
    def __init__(self, args):
        # exchanges and market attributes
        self.exchange, self.market = args['exchange'], args['market']
        self.start_date, self.end_date = args['start_date'], args['end_date']
        self.span, self.base = args['span'], args['base']

        # target featrues attributes
        self.target_features = args['target_features']
        self.target_features_arguments = args['target_features_arguments']

        # buy conditions attributes
        self.buy_features = args['buy_features']
        self.buy_min = args['buy_min']
        self.buy_max = args['buy_max']

        # sell conditions attributes
        self.sell_features = args['sell_features']
        self.sell_min = args['sell_min']
        self.sell_max = args['sell_max']


    def execute(self, plot=False):
        df = self.__market_data()
        df = self.__indicator_preprocessing(df)
        df = self.__backtest_preprocessing(df)
        df = self.__buy_sell(df)
        print(df)

        if plot:
            self.__plot(df)

    def __market_data(self):
        if self.exchange == 'upbit':
            upbit = UpbitCandle(self.market)
            df = upbit.candles_start_end(self.start_date, self.end_date,
                                         self.span, self.base)

        return df

    def __buy_sell(self, df):
        df = filter_spec(df, self.buy_features, self.buy_min, self.buy_max,
                         'buy_signal', 1)

        df = filter_spec(df, self.sell_features, self.sell_min, self.sell_max,
                         'sell_signal', 1)

        turn = 0
        for i in range(df.shape[0]):
            buy_signal = df.loc[df.index[i], 'buy_signal']
            sell_signal = df.loc[df.index[i], 'sell_signal']
            order = df.index[i]

            if turn == 0 and buy_signal == 1:
                df.loc[order, 'buy'] = 1
                buy_price = df.loc[order, 'close']
                turn = 1

            if turn == 1 and buy_signal == 1:
                df.loc[df.index[i+1], 'buy'] = np.nan

            if turn == 0 and sell_signal == 1:
                df.loc[order, 'sell'] = np.nan

            if turn == 1 and sell_signal == 1:

                for f, min, max in zip(self.sell_features, self.sell_min, self.sell_max):
                    if f == 'close_open_ratio' or f == 'close_high_ratio':
                        if min < sell_price / buy_price:
                            df.loc[order, 'sell'] = 1
                            df.loc[order, 'ror'] = sell_min[0]

                    elif min < df.loc[order, f]:
                        sell_price = df.loc[order, 'close']
                        df.loc[order, 'sell'] = 1
                        df.loc[order, 'ror'] = sell_price / buy_price
                turn = 0

        return df


    def __backtest_preprocessing(self, df):
        df = shift_data(df, self.target_features, 2, 'before')
        return df



    def __indicator_preprocessing(self, df):
        indicator_arguments = self.target_features_arguments
        for f in self.target_features:
            if f == 'rsi':
                source = indicator_arguments['rsi_source']
                length = indicator_arguments['rsi_length']
                df = rsi(df, source, length)

            if f == 'bollinger_bands':
                source = indicator_arguments['bollinger_bands_source']
                length = indicator_arguments['bollinger_bands_length']
                standard = indicator_arguments['bollinger_bands_std']
                df = bollinger_bands(df, source, length, standard)

        return df

    def __trendline_preprocessing(self, df):
        pass

    def __plot(self, df):
        candle = go.Candlestick(
            x = df.index,
            open = df['open'],
            close = df['close'],
            high = df['high'],
            low = df['low'],
            name = 'candlesticks'
        )

        data = [candle]

        # layout = go.Layout(title='abc')
        fig = go.Figure(data=data)
        fig.show()



        app.run_server(debug=True)
