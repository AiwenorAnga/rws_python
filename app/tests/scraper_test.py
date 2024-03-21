from typing import List
from app import scraper, db, news
from app.model import Article
from app.tests.config import session, clear_data
import logging


class FakeScraper(news.NewsScraper):
    def get_headers(self) -> List[news.Article]:
        return [news.Article(header='a', url='http://www.some-url.cz'),
                news.Article(header='b', url='http://www.some-url.cz')]


class FailingScraper(news.NewsScraper):
    def get_headers(self) -> List[news.Article]:
        raise Exception("Error when scraping")


def test_scrape_news(caplog, session, clear_data):
    # mock news scrapers and clean DB
    scraper.SCRAPERS = [FakeScraper(), FailingScraper()]

    # test
    scraper.scrape_news()

    # check
    articles = db.session.query(Article).all()        
    assert len(articles) == 1, "With two same URL only first Article should be saved"
    article = articles[0]
    assert article.header == 'a', "With two same URL only first Article should be saved"
    assert article.url == 'http://www.some-url.cz',  "URL should be saved"

    caplog.set_level(logging.ERROR)
    assert len(caplog.records) == 1, "FaillingScraper should write down exactly one ERROR logging"
    if len(caplog.records)==1:
        assert caplog.records[0].msg.startswith("Scraper Errror:") == True, "Error logging should start with Scraper Errror:"