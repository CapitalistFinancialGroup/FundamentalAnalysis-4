#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility to fetch stock financial data from money control namely balance sheet, income statement and cash flow statement


Created on Thu Apr  8 20:56:03 2021

@author: subora
"""

import requests 
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen

class FINANCIALS:
    CASHFLOW = "cash-flow"
    BALANCESHEET = "balance-sheet"
    INCOMESTATEMENT = "profit-loss"

def extract_stock_data(tickerName):
    """
    This Function gets the runtime parameters required to get the data from money control

    Parameters
    ----------
    tickerName : str
        The NSE ticker name or BSE id

    Returns
        The placeholders which will be later used to get financial data 
    -------
    str
        The first placeholder.
    str
        The second placeholder.

    """
    
    url = "https://www.moneycontrol.com/mccode/common/autosuggestion_solr.php?classic=true&query="+tickerName+"&type=1&format=json"
    print("Retrieving stock data from money control {}".format(url))
    
    # fetch data
    response = requests.get(url)
    response_body = response.json()
    
    assert len(response_body) == 1
    
    print("Information fetched:")
    print(response_body[0])
    
    link_src = response_body[0]['link_src']
    extracted_link = link_src.split('/')
    
    return extracted_link[-1] , extracted_link[-2]

def get_financial_data(url_string):
    """
    This utility function fetches the financial sheet

    Parameters
    ----------
    url_string : @str
        The url for the given financial sheet

    Returns
    -------
    df : @dataframe
        The raw dataframe

    """
    
    url = urlopen(url_string).read()
    soup = BeautifulSoup(url,'lxml') 
    table = soup.find('table', attrs={'class':'mctable1'}) 
    df = pd.read_html(str(table))[0]
    
    return df

def get_financial_sheet(tickerName):
    """
    Fetch and format the three financial report (balance sheet, income statement and cash flow statement)

    Parameters
    ----------
    tickerName : @str
        The NSE ID of the company.

    Returns
    -------
    balance_df : @dataframe
        The formatted balance sheet dataframe.
    income_df : @dataframe
        The formatted income statement dataframe.
    cashflow_df : @dataframe
        The formatted cashflow dataframe.

    """
    
    #Get the required url details 
    abbv01,abbv02 = extract_stock_data(tickerName)
    
    #get the three financial data in proper representation
    balance_df = format_financial_sheet(abbv01, abbv02, FINANCIALS.BALANCESHEET)
    income_df = format_financial_sheet(abbv01, abbv02, FINANCIALS.INCOMESTATEMENT)
    cashflow_df = format_financial_sheet(abbv01,abbv02,FINANCIALS.CASHFLOW)
    
    return balance_df,income_df,cashflow_df


def format_financial_sheet(placeholder01,placeholder02,sheet_type):
    """
    This function fetches the required financial sheet and formats it into an acceptable representation

    Parameters
    ----------
    placeholder01 : @str
        The first placeholder to be used in the financial sheet query
    placeholder02 : @str
        The second placeholder to be used in the financial sheet query.
    sheet_type : @FINANCIALS
        The financial sheet type. 
        Currently , it can be only FINANCIALS.CASHFLOW, FINANCIALS.BALANCESHEET and FINANCIALS.INCOMESTATEMENT

    Returns
    -------
    sheet_df : @dataframe
        This is the formatted dataframe 

    """
    
    
    sheet_url = "https://www.moneycontrol.com/financials/"+placeholder02+"/consolidated-"+sheet_type+"VI/"+placeholder01+"#"+placeholder01
    
    print("The url being used to fetch the financial data {}".format(sheet_url))
    sheet_df = get_financial_data(sheet_url)
    
    #remote the last column
    sheet_df = sheet_df.iloc[:, :-1]
    
    #make the first column an index
    sheet_df = sheet_df.set_index(0)
    
    #make the first row as header of the data frame
    new_header = sheet_df.iloc[0]
    sheet_df = sheet_df[1:]
    sheet_df.columns = new_header
    
    #get the list of indices 
    idx = sheet_df.index
    
    #drop the first row 
    sheet_df.drop(index=idx[0], inplace=True)
    
    return sheet_df



