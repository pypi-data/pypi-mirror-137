from qttp.tools.date_interval import DateInterval
from qttp.tools.date import HunDate
from qttp.tools.time_span import time_span
from qttp.tools.log import setup_custom_logger

from datetime import datetime, timedelta
import pandas as pd
import requests
import time
import os

from tqdm import tqdm

import json

pd.set_option('mode.chained_assignment',  None) # turn off the warning

logger = setup_custom_logger("Candles")

hun_date = HunDate()

class Candles:
    def download_1h(self, start, end, log=True):
        down_start = hun_date.date_minus_day(start, 5)
        down_end   = hun_date.date_plus_day(end, 10)
        day = 0

        while True:
            try:
                count_limit = self.__count_limit()
                dates = DateInterval(down_start, down_end, count_limit)[0]
                start_dates = dates[0] ; end_dates = dates[1]

                candles_df = pd.DataFrame()
                for start_d, end_d in zip(start_dates, end_dates):
                    time.sleep(0.5)

                    df = self.candles_1h(start_d, end_d)
                    candles_df = pd.concat([candles_df, df])
                    if log:
                        log_text = (
                            f"Getting {self.exchange} Candles, "
                            f"{start_d} ~ {end_d} Done"
                        )
                        logger.info(log_text)

                candles_df = candles_df.astype(float)
                return candles_df

            except KeyboardInterrupt:
                break

            except UnboundLocalError:
                day = day + 5
                down_start = hun_date.date_plus_day(start, day)
                if log:
                    logger.info(f'{down_start} Checking.....')

            except KeyError:
                day = day + 5
                down_start = hun_date.date_plus_day(start, day)
                if log:
                    logger.info(f'{down_start} Checking.....')



        # while True:
        #     try:
        #         dates = DateInterval(down_start, down_end, count_limit)[0]
        #         start_dates = dates[0] ; end_dates = dates[1]
        #
        #         file_name = self.__save_file_name(self.exchange,
        #                                           start, end, option='1hour')
        #
        #         if save:
        #             try:
        #                 result_df = pd.read_csv(file_name, index_col=0,
        #                                         parse_dates=True)
        #
        #             except FileNotFoundError:
        #                 try:
        #                     new_df = pd.DataFrame()
        #                     for start_d, end_d in zip(start_dates, end_dates):
        #                         time.sleep(0.5)
        #
        #                         df = self.candles_1h(start_d, end_d)
        #                         new_df = pd.concat([new_df, df])
        #                         if log:
        #                             log_text = (
        #                                 f"Getting {self.exchange} Candles, "
        #                                 f"{start_d} ~ {end_d} Done"
        #                             )
        #                             logger.info(log_text)
        #
        #
        #                     new_df.to_csv(file_name, index=True)
        #                     result_df = time_span(new_df, span=span, base=base)
        #
        #                 except KeyboardInterrupt:
        #                     break
        #
        #                 except :
        #                     pass
        #
        #             result_df = time_span(result_df, span=span, base=base)
        #             result_df = result_df.astype(float)
        #
        #             result_df = result_df[start:end]
        #             return result_df
        #
        #         else:
        #             try:
        #                 new_df = pd.DataFrame()
        #                 for start_d, end_d in zip(start_dates, end_dates):
        #                     time.sleep(0.5)
        #
        #                     df = self.candles_1h(start_d, end_d)
        #                     new_df = pd.concat([new_df, df])
        #                     if log:
        #                         log_text = (
        #                             f"Getting {self.exchange} Candles, "
        #                             f"{start_d} ~ {end_d} Done"
        #                         )
        #                         logger.info(log_text)
        #
        #                 result_df = time_span(new_df, span=span, base=base)
        #                 result_df = result_df.astype(float)
        #
        #                 result_df = result_df[start:end]
        #                 return result_df
        #
        #             except KeyboardInterrupt:
        #                 break
        #
        #             except :
        #                 pass
        #
        #         time.sleep(1)
        #
        #     except KeyboardInterrupt:
        #         break
        #
        #     except UnboundLocalError:
        #         if log:
        #             day = day + 5
        #             down_start = hun_date.date_plus_day(start, day)
        #             print(f'{down_start} Checking.....')


    def candles_1h(self, start=None, end=None):
        url, path, params = self.__url_path_params("60", start, end, '1h')
        page_json = requests.get(url + path, params=params).json()
        df = self.__dataframe_convert(page_json)
        df = self.preprocessing(df)
        return df

    def candles_24h(self):
        url, path, params = self.__url_path_params("1D")
        page_json = requests.get(url + path, params=params).json()
        df = self.__dataframe_convert(page_json)
        df = self.preprocessing(df)
        return df

    def candles_15m(self):
        url, path, params = self.__url_path_params("15")
        page_json = requests.get(url + path, params=params).json()
        df = self.__dataframe_convert(page_json)
        df = self.preprocessing(df)
        return df

    def __count_limit(self):
        if self.exchange == "upbit" or self.exchange == "bybit":
            return 200

        if self.exchange == "deribit":
            return 10000

        if self.exchange == "binance":
            return 1000

    def __dataframe_convert(self, page_json):
        if self.exchange == "upbit":
            return pd.DataFrame(page_json)

        if self.exchange == "bybit" or self.exchange == "deribit":
            return pd.DataFrame(page_json['result'])

        if self.exchange == 'binance':
            return pd.DataFrame(page_json)

    def __url_path_params(self, unit, start=None, end=None, option=None):
        # upbit
        if self.exchange == "upbit":
            url = "https://api.upbit.com"

            if unit == "1D":
                path = "/v1/candles/days"
            else:
                path = "/v1/candles/minutes/" + unit

            params = {
                "market" : self.market,
                "count" : 200,
            }

            if start:
                params['to'] = start

        # deribit
        if self.exchange == "deribit":
             url = "https://www.deribit.com"
             path = "/api/v2/public/get_tradingview_chart_data"
             params = {
                 "instrument_name" : self.market,
                 "resolution" : unit
             }

             if not start:
                 start_timestamp = hun_date.now_millisecond(50)
                 end_timestamp = hun_date.now_millisecond()
                 params["start_timestamp"] = start_timestamp
                 params["end_timestamp"] = end_timestamp

             if start:
                 params["start_timestamp"] = hun_date.millisecond(start)
                 params["end_timestamp"] = hun_date.millisecond(end)

        # bybit
        if self.exchange == "bybit":
             url = "https://api.bybit.com"
             path = "/v2/public/kline/list"

             if unit == "1D":
                 unit = "D"

             params = {
                 "symbol" : self.market,
                 "interval" : unit,
             }

             if not start:
                 bybit_date = hun_date.today_minus_day(199)
                 params['from'] = hun_date.seconds(bybit_date)

             if option == "1h":
                 bybit_date = hun_date.minus_hour(199)
                 params['from'] = hun_date.seconds(bybit_date)

             if start:
                params['from'] = hun_date.seconds(start)

        # binance
        if self.exchange == "binance":
             url = "https://api.binance.com"
             path = "/api/v3/klines"

             if unit == "1D":
                 unit = "1d"

             if unit == '60':
                 unit = '1h'

             params = {
                 "symbol" : self.market,
                 "interval" : unit,
             }

             if start:
                 params["startTime"] = hun_date.millisecond(start)
                 params["limit"] = 1000


        return url, path, params

    def __time_converter(self):
        pass

    def __save_file_name(self, exchange, start, end,
                         span=None, base=None, option=None):
        exchange = exchange
        market   = self.market
        start    = start
        end      = end
        span     = span
        base     = base
        path = 'candles/'

        if not os.path.isdir(path):
            os.mkdir(path)

        if option == "1hour":
            file_name = f'{exchange}_{market}_{start}_{end}_1hour.csv'
        else:
            file_name = f'{exchange}_{market}_{start}_{end}_{span}_{base}.csv'

        return path + file_name

