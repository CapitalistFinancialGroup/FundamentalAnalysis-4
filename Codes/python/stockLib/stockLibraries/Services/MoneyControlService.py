"""
======================
Money Control Services
======================

This file contains the functions provided by money control website.

"""
import numpy
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
    get_financial_report : Fetches the required financial report (among balance sheet, income statement, cash flow
    statement, financial ratios)

    """

    def __init__(self):
        self.__config_details = resolve_config_value(['moneycontrol'])

    def __get_basic_stock_information(self,ticker_name: str) -> tuple:
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

        #usually first entry is the correct
        resp = response_body[0]
        for dic in response_body:
            if str(dic['stock_name']).lower() == ticker_name.lower():
                resp = dic

        link_src = resp['link_src']
        extracted_link = link_src.split('/')

        return extracted_link[-1], extracted_link[-2], extracted_link[-3]

    def get_stock_price(self,ticker_name: str) -> float:
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

    def get_outstanding_shares(self,ticker_name: str) -> numpy.int64:
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
        url_string = self.__config_details['financial_statements']['prefix'] + stock_name + self.__config_details['financial_statements']['outstanding_shares']['suffix'] + stock_abbv +"#" + stock_abbv
        url = urlopen(url_string).read()
        soup = BeautifulSoup(url, 'lxml')
        table = soup.find('table', attrs={'class': 'mctable1'})
        df = pd.read_html(str(table))[0]
        #always gets the current outstanding share and as it is in the first row, hence use index 0
        return df.loc[0,('- P A I D U P -','Shares (nos)')]


    def __get_sheet(self,stock_name: str,stock_abbv: str,sheet_name: str) -> pd.DataFrame:
        """
        Internal function to fetch the given financial report in a proper format
        Parameters
        ----------
        stock_name (str) : The name of the stock
        stock_abbv (str) : Webiste specific abbreviation of the stock
        sheet_name (str) : The report to be fetched and formatted

        Returns
        -------
        final_df (pd.DataFrame) : The formatted financial report

        """

        count = 1
        url_permanent = self.__config_details["financial_statements"]["prefix"] + stock_name + "/" + sheet_name + stock_abbv + "/"
        url_suffix_current = str(count)+ "#" + stock_abbv
        url_string = url_permanent + url_suffix_current
        final_df = pd.DataFrame()

        while True:

            # fetch the current page
            url = urlopen(url_string).read()
            soup = BeautifulSoup(url, 'lxml')

            #end condition - check if nodata class is present
            tags = soup.find_all('div',attrs={'class':'nodata'})
            if not len(tags)  == 0:
                break

            # fetch table and add to dataframe
            table = soup.find('table',attrs={'class':'mctable1'})
            current_df = pd.read_html(str(table))[0]

            #format the dataframe
            #drop last column
            current_df = current_df.drop(columns=current_df.columns[-1])
            #make row 1 as current column
            current_df.columns = current_df.iloc[0]
            #drop first two row
            current_df = current_df.iloc[2:]
            #make first column as index
            current_df = current_df.set_index(current_df.columns[0])

            #concatenate with the final dataframe
            final_df = pd.concat([final_df, current_df], axis= 1)

            # add to count to make new current url
            count +=1
            url_suffix_current = str(count) + "#" + stock_abbv
            url_string = url_permanent + url_suffix_current

        return final_df


    def get_financial_report(self,ticker_name: str,report_type: str) -> pd.DataFrame :
        """
        Fetches a particular financial report.
        Parameters
        ----------
        ticker_name (str) : The ticker id of the stock
        report_type (str) : The financial report to be fetched. It can be 'financial_ratios', 'balance_sheet',
        'cash_flow_statement', 'income_statement'

        Returns
        -------
        report_df (pd.DataFrame) : The desire financial report in DataFrame format.

        """

        stock_abbv, stock_name , _ = self.__get_basic_stock_information(ticker_name)

        report_df = self.__get_sheet(stock_name, stock_abbv, self.__config_details['financial_statements'][report_type])
        return report_df














