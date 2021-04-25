#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility class for various dividend model functionalities

Created on Sat Apr 24 13:03:33 2021

@author: subora
"""
import pandas as pd 


def calculate_roe(df,current_share_price):
    """
     
    Calculates minimum return on equity/cost of equity as per gordon
    dividend model. 
    
    In case the dividend history of the company is not continous, we will
    give a return of only 10%

    Parameters
    ----------
    df : @dataframe
        A pandas dataframe containing the dividend history.
    current_share_price : @int
        The current share price of the company.

    Returns
    -------
    @int
        The minimum rate of equity/minimum cost of equity for the company.

    """
    
    dividend_df = df
    
    #preliminary check
    total_years = len(dividend_df)
    dividend_years = len(dividend_df[lambda ddf : ddf['Dividend Amount'] != 0.00])
    
    print("Checking if calculation of roe via Gordon method is possible")
    if total_years == dividend_years:
        print("The company has been giving dividend for the last {} years continously.Going ahead with determining roe by Dividend model".format(total_years)) 
    else:
        print("The company does not give regular dividend. Has given dividend only {} years out of the last {} years. Hence giving a predetermine rate of 10%".format(dividend_years,total_years))
        # return an predetermined ROE
        return 10
    
    # calculate percentage change of dividend and add it as an additional 
    # column in the dataframe 
    dividend_df['Percentage Change'] = dividend_df['Dividend Amount'].pct_change()
    # This does not give us in % but only as Delta/original
    
    #calculate the arithmetic growth rate of dividend 
    # for this we need to ignore the first column which is NaN

    ap_growth = dividend_df['Percentage Change'].mean()*100
    
    #calculate the geometric growth rate of dividend
    
    # Formula : {df['Dividend Amount'][-1]/df['Dividend Amount'][0]}^{1/total_years}
    gp_growth = ((dividend_df.loc[dividend_df.index[-1],'Dividend Amount']/dividend_df.loc[dividend_df.index[0],'Dividend Amount'])**(1/total_years))*100
    
    #Select the more conservative of the growth 
    if ap_growth <= gp_growth:
        growth_rate = ap_growth
    else:
        growth_rate = gp_growth
    
    print("Have selected the growth rate for dividends to be {}".format(growth_rate))
    # Project for the next 5 years.
    last_year = dividend_df.index[-1]
    
    for i in range(5):
        projected_amount = dividend_df.loc[last_year,'Dividend Amount']*(1 + growth_rate/100)
        print("Projected dividend for {} is {}".format(last_year,projected_amount))
        last_year = last_year + 1
        new_row = pd.Series({'Dividend Amount': projected_amount},name = last_year)
        dividend_df = dividend_df.append(new_row)        
    
    # calculate cost of equity
    print("Calculating the cost of equity with dividend amount: {}, current share price: {} and a conservative growth rate of {}".format(dividend_df.loc[dividend_df.index[-1],'Dividend Amount'],current_share_price,growth_rate))
    roe = (dividend_df.loc[dividend_df.index[-1],'Dividend Amount']/current_share_price)*100 + growth_rate
    return roe

