#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which exposes the functionalities to calculate WACC

Created on Sun Apr 25 11:45:17 2021

@author: subora
"""
import stockLibraries.DividendModel as dm
import stockLibraries.CAPMModel as capm
import stockLibraries.DividendDetails as dd
import stockLibraries.FinancialDetails as fd
import pandas as pd

def calculate_cod(balance_df,income_df):
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
        The cost of equity in percentage.

    """
    
    
    # calculate total debt from balance sheet
    current_long_term_debt = float(balance_df.loc['Long Term Borrowings',balance_df.columns[0]])
    current_short_term_debt = float(balance_df.loc['Short Term Borrowings',balance_df.columns[0]])
    
    current_total_debt = current_long_term_debt + current_short_term_debt
    
    #fetch finance cost
    finance_cost = float(income_df.loc['Finance Costs',income_df.columns[0]])
    
    #calculate cost of debt
    cod = finance_cost/current_total_debt*100
    
    return cod


def marginal_tax_rate(income_df):
    """
    Calculates the tax rate of the company. 
    Currently this can be negative.

    Parameters
    ----------
    income_df : @dataframe
        The income statement of the company.

    Returns
    -------
    @float
        The marginal tax rate of the company

    """
    
    # fetch income before tax and total tax
    income_before_tax = float(income_df.loc['Profit/Loss Before Tax',income_df.columns[0]])
    tax_expense = float(income_df.loc['Total Tax Expenses',income_df.columns[0]])
    
    
    #calculate marginal tax rate
    marginal_tax_rate = tax_expense/income_before_tax*100
        
    return marginal_tax_rate

def calculate_roe(dividend_df,current_share_price):
    """
    Calculate return on equity.
    This in turn either calls the dividend model and/or CAPM model

    Parameters
    ----------
    dividend_df : @dataframe
        The dividend dataframe.
    current_share_price : @int
        The current share price of the company.

    Returns
    -------
    @float
        The return on equity for the company.

    """
    
    #preliminary check
    total_years = len(dividend_df)
    dividend_years = len(dividend_df[lambda ddf : ddf['Dividend Amount'] != 0.00])
    
    print("Checking if calculation of roe via Gordon method is possible")
    if total_years == dividend_years:
        print("The company has been giving dividend for the last {} years continously.Going ahead with determining roe by Dividend model".format(total_years)) 
        return dm.calculate_roe(dividend_df,current_share_price)
    else:
        print("The company does not give regular dividend. Has given dividend only {} years out of the last {} years. Hence giving a predetermine rate of 10%".format(dividend_years,total_years))
        # return an predetermined ROE
        # TODO : CALL CAPM.ROE
        return 10
    
def calculate_wacc_dividend(nseId,current_stock_price,outstanding_shares):
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
    
    #fetch the dividend dataframe
    dividend_df = dd.get_dividend_history(nseId)
    
    #calculat the roe
    roe = calculate_roe(dividend_df,current_stock_price)
    
    #fetch the three financial statements
    balancesheet_df,incomestatement_df,_ = fd.get_financial_sheet(nseId)
    
    #calculate cod
    cod = calculate_cod(balancesheet_df,incomestatement_df)
    
    #calculate market value of equity
    market_value_equity = outstanding_shares*current_stock_price
    
    #calulate total debt
    current_long_term_debt = float(balancesheet_df.loc['Long Term Borrowings',balancesheet_df.columns[0]])
    current_short_term_debt = float(balancesheet_df.loc['Short Term Borrowings',balancesheet_df.columns[0]])
    
    current_total_debt = current_long_term_debt + current_short_term_debt
    
    #total debt and equity
    total_debt_equity = current_total_debt + market_value_equity
    
    tax_rate = market_value_equity(incomestatement_df)
    default_tax_rate = 30
    
    #percentage of equity and debt
    percentage_equity = market_value_equity/total_debt_equity*100
    percentage_debt = current_total_debt/total_debt_equity*100
    
    
    print("Calculating wacc with a default tax rate of {}".format(default_tax_rate))
    wacc_default_tax_rate = percentage_equity*roe/10000 + cod/100*percentage_debt/100*(1-default_tax_rate/100)
    
    print("Calculating wacc with the calculated marginal tax rate of {}".format(tax_rate))
    wacc_marginal_tax_rate = percentage_equity*roe/10000 + cod/100*percentage_debt/100*(1-tax_rate/100)
    
    return wacc_default_tax_rate*100,wacc_marginal_tax_rate*100
    
    
    
    
    