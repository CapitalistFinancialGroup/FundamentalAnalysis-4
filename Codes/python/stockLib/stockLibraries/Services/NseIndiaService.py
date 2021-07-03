"""
======================
NSE India Web Services
======================

Encapsulation for the services that communicate with nse india
"""

import pandas as pd
from helper.util import resolve_config_value

class NseIndiaService:
    """
    Functions
    =========

    get_historical_prices : Get historical prices of a stock for a given time frame
    """

    def __init__(self):
        self.__config_details = resolve_config_value(['nse_india'])

    def get_historical_prices(self, stock_name: str, ct: datetime, pt: datetime)-> pd.DataFrame:
        """
        Fetches the daily historical price for the stock for a given time frame

        Parameters
        ----------
        stock_name : str
            The nse ticker id.
        ct : datetime
            The current date which is the end time of the time frame.
        pt : datetime
            The date from where to get the historical prices.

        Returns
        -------
        df : dataframe
            The dataset contains the date and historical price of the stock.

        """

        # change the timestamp to DD-MM-YYYY format
        ct = ct.strftime("%d-%m-%Y")
        pt = pt.strftime("%d-%m-%Y")

        head = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36 "
        }

        base_url = self.__config_details['base_url']

        session = requests.session()
        session.get(base_url, headers=head)
        session.get(base_url + self.__config_details['stock_details'] + stock_name, headers=head)  # to save cookies
        session.get(base_url + self.__config_details['stock_historical_data'] + stock_name, headers=head)
        url = base_url + self.__config_details['stock_historical_data_download'] + stock_name + "&series=[%22EQ%22]&from=" + pt + "&to=" + ct + "&csv=true"
        webdata = session.get(url=url, headers=head)

        df = pd.read_csv(StringIO(webdata.text[3:]))

        # formatting the dataframe to contain only Date and ltp
        df = df.drop(
            ['series ', 'OPEN ', 'HIGH ', 'LOW ', 'PREV. CLOSE ', 'close ', 'vwap ', '52W H ', '52W L ', 'VOLUME ',
             'VALUE ', 'No of trades '], axis=1)

        # changing Date column to timestamp and putting it in the format of YYYY-mm-dd
        # as we will need to sort it
        df['Date '] = pd.to_datetime(df['Date ']).dt.strftime("%Y-%m-%d")

        # sorting df based on Date column in ascending order
        df = df.sort_values(by=['Date '])

        return df