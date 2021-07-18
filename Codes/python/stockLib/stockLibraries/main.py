
from entities.Stock import Stock
from Services.MoneyControlService import MoneyControlService
from Services.TrendlyneService import TrendlyneService
from Services.NseIndiaService import NseIndiaService
from Services.InvestingService import InvestingService
from Services.Factory import Factory
from Services.iModelServiceInterface import iModelServiceInterface


if __name__=="__main__":
    stock_obj = Stock("ITC",MoneyControlService(), TrendlyneService(), NseIndiaService(), InvestingService())

    #instance of modelService
    factory_instance = Factory()
    model_service = factory_instance.create_model(stock_obj)

    print(model_service.calculate_roe(stock_obj))










