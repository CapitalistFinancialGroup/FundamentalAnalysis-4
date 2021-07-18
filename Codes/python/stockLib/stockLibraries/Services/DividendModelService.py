#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility class for various dividend model functionalities

Created on Sat Apr 24 13:03:33 2021

@author: subora
"""
import pandas as pd
from entities.Stock import Stock
import logging
from helper.util import resolve_config_value
from Services.iModelServiceInterface import iModelServiceInterface

class DividendModelService(iModelServiceInterface):

    def calculate_roe(self,stock_obj : Stock) -> float :
        """
        Calculates the minimum return on equity for the given stock

        Parameters
        ----------
        stock_obj (entities.Stock) : Contains all relevant information of the stock

        Returns
        -------
        (float) : The expected return on equity

        """

        dividend_df = stock_obj.dividend_history
        current_share_price = stock_obj.stock_price

        #usually the cod by Dividend Gordon method should be possible (as resolved by factory) - incase it is not
        if not stock_obj.check_dividend_history():
            logging.info("Returning default cost of equity as the stock failed dividend check")
            return float(resolve_config_value(['default','rate_of_equity']))

        # for the remaining part we will remove the initial years if the Dividend Amount is 0
        start_index = dividend_df['Dividend Amount'].__ne__(0).idxmax()
        dividend_df = dividend_df.loc[start_index:,:]
        # substracting 1 as the first year of dividend payout is not calculated for geometric growth rate
        total_years = len(dividend_df) -1
        # calculate percentage change of dividend and add it as an additional
        # column in the dataframe
        dividend_df['Percentage Change'] = dividend_df['Dividend Amount'].pct_change()
        # This does not give us in % but only as Delta/original

        # calculate the arithmetic growth rate of dividend
        # for this we need to ignore the first column which is NaN
        ap_growth = dividend_df['Percentage Change'].mean() * 100

        # calculate the geometric growth rate of dividend
        # Formula : {df['Dividend Amount'][-1]/df['Dividend Amount'][0]}^{1/total_years}
        gp_growth = ((dividend_df.loc[dividend_df.index[-1], 'Dividend Amount'] / dividend_df.loc[
            dividend_df.index[0], 'Dividend Amount']) ** (1 / total_years)) * 100

        # Select the more conservative of the growth
        if ap_growth <= gp_growth:
            growth_rate = ap_growth
        else:
            growth_rate = gp_growth

        logging.info("Have selected the growth rate for dividends to be {}".format(growth_rate))
        # Project for the next 5 years.
        last_year = dividend_df.index[-1]
        year_of_concern = last_year + 1

        for i in range(5):
            projected_amount = dividend_df.loc[last_year, 'Dividend Amount'] * (1 + growth_rate / 100)
            logging.info("Projected dividend for {} is {}".format(last_year, projected_amount))
            last_year = last_year + 1
            new_row = pd.Series({'Dividend Amount': projected_amount}, name=last_year)
            dividend_df = dividend_df.append(new_row)

            # calculate cost of equity
        logging.info(
            "Calculating the cost of equity with dividend amount: {}, current share price: {} and a conservative growth rate of {}".format(
                dividend_df.loc[year_of_concern, 'Dividend Amount'], current_share_price, growth_rate))
        roe = (dividend_df.loc[year_of_concern, 'Dividend Amount'] / current_share_price) * 100 + growth_rate
        return roe

    def calculate_cod(self,stock_obj: Stock)->float:
        """
        Calculate the cost of debt

        Parameters
        ----------
        balance_df : @dataframe
            The balance sheet of the company.
        income_df : @dataframe
            The income statement of the company.

        Returns
        -------
        cod : float
            The cost of debt in percentage.

        """

        balance_df = stock_obj.balance_sheet
        income_df = stock_obj.income_statement

        # calculate total debt from balance sheet
        current_long_term_debt = float(balance_df.loc['Long Term Borrowings', balance_df.columns[0]])
        current_short_term_debt = float(balance_df.loc['Short Term Borrowings', balance_df.columns[0]])

        current_total_debt = current_long_term_debt + current_short_term_debt

        # fetch finance cost
        finance_cost = float(income_df.loc['Finance Costs', income_df.columns[0]])

        # calculate cost of debt
        cod = finance_cost / current_total_debt * 100

        return cod

    def calculate_wacc(self, stock_obj: Stock)->float:
        """
        Calculating WACC with the dividend model.
        However, while calculating the cost of equity we may use CAPM if
        dividend model is not possible

        Parameters
        ----------
        nseId : @str
            The nse id of the stock.
        current_stock_price : @float
            The current stock price of the stock.
        outstanding_shares : @float
            The total number of outstanding shares of the stock (in crores).

        Returns
        -------
        wacc_default_tax_rate : @float
            The wacc with a default tax rate.
        wacc_marginal_tax_rate : @float
            The wacc with a calculated marginal tax rate.

        """

        # fetch the dividend dataframe

        dividend_df = stock_obj.dividend_history
        current_stock_price = stock_obj.stock_price

        # calculat the roe
        roe = calculate_roe(dividend_df, current_stock_price)

        # fetch the required financial statements
        balancesheet_df = stock_obj.balance_sheet
        incomestatement_df = stock_obj.income_statement

        # calculate cod
        cod = calculate_cod(balancesheet_df, incomestatement_df)

        # calculate market value of equity
        market_value_equity = outstanding_shares * current_stock_price

        # calulate total debt
        current_long_term_debt = float(balancesheet_df.loc['Long Term Borrowings', balancesheet_df.columns[0]])
        current_short_term_debt = float(balancesheet_df.loc['Short Term Borrowings', balancesheet_df.columns[0]])

        current_total_debt = current_long_term_debt + current_short_term_debt

        # total debt and equity
        total_debt_equity = current_total_debt + market_value_equity

        tax_rate = marginal_tax_rate(incomestatement_df)
        default_tax_rate = 30

        # percentage of equity and debt
        percentage_equity = market_value_equity / total_debt_equity * 100
        percentage_debt = current_total_debt / total_debt_equity * 100

        logging.info("Calculating wacc with a default tax rate of {}".format(default_tax_rate))
        wacc_default_tax_rate = percentage_equity * roe / 10000 + cod / 100 * percentage_debt / 100 * (
                    1 - default_tax_rate / 100)

        logging.info("Calculating wacc with the calculated marginal tax rate of {}".format(tax_rate))
        wacc_marginal_tax_rate = percentage_equity * roe / 10000 + cod / 100 * percentage_debt / 100 * (
                    1 - tax_rate / 100)

        result_wacc = wacc_marginal_tax_rate if wacc_default_tax_rate > wacc_default_tax_rate else wacc_default_tax_rate

        return result_wacc*100


    

