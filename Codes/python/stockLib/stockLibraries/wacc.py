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
import datetime
from dateutil.relativedelta import relativedelta
import requests
from bs4 import BeautifulSoup

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
    
    tax_rate = marginal_tax_rate(incomestatement_df)
    default_tax_rate = 30
    
    #percentage of equity and debt
    percentage_equity = market_value_equity/total_debt_equity*100
    percentage_debt = current_total_debt/total_debt_equity*100
    
    
    print("Calculating wacc with a default tax rate of {}".format(default_tax_rate))
    wacc_default_tax_rate = percentage_equity*roe/10000 + cod/100*percentage_debt/100*(1-default_tax_rate/100)
    
    print("Calculating wacc with the calculated marginal tax rate of {}".format(tax_rate))
    wacc_marginal_tax_rate = percentage_equity*roe/10000 + cod/100*percentage_debt/100*(1-tax_rate/100)
    
    return wacc_default_tax_rate*100,wacc_marginal_tax_rate*100


def risk_free_return():
    """
    Calculates the rate of return of a risk free commodity.
    Currently the 1 year daily historical return rate of Indian Government 91 days T bill 
    is considered. 

    Returns
    -------
    risk_free_return_rate : float
        The rate of return of a risk free commodity.

    """
    
    
    #Step 1: Fetch the current dates. 
    
    current_date = datetime.datetime.now() - relativedelta(days=1)
    previous_date = current_date - relativedelta(years=1)
    
    current_date_str = current_date.strftime("%d/%m/%Y")
    previous_date_str = previous_date.strftime("%d/%m/%Y")
    
    #Step 2 : Create the header and data for extracting information
    
    data = {'curr_id': '24003','smlID': '203924','header': 'India 3-Month Bond Yield Historical Data','st_date': previous_date_str,
            'end_date': current_date_str,'interval_sec': 'Daily','sort_col': 'date','sort_ord': 'DESC','action': 'historical_data'
            }
    
    headers = {
    'authority': 'in.investing.com',
    'accept': 'text/plain, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-gpc': '1',
    'origin': 'https://in.investing.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://in.investing.com/rates-bonds/india-3-month-bond-yield-historical-data',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': '__cfduid=d3c2e1fe62f9856cf29821a05e88b54811619441949; _tz_id=c528baa594cfdfaf5e93a86048b5c4f4; PHPSESSID=8h8jqnmeg1f2o5j03vo1nk7llr; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2224003%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A37%3A%22%2Frates-bonds%2Findia-3-month-bond-yield%22%3B%7D%7D%7D%7D; geoC=IN; adBlockerNewUserDomains=1619441951; gtmFired=OK; StickySession=id.6100660358.631in.investing.com; udid=f54e7210e8e3bc9b35a468ba65a8ad14; __cflb=02DiuF9qvuxBvFEb2qB1HcuDLvqD9ieP4QJ9YHcUfbsS4; G_ENABLED_IDPS=google; _fbp=fb.1.1619441955314.16268788; adsFreeSalePopUp=2; comment_notification_202451988=1; adsFreeSalePopUpa41d6b177ab422862f5e64f395319b37=1; r_p_s_n=1; smd=f54e7210e8e3bc9b35a468ba65a8ad14-1619454509; UserReactions=true; ses_id=ZSthIGJtNj4%2BempsN2YyMD5tN2g%2FPTs4Zm43PDA%2Fbng3I2RqYDc%2FeTE%2BbiBjYGZ6YmMyMjQ3YDA8PjJsNjZmN2UzYTRiZjY8PmtqMzdhMmE%2BPjdtPz87bWZlN2cwY24wNzdkZGBvP28xYm42Y2tmaGJwMi40cGBxPG4yYjZ3ZiFlamEgYjI2aj5gamA3MTJlPmo3ZT9tOzhmZzcyMGJudjd8; nyxDorf=ZWRmPDF5ZDo%2FaT02biNjY2IyYjgyK2dnMjBvaQ%3D%3D',
    }
    
    req = requests.post('https://in.investing.com/instruments/HistoricalDataAjax', headers=headers, data=data)
    soup = BeautifulSoup(req.content, "lxml")
    table = soup.find('table', attrs={'id':'curr_table'})
    df = pd.read_html(str(table))[0]
    
    #Step 3 : calculating the rate
    
    print("Fetched data, calculating the rate of risk free return")

    risk_free_return_rate = df['Price'].mean()
    
    return risk_free_return_rate

    
    
    
    
    