class UpbitCandle(Candles):
    def __init__(self, market):
        self.exchange = "upbit"
        self.market = market
        self.preprocessing = self.__preprocessing

    def __preprocessing(self, df):
        columns = [
            'candle_date_time_kst', 'opening_price',
            'high_price', 'low_price',
            'trade_price', 'candle_acc_trade_volume'
        ]
        df = df[columns]
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume' ]
        df = df.sort_values(by='date')
        df.index = df['date']
        df.drop('date', axis=1, inplace=True)
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        return df

class BybitCandle(Candles):
    def __init__(self, market):
        self.exchange = "bybit"
        self.market = market
        self.preprocessing = self.__preprocessing

    def __preprocessing(self, df):
        df['open_time'] = pd.to_datetime(df['open_time'], unit='s')
        df['open_time'] = df['open_time'] + timedelta(hours=9)
        df.rename(columns={"open_time": "date"}, inplace=True)
        df.index = df['date']
        df = df[['open', 'high', 'low', 'close', 'volume']]
        df = df.astype(float)
        return df

class DeribitCandle(Candles):
    def __init__(self, market):
        self.exchange = "deribit"
        self.market = market
        self.preprocessing = self.__preprocessing

    def __preprocessing(self, df):
        df['ticks'] = pd.to_datetime(df['ticks'], unit='ms') + timedelta(hours=9)
        df.drop("volume", axis=1, inplace=True)
        df.rename(columns={"ticks": "date", "cost" : "volume"}, inplace=True)
        df.index = df['date']
        df = df[['open', 'high', 'low', 'close', 'volume']]
        df = df.astype(float)
        return df

class BinanceCandle(Candles):
    def __init__(self, market):
        self.exchange = "binance"
        self.market = market
        self.preprocessing = self.__preprocessing

    def __preprocessing(self, df):
        columns = {
            0 : 'date', 1 : 'open', 2 : 'high',
            3 : 'low', 4 : 'close', 5 : 'volume'
        }
        df.rename(columns=columns, inplace=True)
        df['date'] = pd.to_datetime(df['date'], unit='ms') + timedelta(hours=9)
        df.index = df['date']
        df['open'] = df['open'].astype(float, 0)
        df['high'] = df['high'].astype(float, 0)
        df['low'] = df['low'].astype(float, 0)
        df['close'] = df['close'].astype(float, 0)
        df['volume'] = df['volume'].astype(float, 0)
        df = df[['open', 'high', 'low', 'close', 'volume']]
        return df

class FearGreedIndex:
    def __init__(self, url):
        if url == 'alternative':
            self.url = 'https://api.alternative.me'
            self.path = '/fng/'

    def request_data(self):
        params = {
            "limit": 4000,
            "format": 'json',
            "date_format" : 'kr'
        }
        response = requests.get(self.url + self.path, params=params).json()
        df = pd.DataFrame(response['data'])

        return self.__preprocessing(df)

    def __preprocessing(self, df):
        df.index = pd.to_datetime(df['timestamp'])
        df.index.name = 'date'
        df.drop(['timestamp', 'time_until_update'], axis=1, inplace=True)
        df['value'] = df['value'].astype(int)
        df.index = df.index + timedelta(hours=9)
        return df
