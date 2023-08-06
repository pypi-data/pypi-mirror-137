from qttp.tools.filter import filter_spec
from qttp.tools.data_preprocessing import shift_data
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import gridspec


import numpy as np

class BackTest_03:
    '''
    This backtest is ror that is designated
    '''
    def __init__(self, args):
        # dataframe date filter
        self.df = args['df']
        self.start_date = args['start_date']
        self.end_date = args['end_date']

        # buy conditions attributes
        self.buy_features = args['buy_features']
        self.buy_min = args['buy_min']
        self.buy_max = args['buy_max']

        # ror information
        self.fee = args['fee']
        self.set_ror = args['set_ror']

    def run(self, chart=False, csv_save=False):
        df = self.__preprocessing(self.df)
        df = self.__designated_ror(df)

        if csv_save:
            df.to_csv('abc.csv')
            df.to_csv('abc.csv')

    def __preprocessing(self, df):

        df = df.loc[self.start_date:self.end_date, :].copy()

        df = filter_spec(df, self.buy_features, self.buy_min, self.buy_max,
                         'buy_signal', 1)

        return df

    def __designated_ror(self, df):
        amount_list = []
        turn = 0
        amount = 0
        scaling_price = 0
        try:
            for i in range(df.shape[0]):
                buy_signal = df.loc[df.index[i], 'buy_signal']
                order = df.index[i]

                if turn == 0 and buy_signal == 1:
                    amount += 1
                    df.loc[order, 'amount'] = amount

                    df.loc[order, 'buy'] = 1
                    avg_price = df.loc[order, 'open']

                    if scaling_price == 0:
                        df.loc[order, 'avg_price'] = avg_price
                        sell_price = avg_price * self.set_ror
                        df.loc[order, 'sell_price'] = sell_price

                    if scaling_price > 0:
                        avg_price = (scaling_price + avg_price) / amount
                        df.loc[order, 'avg_price'] = avg_price
                        sell_price = avg_price * self.set_ror
                        df.loc[order, 'sell_price'] = sell_price

                    turn = 1

                if turn == 1 and buy_signal == 1:
                    df.loc[df.index[i+1], 'buy'] = np.nan

                if turn == 1 and df.loc[order, 'high'] > sell_price:
                    df.loc[order, 'sell'] = 1
                    df.loc[order, 'ror'] = self.set_ror - self.fee
                    turn = 0
                    amount = 0
                    scaling_price = 0

                if turn == 1 and df.loc[order, 'high'] < sell_price:
                    if df.loc[order, 'open'] / avg_price < 1.0:
                        scaling_price = avg_price * amount
                        turn = 0
                    else:
                        turn = 1

                if df.loc[order, 'low'] / avg_price < 0.5 and turn == 1:
                    df.loc[order, 'danger'] = 1
                # print(amount_list)
                amount_list.append(amount)
                print(max(amount_list))
            print(amount_list)



        except:
            pass
        # print(take_day)
        # print(len(take_day))

        return df

class BackTest_04:
    '''
    This backtest is ror that is designated
    '''
    def __init__(self, args):
        # dataframe date filter
        self.df = args['df'].loc[args['start_date']:args['end_date'], :].copy()

        # ror information
        self.fee = args['fee']
        self.set_ror = args['set_ror']

    def run(self, chart=False, csv_save=False):
        df = self.df
        df = self.__designated_ror(df)
        # df.to_csv('abc.csv')
        df = self.__ror_hpr(df)


        if csv_save:
            df.to_csv('abc.csv')

        if chart:
            self.__chart(df)

    def __designated_ror(self, df):
        turn = 0
        day = 0
        try:
            for i in range(df.shape[0]):
                buy_signal = df.loc[df.index[i], 'buy_signal']
                order = df.index[i]

                if turn == 0 and buy_signal == 1:
                    df.loc[order, 'buy'] = 1
                    buy_price = df.loc[order, 'open']
                    sell_price = buy_price * self.set_ror

                    day += 1
                    turn = 1

                if turn == 1 and buy_signal == 1:
                    df.loc[df.index[i+1], 'buy'] = np.nan

                if turn == 1 and df.loc[order, 'high'] < sell_price:
                    day += 1

                if turn == 1 and  df.loc[order, 'high'] > sell_price:
                    df.loc[order, 'sell'] = 1
                    df.loc[order, 'ror'] = self.set_ror - self.fee
                    df.loc[order, 'buy_price'] = buy_price
                    df.loc[order, 'sell_price'] = sell_price
                    df.loc[order, 'day'] = day

                    day = 0
                    turn = 0

        except KeyError as error:
            print(f'KeyError : {error}')

        except IndexError as error:
            print(f'IndexError : {error}')

        return df

    def __ror_hpr(self, df):
        df['ror'].fillna(1, inplace=True)
        df.loc[:, 'hpr'] = df['ror'].cumprod()
        hpr = round(df.iloc[-1, -1], 2)
        trading_count = df.loc[:, 'buy'].sum()
        total_day = df.shape[0]
        trading_ratio = round(df.loc[:, 'buy'].sum() / df.shape[0]* 100, 2)
        trading_day_max = df['day'].max()
        text = (
            f"hpr: {hpr}배, trading_count: {trading_count}개, "
            f"total_day: {total_day}일, trading_ratio: {trading_ratio}%, "
            f"trading_day_max: {trading_day_max}일"
        )
        print(text)

        return df

    def __chart(self, df):
        buy_data_x = df.loc[df['buy'] == 1, 'close'].index
        buy_data_y = df.loc[df['buy'] == 1, 'close'].values

        sell_data_x = df.loc[df['sell'] == 1, 'close'].index
        sell_data_y = df.loc[df['sell'] == 1, 'close'].values

        fig = make_subplots(rows=1, cols=2)

        fig.add_trace(
             px.scatter(df, x=df.index, y="close"),
             row=1, col=1
        )
        # fig = px.line(df, x=df.index, y="close", row=1, col=1)

        # for x, y in zip(buy_data_x, buy_data_y):
        #     fig.add_annotation(x=x, y=y, text="B", showarrow=False,
        #                        yshift=30, bordercolor='blue')
        #
        # for x, y in zip(sell_data_x, sell_data_y):
        #     fig.add_annotation(x=x, y=y, text="S", showarrow=False,
        #                        yshift=30, bordercolor='red')

        fig.add_trace(
             px.scatter(df, x=df.index, y="close"),
              row=1, col=2
        )

        fig.show()
