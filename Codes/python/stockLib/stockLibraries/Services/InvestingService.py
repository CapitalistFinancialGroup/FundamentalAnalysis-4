from helper.util import resolve_config_value

class InvestingService:

    def __init__(self):
        self.__config_details = resolve_config_value('investing')

    def fetch_price_data_nifty50(self, ct: datetime, pt: datetime):
        """
        Fetches the daily historical price for 1 year for NIFTY 50 index

        Parameters
        ----------
        ct : datetime
            The Current date.
        pt : datetime
            The date 1 year previous.

        Returns
        -------
        df : dataframe
            A dataframe containtaing Date and the correspnding price
            .

        """

        # convert to epoch
        current_timestamp = int(ct.timestamp())
        previous_timestamp = int(pt.timestamp())

        headers = {
            'authority': 'in.investing.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-gpc': '1',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': '__cfduid=d3c2e1fe62f9856cf29821a05e88b54811619441949; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2224003%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A37%3A%22%2Frates-bonds%2Findia-3-month-bond-yield%22%3B%7D%7D%7D%7D; adBlockerNewUserDomains=1619441951; udid=f54e7210e8e3bc9b35a468ba65a8ad14; G_ENABLED_IDPS=google; _fbp=fb.1.1619441955314.16268788; r_p_s_n=1; PHPSESSID=ojh953jnvn10jlr2df6l722n98; StickySession=id.22709788039.279in.investing.com; _tz_id=d1084eeb396bb44ef6ef1f44c51b7af5; welcomePopup=1; geoC=IN; nyxDorf=ODk%2BZGYuZDo3YWFqYy41NWIyZjw1LDAwNTdlYw%3D%3D; __cflb=02DiuF9qvuxBvFEb2qB1HcuDLvqD9ieP4VA1bEKif7H4g; ses_id=MX8xcGJtMjphJWlvZzY3NTJhM2wzMWVmZ29nbDs0Z3EwJGZoNWI%2BeGRrbiAwMzYqZGU3MjZiMGM9b2Y4N2RnOzEyMWRiYjJpYTRpYGc3N2EyazNoM2dlNGdgZ2M7aGduMDZmNzViPjNkNG5jMDg2O2R2Nys2cjAhPW9mNjd2ZyAxPjFwYjIybmE%2BaWVnNDc2MjIzOjM9ZWdnN2dkOzlnfzB7; smd=f54e7210e8e3bc9b35a468ba65a8ad14-1620052261',
        }
        params = (
            ('end_date', int(current_timestamp)),
            ('st_date', int(previous_timestamp)),
        )

        response = requests.get(self.__config_details['nifty_50']['full_url'], headers=headers,
                                params=params)

        soup = BeautifulSoup(response.content, "lxml")
        table = soup.find('table', attrs={'class': 'common-table medium js-table'})
        df = pd.read_html(str(table))[0]

        # drop columns and keep only Date and Price
        df = df.drop(['Open', 'High', 'Low', 'Volume', 'Chg%'], axis=1)

        # change the Date to timestamp and change to the format %Y-%m-%d
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime("%Y-%m-%d")

        df = df.sort_values(by=['Date'])

        return df

    def risk_free_return(self):
        """
        Calculates the rate of return of a risk free commodity.
        Currently the 1 year daily historical return rate of Indian Government 91 days T bill
        is considered.

        Returns
        -------
        risk_free_return_rate : float
            The rate of return of a risk free commodity.

        """

        # Step 1: Fetch the current dates.

        current_date = datetime.datetime.now() - relativedelta(days=1)
        previous_date = current_date - relativedelta(years=1)

        current_date_str = current_date.strftime("%d/%m/%Y")
        previous_date_str = previous_date.strftime("%d/%m/%Y")

        # Step 2 : Create the header and data for extracting information

        data = {'curr_id': '24003', 'smlID': '203924', 'header': 'India 3-Month Bond Yield Historical Data',
                'st_date': previous_date_str,
                'end_date': current_date_str, 'interval_sec': 'Daily', 'sort_col': 'date', 'sort_ord': 'DESC',
                'action': 'historical_data'
                }

        headers = {
            'authority': 'in.investing.com',
            'accept': 'text/plain, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-gpc': '1',
            'origin': 'https://in.investing.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://in.investing.com/rates-bonds/india-3-month-bond-yield-historical-data',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': '__cfduid=d3c2e1fe62f9856cf29821a05e88b54811619441949; _tz_id=c528baa594cfdfaf5e93a86048b5c4f4; PHPSESSID=8h8jqnmeg1f2o5j03vo1nk7llr; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2224003%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A37%3A%22%2Frates-bonds%2Findia-3-month-bond-yield%22%3B%7D%7D%7D%7D; geoC=IN; adBlockerNewUserDomains=1619441951; gtmFired=OK; StickySession=id.6100660358.631in.investing.com; udid=f54e7210e8e3bc9b35a468ba65a8ad14; __cflb=02DiuF9qvuxBvFEb2qB1HcuDLvqD9ieP4QJ9YHcUfbsS4; G_ENABLED_IDPS=google; _fbp=fb.1.1619441955314.16268788; adsFreeSalePopUp=2; comment_notification_202451988=1; adsFreeSalePopUpa41d6b177ab422862f5e64f395319b37=1; r_p_s_n=1; smd=f54e7210e8e3bc9b35a468ba65a8ad14-1619454509; UserReactions=true; ses_id=ZSthIGJtNj4%2BempsN2YyMD5tN2g%2FPTs4Zm43PDA%2Fbng3I2RqYDc%2FeTE%2BbiBjYGZ6YmMyMjQ3YDA8PjJsNjZmN2UzYTRiZjY8PmtqMzdhMmE%2BPjdtPz87bWZlN2cwY24wNzdkZGBvP28xYm42Y2tmaGJwMi40cGBxPG4yYjZ3ZiFlamEgYjI2aj5gamA3MTJlPmo3ZT9tOzhmZzcyMGJudjd8; nyxDorf=ZWRmPDF5ZDo%2FaT02biNjY2IyYjgyK2dnMjBvaQ%3D%3D',
        }

        url = self.__config_details['t_bill_91']['full_url']

        req = requests.post(url, headers=headers, data=data)
        soup = BeautifulSoup(req.content, "lxml")
        table = soup.find('table', attrs={'id': 'curr_table'})
        df = pd.read_html(str(table))[0]

        # Step 3 : calculating the rate
        risk_free_return_rate = df['Price'].mean()

        return risk_free_return_rate