"""
=================
Trendlyne Service
=================

This module contains the api that utilises Trendlyne website

"""
import pandas as pd
from helper.util import resolve_config_value
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import numpy as np

class TrendlyneService:
    """
    Class containing the services provided by Trendlyne

    Functions
    =========
    get_dividend_history : Fetches the cumulative dividend history of the stock
    """

    def __init__(self):
        self.__config_details = resolve_config_value(['trendlyne'])

    def __get_stock_information(self,ticker_name: str)-> tuple:
        """
        Fetches important information regarding the stock which will be used by other trendlyne api
        Parameters
        ----------
        ticker_name (str) : The ticker name of the stock

        Returns
        -------
        k, stock_name , company_name (tuple) : A tuple containing stock identifer, stock name and the company identifier

        """


        base_url = self.__config_details['stock_details']['full_url']
        url = base_url + ticker_name

        # fetch data
        payload = {}
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'Cookie': 'csrftoken=V28uVslOGrPwMMqa9hJ6bREB0gvAgVLW',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response_body = response.json()

        object_body = {}

        assert len(response_body) != 0

        for entity in response_body:
            if entity['id'] == ticker_name:
                object_body = entity

        return object_body['k'], object_body['id'], object_body['nexturl'].split('/')[-2]


    def get_dividend_history(self,ticker_name: str) -> pd.DataFrame:
        """
        Fetches the dividend history of the stock
        Parameters
        ----------
        ticker_name (str) : The NSE ticker name of the stock

        Returns
        -------
        final_df (pd.DataFrame) : The formatted dataframe containing the dividend history

        """

        k, stock_name, company_name = self.__get_stock_information(ticker_name)
        dividend_url = self.__config_details['dividend']['full_url'] + stock_name + "/" + str(k) + "/" + company_name + "/"

        req = Request(dividend_url,headers={'User-Agent': 'XYZ/3.0'})
        url = urlopen(req).read()
        soup = BeautifulSoup(url,'lxml')
        table = soup.find('table', attrs={'class':'table'})
        df = pd.read_html(str(table))[0]

        #format the df
        # The dataframe is like this :-
        # Ex-Date  Dividend Amount Dividend Type    Record Date
        # 0  Feb. 11, 2021              2.5       INTERIM  Feb. 12, 2021

        # Step 1 : Remove last two columns as unnencessary
        df = df.drop(['Dividend Type', 'Record Date'], axis=1)

        # Step 2 : Convert 'Ex-Date' contents into only Year
        df['Ex-Date'] = df['Ex-Date'].str.split(',').str[-1].str.strip()

        # Step 3 : Convert the 'Ex-Date' to year
        df['Ex-Date'] = pd.to_datetime(df['Ex-Date'], format='%Y').dt.year

        # Now we will group similar years and add their Dividend Amount and keep
        # make index as false as it will otherwise remove the column and make the
        # groups into indices
        df = df.groupby('Ex-Date', as_index=False).sum('Dividend Amount')

        # filling up missing years with 0.0
        final_df = df.set_index('Ex-Date')
        final_df = final_df.sort_index()
        final_df = final_df.reindex(np.arange(df['Ex-Date'].min(), df['Ex-Date'].max() + 1))
        final_df = final_df.fillna(0.0)

        return final_df
