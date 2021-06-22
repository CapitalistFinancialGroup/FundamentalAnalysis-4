"""
======================
Money Control Services
======================

This file contains the functions provided by money control
"""


from helper.util import resolve_config_value
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

class MoneyControlService:
    """
    Class containing the services provided by money control

    Functions
    =========
    get_stock_price : Fetches the stock price of the company
    get_outstanding_shares : Fetches the number of publically traded shares of the company

    """

    def __init__(self):
        self.__config_details = resolve_config_value(['moneycontrol'])

    def __get_basic_stock_information(self,ticker_name):
        """
        Get important company details which will be used by the service
        Parameters
        ----------
        ticker_name (str):

         The ticker id of the company

        Returns
        -------
        stock_abbreviation , stock_name, stock_sector (tuple) :

        Contains the relevant stock abbreviation, stock name (as used in the website) and the
        sector in which the company belongs
        """
        base_url_prefix = self.__config_details['stock_details']['prefix']
        base_url_suffix = self.__config_details['stock_details']['postfix']
        url = base_url_prefix + ticker_name + base_url_suffix

        # fetch data
        response = requests.get(url)
        response_body = response.json()

        assert len(response_body) == 1

        resp = response_body[0]
        link_src = resp['link_src']
        extracted_link = link_src.split('/')

        return extracted_link[-1], extracted_link[-2], extracted_link[-3]

    def get_stock_price(self,ticker_name):
        """
        Fetches the last traded stock price of the company
        Parameters
        ----------
        ticker_name (str) : The ticker id of the company

        Returns
        -------
        share_price (float) : The last traded share price of the company
        """

        stock_abbv , stock_name, stock_sector = self.__get_basic_stock_information(ticker_name)
        url_string = self.__config_details['stock_price']['prefix'] + stock_sector + "/" + stock_name + "/" + stock_abbv
        url = urlopen(url_string).read()
        soup = BeautifulSoup(url,'lxml')
        div_tags = soup.find_all('div', attrs={'class':'inprice1 nsecp'})
        assert len(div_tags) == 1
        return float(div_tags[0].text)

    def get_outstanding_shares(self,ticker_name):
        """
        Fetches the total outstanding shares of the company
        Parameters
        ----------
        ticker_name (str) : The ticker id of the company

        Returns
        -------
        outstanding_shares (numpy.int64) : The total number of outstanding share of the company
        """

        stock_abbv, stock_name, _ = self.__get_basic_stock_information(ticker_name)
        url_string = self.__config_details['financials']['prefix'] + stock_name + self.__config_details['financials']['outstanding_shares']['suffix'] + stock_abbv +"#" + stock_abbv
        url = urlopen(url_string).read()
        soup = BeautifulSoup(url, 'lxml')
        table = soup.find('table', attrs={'class': 'mctable1'})
        df = pd.read_html(str(table))[0]
        #always gets the current outstanding share and as it is in the first row, hence use index 0
        return df.loc[0,('- P A I D U P -','Shares (nos)')]








