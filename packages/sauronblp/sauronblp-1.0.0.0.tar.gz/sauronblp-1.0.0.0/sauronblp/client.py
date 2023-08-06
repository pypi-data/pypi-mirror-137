import requests

class Client(object):
    def __init__(self, end_point):
        self.end_point = end_point

    def get(self, func, params):
        params['function'] = func
        response = requests.get(self.end_point, params=params)
        jsn = response.json()
        return jsn['data']

    def bdp(self, tickers, flds, **kwargs) -> dict:
        """
        Bloomberg reference data

        Args:
            tickers: tickers
            flds: fields to query
            **kwargs: Bloomberg overrides

        Returns:
            dict
        """
        return self.get('bdp', {
            'tickers': tickers,
            'flds': flds,
            **kwargs
        })

    def bds(self, tickers, flds, use_port=False, **kwargs) -> dict:
        """
        Bloomberg block data

        Args:
            tickers: ticker(s)
            flds: field
            use_port: use PortfolioDataRequest
            **kwargs: other overrides for query

        Returns:
            dict
        """
        return self.get('bds', {
            'tickers': tickers,
            'flds': flds,
            'use_port': use_port,
            **kwargs
        })

    def bdh(self, tickers, flds=None, start_date=None, end_date='today', adjust=None, **kwargs) -> dict:
        """
        Bloomberg historical data

        Args:
            tickers: ticker(s)
            flds: field(s)
            start_date: start date
            end_date: end date - default today
            adjust: all, dvd, normal, abn (=abnormal), split, - or None
                    exact match of above words will adjust for corresponding events
                    Case 0: - no adjustment for dividend or split
                    Case 1: dvd or normal|abn will adjust for all dividends except splits
                    Case 2: adjust will adjust for splits and ignore all dividends
                    Case 3: all == dvd|split == adjust for all
                    Case 4: None == Bloomberg default OR use kwargs
            **kwargs: overrides

        Returns:
            dict
        """
        return self.get('bdh', {
            'tickers': tickers,
            'flds': flds,
            'start_date': start_date,
            'end_date': end_date,
            'adjust': adjust,
            **kwargs
        })

    def bdib(self, ticker: str, dt, session='allday', typ='TRADE', **kwargs) -> dict:
        """
        Bloomberg intraday bar data

        Args:
            ticker: ticker name
            dt: date to download
            session: [allday, day, am, pm, pre, post]
            typ: [TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID, BEST_ASK]
            **kwargs:
                ref: reference ticker or exchange
                     used as supplement if exchange info is not defined for ticker
                batch: whether is batch process to download data
                log: level of logs

        Returns:
            dict
        """
        return self.get('bdib', {
            'ticker': ticker,
            'dt': dt,
            'session': session,
            'typ': typ,
            **kwargs
        })

    def bdtick(self, ticker, dt, session='allday', time_range=None, types=None, **kwargs) -> dict:
        """
        Bloomberg tick data

        Args:
            ticker: ticker name
            dt: date to download
            session: [allday, day, am, pm, pre, post]
            time_range: tuple of start and end time (must be converted into UTC)
                        if this is given, dt and session will be ignored
            types: str or list, one or combinations of [
                TRADE, AT_TRADE, BID, ASK, MID_PRICE,
                BID_BEST, ASK_BEST, BEST_BID, BEST_ASK,
            ]

        Returns:
            dict
        """
        return self.get('bdtick', {
            'ticker': ticker,
            'dt': dt,
            'session': session,
            'time_range': time_range,
            'types': types,
            **kwargs
        })

    def earning(self, ticker, by='Product', typ='Revenue', ccy=None, level=None, **kwargs) -> dict:
        """
        Earning exposures by Geo or Products

        Args:
            ticker: ticker name
            by: [G(eo), P(roduct)]
            typ: type of earning, start with PG_ in Bloomberg FLDS - default Revenue
                Revenue - Revenue of the company
                Operating_Income - Operating Income (also named as EBIT) of the company
                Assets - Assets of the company
                Gross_Profit - Gross profit of the company
                Capital_Expenditures - Capital expenditures of the company
            ccy: currency of earnings
            level: hierarchy level of earnings

        Returns:
            dict
        """
        return self.get('earning', {
            'ticker': ticker,
            'by': by,
            'typ': typ,
            'ccy': ccy,
            'level': level,
            **kwargs
        })

    def dividend(self, tickers, typ='all', start_date=None, end_date=None, **kwargs) -> dict:
        """
        Bloomberg dividend / split history

        Args:
            tickers: list of tickers
            typ: dividend adjustment type
                all:       DVD_Hist_All
                dvd:       DVD_Hist
                split:     Eqy_DVD_Hist_Splits
                gross:     Eqy_DVD_Hist_Gross
                adjust:    Eqy_DVD_Adjust_Fact
                adj_fund:  Eqy_DVD_Adj_Fund
                with_amt:  DVD_Hist_All_with_Amt_Status
                dvd_amt:   DVD_Hist_with_Amt_Status
                gross_amt: DVD_Hist_Gross_with_Amt_Stat
                projected: BDVD_Pr_Ex_Dts_DVD_Amts_w_Ann
            start_date: start date
            end_date: end date
            **kwargs: overrides

        Returns:
            dict
        """
        return self.get('dividend', {
            'tickers': tickers,
            'typ': typ,
            'start_date': start_date,
            'end_date': end_date,
            **kwargs
        })

    def beqs(self, screen, asof=None, typ='PRIVATE', group='General', **kwargs) -> dict:
        """
        Bloomberg equity screening

        Args:
            screen: screen name
            asof: as of date
            typ: GLOBAL/B (Bloomberg) or PRIVATE/C (Custom, default)
            group: group name if screen is organized into groups

        Returns:
            dict
        """
        return self.get('beqs', {
            'screen': screen,
            'asof': asof,
            'typ': typ,
            'group': group,
            **kwargs
        })

    def active_futures(self, ticker: str, dt, **kwargs) -> str:
        """
        Active futures contract

        Args:
            ticker: futures ticker, i.e., ESA Index, Z A Index, CLA Comdty, etc.
            dt: date

        Returns:
            str: ticker name
        """
        return self.get('active_futures', {
            'ticker': ticker,
            'dt': dt,
            **kwargs
        })

    def fut_ticker(self, gen_ticker: str, dt, freq: str, **kwargs) -> str:
        """
        Get proper ticker from generic ticker

        Args:
            gen_ticker: generic ticker
            dt: date
            freq: futures contract frequency

        Returns:
            str: exact futures ticker
        """
        return self.get('fut_ticker', {
            'gen_ticker': gen_ticker,
            'dt': dt,
            'freq': freq,
            **kwargs
        })

    def turnover(self, tickers, flds='Turnover', start_date=None, end_date=None, ccy: str = 'USD', factor: float = 1e6):
        """
        Currency adjusted turnover (in million)

        Args:
            tickers: ticker or list of tickers
            flds: override flds,
            start_date: start date, default 1 month prior to end_date
            end_date: end date, default T - 1
            ccy: currency - 'USD' (default), any currency, or 'local' (no adjustment)
            factor: adjustment factor, default 1e6 - return values in millions

        Returns:
            dict
        """
        return self.get('turnover', {
            'tickers': tickers,
            'flds': flds,
            'start_date': start_date,
            'end_date': end_date,
            'ccy': ccy,
            'factor': factor,
        })
        