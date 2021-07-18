"""
==============
iModelService
==============

"""
import abc
from entities.Stock import Stock


class iModelServiceInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def calculate_roe(self,stock : Stock)-> float:
        """
        Calculates the return on equity for given stock
        Parameters
        ----------
        stock (entities.Stock) : The stock entity

        Returns
        -------
        The calculated rate of return

        """

        raise NotImplementedError

    @abc.abstractmethod
    def calculate_cod(self,stock : Stock) -> float:
        """
        Calculates the cost of debt for the stock
        Parameters
        ----------
        stock (Stock) : The stock entity

        Returns
        -------
        The calculated cost of debt

        """

        raise NotImplementedError

    @abc.abstractmethod
    def calculate_wacc(self, stock: Stock) -> float:
        """
        Calculates the weighted average cost of capital
        Parameters
        ----------
        stock (Stock) : The stock entity


        Returns
        -------
        The calculated average cost of capital

        """

        raise NotImplementedError



