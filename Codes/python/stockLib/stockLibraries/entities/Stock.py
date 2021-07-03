"""
==============
Entity : Stock
==============

Encapsulation of the stock entity with relevant details
"""
from Services.MoneyControlService import MoneyControlService
from Services.TrendlyneService import TrendlyneService
from Services.NseIndiaService import NseIndiaService
from Services.InvestingService import InvestingService
from helper.util import resolve_config_value
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
    calculate_beta : Calculates the beta value of the stock
    calculate_marginal_tax_rate : Calculates the marginal tax rate of the stock or gives the default 30% if lower
    calculate_expected_return : Calculates the expected return of the stock

    """

    def __init__(self,ticker_name: str, money_control_service: MoneyControlService, trendlyne_service: TrendlyneService,
                 nse_service: NseIndiaService, investing_service: InvestingService):
        # dependency injection
        # won't give any setter or getter as I don't want it to be accessible from an instance
        self.__money_control_services = money_control_service
        self.__trendlyne_services = trendlyne_service
        self.__nse_services = nse_service
        self.__investing_service = investing_service

        # other attributes
        self.__stock_name = self.stock_name = ticker_name
        self.__stock_price = self.stock_price = ticker_name
        self.__outstanding_shares = self.outstanding_shares = ticker_name
        self.__financial_ratios = self.financial_ratios = ticker_name
        self.__balance_sheet = self.balance_sheet = ticker_name , "balance_sheet"
        self.__cashflow_statement = self.cashflow_statement = ticker_name, "cash_flow_statement"
        self.__income_statement = self.income_statement = ticker_name, "income_statement"
        self.__dividend_history = self.dividend_history = ticker_name
        self.__historical_data = self.historical_data = ticker_name, datetime.datetime.now(), datetime.datetime.now() - relativedelta(years=1)


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

    @property
    def historical_data(self):
        return self.__historical_data

    @historical_data.setter
    def historical_data(self,values):
        ticker_name = values[0]
        end_time = values[1]
        start_time = values[2]
        self.__historical_data = self.__nse_services.get_historical_prices(ticker_name, end_time, start_time)



    def check_dividend_history(self)-> bool:
        """
        Sanity check of the dividend history of the company
        1. Checks dividend is paid every year (no discontinuity).
        2. Checks the last dividend paid is this year or atmost last year.

        Returns
        -------
        Boolean flag : True if the dividend history passes sanity, else false

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


    def calculate_beta(self)->float:
        """
        Calculates the beta value of the stock based on 1 year historical data against nifty 50
        Returns
        -------
        beta value (float) : The beta value of the stock

        """

        current_time = datetime.datetime.now()
        previous_time = current_time - relativedelta(years=1)

        # get nifty df
        nifty50_df = self.__investing_service.fetch_price_data_nifty50(current_time, previous_time)

        # fetch data of nse id
        stock_df = self.historical_data

        # add percentage change on both
        nifty50_df['Percentage Change'] = nifty50_df['Price'].pct_change() * 100
        stock_df['Percentage Change'] = stock_df['ltp '].pct_change() * 100

        # calculate covariance and variance
        cov_data = nifty50_df['Percentage Change'].cov(stock_df['Percentage Change'])

        var_data = stock_df['Percentage Change'].var()

        beta_value = cov_data / var_data

        return beta_value



    def calculate_expected_return(self)->tuple:
        """
        Calculates the expected return percentage of the stock and the market (Nifty 50)

        Returns
        -------
        ( expected_return_stock (float) , expected_return_market (float) ) :
        The expected return are in percentage form
        """

        current_time = datetime.datetime.now()
        previous_time = current_time - relativedelta(years=1)

        nifty50_df = self.__investing_service.fetch_price_data_nifty50(current_time, previous_time)
        stock_df = self.historical_data

        # add percentage change on both
        nifty50_df['Percentage Change'] = nifty50_df['Price'].pct_change()
        stock_df['Percentage Change'] = stock_df['ltp '].pct_change()

        # calculate expected return daily
        avg_price_change_stock = stock_df['Percentage Change'].mean()
        avg_price_change_nifty50 = nifty50_df['Percentage Change'].mean()

        # calculate yearly expected return
        yearly_expected_return_stock = ((1 + avg_price_change_stock) ** 365) - 1
        yearly_expected_return_market = ((1 + avg_price_change_nifty50) ** 365) - 1

        return yearly_expected_return_stock * 100, yearly_expected_return_market * 100


    def calculate_marginal_tax_rate(self)->float:
        """
        Calculates the marginal tax rate of the company or gives a default 30% if lower than 30%
        Returns
        -------
        marginal_tax_rate (float) :
        The tax rate is in percentage
        """

        income_df = self.income_statement

        income_before_tax = float(income_df.loc['Profit/Loss Before Tax', income_df.columns[0]])
        tax_expense = float(income_df.loc['Total Tax Expenses', income_df.columns[0]])

        # calculate marginal tax rate
        marginal_tax_rate = tax_expense / income_before_tax * 100
        default_marginal_tax_rate = resolve_config_value(['default', 'marginal_tax_rate'])
        marginal_tax_rate = marginal_tax_rate if marginal_tax_rate > default_marginal_tax_rate else default_marginal_tax_rate
        return marginal_tax_rate






