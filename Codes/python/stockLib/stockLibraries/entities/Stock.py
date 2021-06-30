"""
==============
Entity : Stock
==============

Encapsulation of the stock entity with relevant details
"""
from Services.MoneyControlService import MoneyControlService
from Services.TrendlyneService import TrendlyneService
import numpy as np
import datetime

class Stock:
    """
    Stock Entity

    Attributes
    ==========
    stock_name (str): The ticker id of the stock
    stock_price (float): The last traded price of the stock
    outstanding_shares (numpy.int64) : The number of publically traded shares of the company

    Functions
    =========
    check_dividend_history : Sanity check of the dividend history of the stock

    """

    def __init__(self,ticker_name: str, money_control_service: MoneyControlService, trendlyne_service: TrendlyneService):
        # dependency injection
        # won't give any setter or getter as I don't want it to be accessible from an instance
        self.__money_control_services = money_control_service
        self.__trendlyne_services = trendlyne_service

        # other attributes
        self.__stock_name = self.stock_name = ticker_name
        self.__stock_price = self.stock_price = ticker_name
        self.__outstanding_shares = self.outstanding_shares = ticker_name
        self.__financial_ratios = self.financial_ratios = ticker_name
        self.__balance_sheet = self.balance_sheet = ticker_name , "balance_sheet"
        self.__cashflow_statement = self.cashflow_statement = ticker_name, "cash_flow_statement"
        self.__income_statement = self.income_statement = ticker_name, "income_statement"
        self.__dividend_history = self.dividend_history = ticker_name


    @property
    def stock_name(self):
        return self.__stock_name

    @stock_name.setter
    def stock_name(self,var):
        self.__stock_name = var

    @property
    def stock_price(self):
        return self.__stock_price

    #TODO : Better way to call setter without variable
    @stock_price.setter
    def stock_price(self,ticker_name):
        self.__stock_price = self.__money_control_services.get_stock_price(ticker_name)

    @property
    def outstanding_shares(self):
        return self.__outstanding_shares

    @outstanding_shares.setter
    def outstanding_shares(self,ticker_name):
        self.__outstanding_shares = self.__money_control_services.get_outstanding_shares(ticker_name)

    @property
    def financial_ratios(self):
        return self.__financial_ratios

    @financial_ratios.setter
    def financial_ratios(self,ticker_name):
        self.__financial_ratios = self.__money_control_services.get_financial_report(ticker_name,"financial_ratios")

    @property
    def balance_sheet(self):
        return self.__balance_sheet

    @balance_sheet.setter
    def balance_sheet(self,values):
        self.__balance_sheet = self.__money_control_services.get_financial_report(values[0],values[1])

    @property
    def cashflow_statement(self):
        return  self.__cashflow_statement

    @cashflow_statement.setter
    def cashflow_statement(self, values):
        self.__cashflow_statement = self.__money_control_services.get_financial_report(values[0],values[1])

    @property
    def income_statement(self):
        return self.__income_statement

    @income_statement.setter
    def income_statement(self, values):
        self.__income_statement = self.__money_control_services.get_financial_report(values[0],values[1])

    @property
    def dividend_history(self):
        return self.__dividend_history

    @dividend_history.setter
    def dividend_history(self,ticker_name):
        self.__dividend_history = self.__trendlyne_services.get_dividend_history(ticker_name)


    def check_dividend_history(self)-> bool:
        """
        Sanity check of the dividend history of the company
        1. Checks dividend is paid every year (no discontinuity).
        2. Checks the last dividend paid is this year or atmost last year.

        Returns
        -------
        Boolean flag : True if the dividend history passes sanity check else false

        """

        dividend_df = self.__dividend_history

        #check if dividend history is not empty , if empty return false
        if len(dividend_df) == 0:
            return False

        # check if dividend history is continous

        # Step 1: Delete all columns with Dividend amount = 0
        dividend_df = dividend_df[dividend_df['Dividend Amount'] != 0]

        # Additional check to see if the latest dividend is this year or last year
        current_year = int(datetime.datetime.now().year)
        # Get start year and end year from index
        start_year = dividend_df.index[0]
        end_year = dividend_df.index[-1]

        # Step 2: Create time range [done in set]
        time_range = set(np.arange(start_year,end_year+1,1))
        dividend_year_range = set(dividend_df.index)

        if ~(current_year == end_year or current_year == end_year - 1):
            print("The dividend history is not latest")
            return False

        # Step 4: Compute missing year
        missing_years = time_range.difference(dividend_year_range)

        return len(missing_years) == 0 and len(time_range) == len(dividend_year_range)


if __name__=="__main__":
    stock_obj = Stock("AXISBANK",MoneyControlService(),TrendlyneService())
    print(stock_obj.check_dividend_history())





