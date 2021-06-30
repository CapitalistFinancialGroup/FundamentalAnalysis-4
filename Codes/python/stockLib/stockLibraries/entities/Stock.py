"""
==============
Enttty : Stock
==============

Encapsulation of the stock entity with relevant details
"""
from Services.MoneyControlService import MoneyControlService

class Stock:
    """
    Stock Entity

    Attributes
    ==========
    stock_name (str): The ticker id of the stock
    stock_price (float): The last traded price of the stock
    outstanding_shares (numpy.int64) : The number of publically traded shares of the company

    """

    def __init__(self,ticker_name: str, money_control_service: MoneyControlService):
        # dependency injection
        # won't give any setter or getter as I don't want it to be accessible from an instance
        self.__money_control_services = money_control_service

        # other attributes
        self.__stock_name = self.stock_name = ticker_name
        self.__stock_price = self.stock_price = ticker_name
        self.__outstanding_shares = self.outstanding_shares = ticker_name
        self.__financial_ratios = self.financial_ratios = ticker_name
        self.__balance_sheet = self.balance_sheet = ticker_name , "balance_sheet"
        self.__cashflow_statement = self.cashflow_statement = ticker_name, "cash_flow_statement"
        self.__income_statement = self.income_statement = ticker_name, "income_statement"


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

