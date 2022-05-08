import sys
import os
import pandas as pd
from helper.util import resolve_config_value
from entities.Stock import Stock

class WorkflowService:

    def __init__(self):
        self.__config_details = resolve_config_value(['default'])

    def updater_workflow(self) -> None:

        #step 1: Read data from stocks files
        stock_list_df = pd.read_excel(os.getcwd() + self.__config_details['source_file'])
        stock_list_df = stock_list_df[['Symbol','Company Name']]
        target_df = stock_list_df.copy()
        target_df['Current Price'] = None
        target_df['PE'] = None
        target_df['Market Capital'] = None
        target_df['FFMC'] = None
        target_df['Outstanding Shares'] = None
        target_df['Basic Industry'] = None
        target_df['Industry'] = None
        target_df['Macro'] = None
        target_df['Sectoral Index'] = None
        target_df['Sectoral PE'] = None
        target_df['Status'] = None
        for index, row in stock_list_df.iterrows():
            try:
                print(f'Starting with stock: {row.Symbol} which is {index +1}/{len(stock_list_df)} stocks.')
                stock_obj = Stock(row['Symbol'])
                target_df.at[row.name, 'Current Price'] = stock_obj.stock_price
                target_df.at[row.name, 'PE'] = stock_obj.symbol_pe
                target_df.at[row.name, 'Market Capital'] = stock_obj.market_cap
                target_df.at[row.name, 'FFMC'] = stock_obj.ffmc
                target_df.at[row.name, 'Outstanding Shares'] = int(stock_obj.outstanding_shares)
                target_df.at[row.name, 'Basic Industry'] = stock_obj.basic_industry
                target_df.at[row.name, 'Industry'] = stock_obj.industry
                target_df.at[row.name, 'Macro'] = stock_obj.macro
                target_df.at[row.name, 'Sectoral Index'] = stock_obj.sectoral_index
                target_df.at[row.name, 'Sectoral PE'] = stock_obj.sectoral_index_pe
                target_df.at[row.name, 'Status'] = stock_obj.status
                del stock_obj
            except:
                print(f'Encountered error. Checkpoint saving')
                target_df.to_excel(os.getcwd() + self.__config_details['target_path'], index=False)

        # store in target
        target_df.to_excel(os.getcwd() + self.__config_details['target_path'], index= False)

