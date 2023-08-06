import feedparser
from Shynatime import ShTime


class ShynaNews:
    """
    This will help in extract the news for the provided url. I have URL(s) stacked in database with their sources
    (TOI, Zee news)

    We have two method as per the sources:
    get_news_toi
    get_news_zee

    Define url at class level and call the function as per the URL source.
    """
    Sh_time = ShTime.ClassTime()
    url = ''
    news_item = {}

    def get_news_toi(self):
        news_feed = feedparser.parse(url_file_stream_or_string=self.url)
        entry = news_feed.entries
        for row in entry:
            for _ in row.items():
                news_date = str(row['published_parsed'].tm_year) + "-" + str(
                    row['published_parsed'].tm_mon) + "-" + str(row['published_parsed'].tm_mday)
                new_time = str(row['published_parsed'].tm_hour) + ":" + str(row['published_parsed'].tm_min) + ":" + str(
                    row['published_parsed'].tm_sec)
                if row['description'] == '':
                    row['description'] = 'Sorry, I have no description. Feel free to checkout the URL'
                    self.news_item[row['title']] = row['description'], row['id'], news_date, new_time
                else:
                    self.news_item[row['title']] = row['description'], row['id'], news_date, new_time
        return self.news_item

    def get_news_zee(self):
        news_feed = feedparser.parse(url_file_stream_or_string=self.url)
        entry = news_feed.entries
        for row in entry:
            for _ in row.items():
                news_date, news_time = self.Sh_time.get_date_and_time(text_string=row['published'])
                self.news_item[row['title']] = row['summary'], news_date, news_time
        return self.news_item
