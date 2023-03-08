
import argparse
from entities.Stock import Stock
from Services.MoneyControlService import MoneyControlService
from Services.TrendlyneService import TrendlyneService
from Services.NseIndiaService import NseIndiaService
from Services.InvestingService import InvestingService
from Services.Factory import Factory
from Services.iModelServiceInterface import iModelServiceInterface
from Services.WorkflowService import WorkflowService
from helper.util import finance_model


if __name__=="__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("--update_stock", dest='update', type=bool, help='Flag to run stock updater', default=False)
    parser.add_argument("--format_stock", dest='formatter', type=bool, help='Flag to format csv file to json', default=False)
    args = parser.parse_args()
    if args.update:
        workflow = WorkflowService()
        workflow.updater_workflow()
    if args.formatter:
        workflow = WorkflowService()
        workflow.format_to_json()


    # stock_obj = Stock("TRIDENT", MoneyControlService(), TrendlyneService(), NseIndiaService(), InvestingService())
    # stock_obj.financial_ratios = stock_obj.stock_name
    # stock_obj.balance_sheet = stock_obj.stock_name
    # stock_obj.cashflow_statement = stock_obj.stock_name
    # stock_obj.income_statement = stock_obj.stock_name
    # stock_obj.dividend_history = stock_obj.stock_name
    # stock_obj.historical_data = stock_obj.stock_name
    # #instance of modelService
    # factory_instance = Factory()
    # model_service = factory_instance.create_model(stock_obj)
    #
    # print(model_service.calculate_cod(stock_obj))










