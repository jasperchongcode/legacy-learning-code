
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# for todays date
from datetime import date as dt
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# this function should return a dataframe with the average sentiment for each day, given an input of a link and a list of tickers
# create a function for yahoo next


class news_scraper:
    def __init__(self, tickers, avg_type='mean') -> None:
        self.tickers = tickers
        self.sentiment_analyser = SentimentIntensityAnalyzer()
        self.avg_type = avg_type

    def finvis(self):
        """
        Returns a dataframe with the average sentiment for each news day (for each ticker)

            Parameters:
                    tickers (list): a list of tickers to search
                    type (mean, sum): method of averageing the days

            Returns:
                    dataframe (DataFrame): pandas dataframe
        """
        finviz_url = "https://finviz.com/quote.ashx?t="

        news_tables = {}
        # id for the news table
        news_table_id = 'news-table'
        for ticker in self.tickers:
            url = finviz_url + ticker

            req = Request(url=url, headers={'user-agent': 'my-app'})
            response = urlopen(req)

            # now we have a http response object that can be parsed by beautiful soup
            html = BeautifulSoup(response, 'html')

            # we will now parse the html by the id for the table the news data is in
            news_table = html.find(id=news_table_id)
            # add to dict
            news_tables[ticker] = news_table

        parsed_data = []
        for ticker, news_table in news_tables.items():
            data = news_tables[ticker]
            rows = data.findAll('tr')

            # get all the titles and their timestamp
            for index, row in enumerate(rows):
                title = row.a.text
                date_data = row.td.text.strip().split(' ')

                if len(date_data) == 2:  # if there is a date and time
                    date = date_data[0]
                    time = date_data[1]

                else:  # if there is just a time
                    time = date_data[0]
                    # use the previous date as the date

                # get the date for today
                if date == 'Today':
                    date = dt.today().strftime('%b-%d-%y')

                parsed_data.append([ticker, date, time, title])

        # format the parsed data to be more useable
        df = pd.DataFrame(parsed_data, columns=[
                          'ticker', 'date', 'time', 'title'])

        def f(title): return self.sentiment_analyser.polarity_scores(
            title)['compound']
        df['compound'] = df['title'].apply(f)  # apply the lambda function

        df['date'] = pd.to_datetime(df.date).dt.date

        mean_df = df.groupby(['ticker', 'date']).agg(
            avg=('compound', self.avg_type))  # get the mean for each day
        mean_df = mean_df.unstack()  # turn the date into the top
        mean_df = mean_df.xs('avg', axis='columns').transpose()

        return mean_df
