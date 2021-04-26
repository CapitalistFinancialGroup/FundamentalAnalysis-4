# Functionality Description

### Author : Sudeshna Bora

---

#### File : FinancialDetails

This file gives functionality to fetch the three important financial reports of a company based on its nse id. 

The functionalities given are:-

<b>__extract_stock_data</b> 

This gives us the important data required to complete the url to fetch the data. 
As we are using moneycontrol for getting financial reports and sending unique nse ticker id ; hence we are getting only one stock (thus this function 
has a check to see if the retrieved details are for only one stock) 
It is an internal function. 
Though internal it can be called from outside the module as it is not tightly coupled with any other function available.

```diff

- Note 

In future we may need to make code change to add functionality to select the correct stock from a group of stock returned on query. 
Something similar has already been done for getting dividend stock information in DividendDetails submodule.


```

<b>__get_financial_data</b>

This takes the final url and gives us the dataframe in raw format i.e. it just scrapes the url to get the required element , stores it as a 
pandas dataframe and returns it to the caller.
The url contains the type of financial report to be scraped.
It is also an internal function.

<b>get_financial_sheet</b>

This can be considered as the entrance function for this submodule. 
It receives a nse id and gives back all the three financial reports in a well structured dataframe. 
The ```columns``` are the years (with column 0 being the latest year).
The ```indices``` signifies what does this row signify. For instance, the row with the index ```Current Liabilities``` will give us the monetary value of 
the current liabilities.

<b>__format_financial_sheet</b>

Formats the financial sheet fetched into predetermined format.
This is also a internal functionality.

---

#### DividendDetails

This submodule fetches dividend history and format it into proper format.

<b>__extract_stock_data</b>

Extracts the required url information. This is an internal function.
Also, in case of multiple results being fetched, it selects the appropiate stock company.

<b>get_dividend_history</b>

This is the main function of this submodule. 
It takes a nse id as input , fetches relevant stock details and then fetches and formats the dividend history. 

<b>__format_dividend_table</b>

Internal function that formats a given dividend history dataframe.
It drops unnecessary columns ```('Dividend Type','Record Date')``` and converts ```Ex-Date``` into a time series (having only year).
The rows of dividend for same year is added. 
Finally, ```Ex-Date``` is made into row index. 

---



