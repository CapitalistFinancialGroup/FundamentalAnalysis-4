#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 11:49:09 2021

@author: subora
"""
import pandas as pd
from entities.Stock import Stock
from InvestingService import InvestingService

class CAPMModelService(iModelServiceInterface):

    def __init__(self, investing_service: InvestingService):
        self.__investing_services = investing_service

    def calculate_cod(self, stock_obj: Stock)->float:
        """
        Calculate the required return on debt by capital asset pricing
        method
        Parameters
        ----------
        bdf : dataframe
            The balance sheet.
        idf : dataframe
            The income statement.
        Returns
        -------
        rate_of_debt : TYPE
            DESCRIPTION.
        """

        idf = stock_obj.income_statement

        average_total_debt = self.calculate_average_debt(stock_obj)

        # interest paid current year
        interest_paid = float(idf.loc['Finance Costs', 'Mar 20'])

        rate_of_debt = interest_paid / average_total_debt * 100

        return rate_of_debt

    def calculate_average_debt(self, stock_obj) -> float:

        bdf = stock_obj.balance_sheet

        # fetch debt current and previous years
        current_total_debt = float(bdf.loc['Long Term Borrowings', 'Mar 20']) + float(
            bdf.loc['Short Term Borrowings', 'Mar 20'])
        previous_total_debt = float(bdf.loc['Long Term Borrowings', 'Mar 19']) + float(
            bdf.loc['Short Term Borrowings', 'Mar 19'])

        return (current_total_debt + previous_total_debt) / 2



    def calculate_wacc(self, stock_obj: Stock):
        # get the balance sheet and income statement
        bdf = stock_obj.balance_sheet
        idf = stock_obj.income_statement

        # calculate cost of debt
        cod = self.calculate_cod(stock_obj)
        total_debt = self.calculate_average_debt(stock_obj)

        # calculate marginal tax rate
        mar_tax_rate = stock_obj.calculate_marginal_tax_rate()

        # calculate market value
        market_value = stock_obj.stock_price * stock_obj.outstanding_shares

        roe = self.calculate_roe()

        # calculating both the weights
        weight_equity = market_value / (market_value + total_debt) * 100
        weight_debt = total_debt / (market_value + total_debt) * 100

        assert weight_debt + weight_equity == 100

        wacc = weight_equity / 100 * roe / 100 + weight_debt / 100 * (1 - mar_tax_rate / 100) * cod / 100

        return wacc * 100


    def calculate_roe(self):

        risk_free_rate = self.__investing_services.risk_free_return()
        beta_value = stock_obj.calculate_beta()
        _, erm = stock_obj.calculate_expected_return()

        return risk_free_rate + beta_value * (erm + risk_free_rate)




