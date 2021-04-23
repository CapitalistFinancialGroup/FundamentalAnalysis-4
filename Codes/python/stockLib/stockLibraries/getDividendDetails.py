#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 22:02:58 2021

@author: subora
"""

import requests 
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, Request
import numpy as np

def __extract_stock_data(nse_ticker):
    """
    This fetches the important url parameter to get dividend history

    Parameters
    ----------
    nse_ticker : str
        The NSE Ticker id

    Returns
    -------
    k
        Internal stock id of the website
    id
        NSE ID of the stock.
    company_name
        The full name of the company.

    """

    url = "https://trendlyne.com/member/api/ac_snames/stock/?term="+nse_ticker
    
    print("Retrieving stock data from trendlyne {}".format(url))
    
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
        if entity['id'] == nse_ticker:
            object_body = entity
            
    
    
    return object_body['k'],object_body['id'],object_body['nexturl'].split('/')[-2]


def get_dividend_history(nse_ticker):
    """
    Gives a formatted dataframe of the dividend history of the stock.
    It fills up missing years with 0.0

    Parameters
    ----------
    nse_ticker : str
        The NSE ID for the stock whose dividend we need to find.

    Returns
    -------
    formatted_df : @dataframe
        formateed dataframe with the years as index.

    """
    
    k,value,company_name = __extract_stock_data(nse_ticker)
    
    dividend_url = "https://trendlyne.com/equity/Dividend/"+value+"/"+ str(k) + "/"+ company_name + "/"
    
    req = Request(dividend_url,headers={'User-Agent': 'XYZ/3.0'})
    url = urlopen(req).read()
    soup = BeautifulSoup(url,'lxml') 
    table = soup.find('table', attrs={'class':'table'}) 
    df = pd.read_html(str(table))[0]
    
    return df
    
    #format the dataframe
    formatted_df = __format_dividend_table(df)
    
    return formatted_df

def __format_dividend_table(df):
    """
    Formats the fetched data table.

    Parameters
    ----------
    df : @dataframe
        The unformatted datatable fetched from the website.

    Returns
    -------
    final_df : @dataframe
        The final dataframe

    """
    # The dataframe is like this :-
    #Ex-Date  Dividend Amount Dividend Type    Record Date
    #0  Feb. 11, 2021              2.5       INTERIM  Feb. 12, 2021
  
    # Step 1 : Remove last two columns as unnencessary
    df = df.drop(['Dividend Type','Record Date'],axis=1)
    
    # Step 2 : Convert 'Ex-Date' contents into only Year
    df['Ex-Date'] = df['Ex-Date'].str.split(',').str[-1].str.strip()

    # Step 3 : Convert the 'Ex-Date' to year
    df['Ex-Date'] = pd.to_datetime(df['Ex-Date'], format='%Y').dt.year

    # Now we will group similar years and add their Dividend Amount and keep 
    # make index as false as it will otherwise remove the column and make the 
    #groups into indices
    df = df.groupby('Ex-Date',as_index=False).sum('Dividend Amount')
    
    # filling up missing years with 0.0
    final_df = df.set_index('Ex-Date')
    final_df = final_df.sort_index()
    final_df = final_df.reindex(np.arange(df['Ex-Date'].min(),df['Ex-Date'].max()+1))
    final_df = final_df.fillna(0.0)
    
    return final_df
