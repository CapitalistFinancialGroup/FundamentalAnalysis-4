"""
=======
Factory
=======

Factory class for entire project

"""
from Services.CAPMModelService import CAPMModelService
from Services.DividendModelService import DividendModelService
from Services.iModelServiceInterface import iModelServiceInterface
from Services.InvestingService import InvestingService
from helper.util import finance_model
from entities.Stock import Stock

class Factory:
    """
    Factory class for entire project

    Creators
    ========
    create_model() : Creates an instance of iModelServiceInterface.
    """

    def create_model(self, stock_obj: Stock, type = None) -> iModelServiceInterface:
        """
        Creates concrete implementation of iModelServiceInterface.
        It is based on dividend history of the stock or the type mentioned
        Parameters
        ----------
        stock_obj (entitie.Stock) : Instance of the stock object
        type (str) : The instance type of the interface

        Returns
        -------
        Concrete implementation of iModelServiceInterface

        """

        if not (type==None):
            if type == finance_model.CAPM.name:
                return CAPMModelService(InvestingService())
            if type == finance_model.Dividend.name:
                return DividendModelService()
            else:
                raise ValueError('Finance Model not valid')

        if stock_obj.check_dividend_history():
            return DividendModelService()
        else:
            return CAPMModelService(InvestingService())