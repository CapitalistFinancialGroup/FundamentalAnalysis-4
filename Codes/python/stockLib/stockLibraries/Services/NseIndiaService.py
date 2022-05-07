"""
======================
NSE India Web Services
======================

Encapsulation for the services that communicate with nse india
"""

import pandas as pd
from helper.util import resolve_config_value
import datetime
import requests
from io import StringIO
from bs4 import BeautifulSoup

class NseIndiaService:
    """
    Functions
    =========

    get_historical_prices : Get historical prices of a stock for a given time frame
    """

    def __init__(self):
        self.__config_details = resolve_config_value(['nse_india'])

    def get_historical_prices(self, stock_name: str, ct: datetime, pt: datetime)-> pd.DataFrame:
        """
        Fetches the daily historical price for the stock for a given time frame

        Parameters
        ----------
        stock_name : str
            The nse ticker id.
        ct : datetime
            The current date which is the end time of the time frame.
        pt : datetime
            The date from where to get the historical prices.

        Returns
        -------
        df : dataframe
            The dataset contains the date and historical price of the stock.

        """

        # change the timestamp to DD-MM-YYYY format
        ct = ct.strftime("%d-%m-%Y")
        pt = pt.strftime("%d-%m-%Y")

        head = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36 "
        }

        base_url = self.__config_details['base_url']

        session = requests.session()
        session.get(base_url, headers=head)
        session.get(base_url + self.__config_details['stock_details'] + stock_name, headers=head)  # to save cookies
        session.get(base_url + self.__config_details['stock_historical_data'] + stock_name, headers=head)
        url = base_url + self.__config_details['stock_historical_data_download'] + stock_name + "&series=[%22EQ%22]&from=" + pt + "&to=" + ct + "&csv=true"
        webdata = session.get(url=url, headers=head)

        df = pd.read_csv(StringIO(webdata.text[3:]))

        # formatting the dataframe to contain only Date and ltp
        df = df.drop(
            ['series ', 'OPEN ', 'HIGH ', 'LOW ', 'PREV. CLOSE ', 'close ', 'vwap ', '52W H ', '52W L ', 'VOLUME ',
             'VALUE ', 'No of trades '], axis=1)

        # changing Date column to timestamp and putting it in the format of YYYY-mm-dd
        # as we will need to sort it
        df['Date '] = pd.to_datetime(df['Date ']).dt.strftime("%Y-%m-%d")

        # sorting df based on Date column in ascending order
        df = df.sort_values(by=['Date '])

        return df


    def create_cookies(self, cookie: dict, ticker_name: str) -> str:
        """

        Parameters
        ----------
        cookie

        Returns
        -------

        """

        keys = ['nsit','ak_bmsc','nseappid','bm_sv']
        cookies = f'AKA_A2=A;'
        cookies += ' nseQuoteSymbols=[{"symbol":"' +ticker_name +',"identifier":null,"type":"equity"}];'
        for key in keys:
            cookies += f'{key}={cookie[key]};'
        return cookies


    def get_stock_metadata(self, ticker_name: str) -> tuple:
        """

        Parameters
        ----------
        ticker_name

        Returns
        -------

        """

        head = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36 ",
            'authority': 'www.nseindia.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'accept': '/',
            'sec-gpc': '1',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.nseindia.com/get-quotes/equity?symbol='+ticker_name,
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        base_url = self.__config_details['base_url']
        session = requests.session()
        session.get(base_url, headers=head)
        session.get(base_url + self.__config_details['base_stock_details'] + ticker_name, headers=head)
        # to save cookies
        url = base_url + self.__config_details['stock_details'] + ticker_name
        head['cookie'] = self.create_cookies(session.cookies.get_dict(),ticker_name)
        #session.get(url, headers=head)
        response = requests.get(url, headers=head).json()

        industry = response['metadata']['industry']
        sector_pe = response['metadata']['pdSectorPe']
        symbol_pe = response['metadata']['pdSymbolPe']
        sector_industry = response['metadata']['pdSectorInd']
        status = response['securityInfo']['tradingStatus']
        macro = response['industryInfo']['macro']
        #sector = response['industryInfo']['sector']
        basic_industry = response['industryInfo']['basicIndustry']
        outstanding_share = response['securityInfo']['issuedSize']
        stock_price = response['priceInfo']['lastPrice']

        return stock_price, outstanding_share, basic_industry, symbol_pe, sector_pe, sector_industry, macro, industry


