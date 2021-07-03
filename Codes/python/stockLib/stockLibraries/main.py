
from entities.Stock import Stock
from Services.MoneyControlService import MoneyControlService
from Services.TrendlyneService import TrendlyneService

if __name__=="__main__":
    stock_obj = Stock("ITC",MoneyControlService(), TrendlyneService())
    print(stock_obj.stock_price)

