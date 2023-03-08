# Functionality Description

### Author : Sudeshna Bora

---

#### Submodule : FinancialDetails

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

#### Submodule: DividendDetails

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
The rows of dividend for same year is added. Missing years are added with 0 dividend.
Finally, ```Ex-Date``` is made into row index. 

---

#### Submodule : DividendModel

This ```submodule``` gives the functionality required for ```Gordon Dividend Model```.

<b>calculate_roe</b>

This functionality calculates the ```cost of equity``` based on dividend model.
The most important prerequisite is the dividend should be continous (all the years present in the dividend history needs to have non zero dividend amount).
Conservative growth rate are taken for growth of dividend (though both arithmetic and geometric growth rate are calculated).

```diff

- Note

We should make the check for cost of equity to be more flexible. Instead of every year having a dividend amount, we should check if the last 5 years have 
continous dividend history

```

---

#### Submodule : wacc

This submodule gives the functionalities required to implement ```weighted average cost of capital```.

<b>calculate_cod</b>

It calculates the cost of debt of the stock.
It takes the balance sheet and the income statement to compute the cost of stock in percentage.

</b>marginal_tax_rate</b>

It calculates the tax rate paid by the company based on its income statement.
In place of this we can use a default tax rate of ```30%``` as well.

<b>calculate_roe</b>

This can be considered the caller function for the [dividend]() based implementation and the [capm](https://github.com/SudeshnaBora/FundamentalAnalysis/blob/master/Codes/python/stockLib/stockLibraries/CAPMModel.py) based implementation.
It takes the dividend history and the current share price and gives the roe based on if the company has a continuous dividend or not. 
If it has a continous dividend , it computes the roe based on that otherwise it will compute based on the ```capm``` model.

```diff

- Note

We need to refactor this code to give a choice of whether the user wants dividend model of roe or capm model of roe.

```

<b>calculate_wacc_dividend</b>

This functionality calculates the ```weighted average cost of capital``` based on the ```gordon dividend model```.
It calculates the wacc using both default tax rate (30%) and the calculated marginal tax rate. 

```diff

- Note

It future (once CAPM is done) we will make this the caller function that will either call DividendModel or CAPM model to calculate the wacc.

```

---

#### Submodule : CAPM

This submodule contains the functionalities required to calculate intrinsic value using the ```capital asset pricing model```.

---

#### Submodule : Workflow service 

This is an updater which runs with the field ```--update```. 
It depends on ```source_file``` configuration. So we need to update it. 

<b>Steps to update ```source_file```:</b>

1. Down the excel file from [here](https://www.nseindia.com/regulations/listing-compliance/nse-market-capitalisation-all-companies).
<br><b>TODO:</b> Automate it as well.


