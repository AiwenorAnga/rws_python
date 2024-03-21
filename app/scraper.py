"""
Web scraping service.

This script periodically retrieves news articles from configured servers,
extracting headers and URLs, and stores new articles in the database.

It leverages a list of scraper objects (e.g., IdnesScraper, IhnedScraper)
to fetch articles from different news sources. Errors encountered during
scraping are logged with details.
"""
import logging
import app.service
import time
from app.news import IdnesScraper, IhnedScraper, BbcScraper

logger = logging.getLogger(__name__)
SCRAPERS = [IdnesScraper(), IhnedScraper(), BbcScraper()]

def scrape_news():
    """Gets articles from news servers and saves new ones into our DB.    

    Logs informational messages about scraping and errors encountered
    with individual scrapers. Handles scraper errors gracefully,
    allowing continued operation
    """
    for scraper in SCRAPERS:
        logger.info(f"Scraping news using {type(scraper).__name__}")   
        try:   
            articles = scraper.get_headers()
            for article in articles:
                app.service.save_article_if_new(article)
        except Exception as e:
            logger.error(f"Scraper Errror: {type(scraper).__name__} : exit(){e}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='{asctime} {levelname:<8} {name}:{module}:{lineno} - {message}', style='{')    

    while True:
        scrape_news()
        time.sleep(10)