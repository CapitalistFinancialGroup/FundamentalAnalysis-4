#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 20:56:03 2021

@author: subora
"""

import requests 

def extract_stock_data(tickerName):
    
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