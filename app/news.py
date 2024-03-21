"""
News scrapers.

This module defines a base class `NewsScraper` for web scraping news articles,
along with specific scraper implementations for Idnes, Ihned, and BBC websites.

The base class provides functionalities for fetching website content, parsing HTML
using BeautifulSoup, and handling basic error logging. Specific scraper classes
inherit from the base class and implement the `get_headers` method to scrape
article headers and URLs from their respective websites.
"""
from abc import abstractmethod
from dataclasses import dataclass
from typing import List
import logging
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import validators
logger = logging.getLogger(__name__)


@dataclass
class Article:
    """Represents an article from a news server."""
    header: str
    url: str

def check_url(url=None) -> bool:
        """
        Checks if the provided URL is valid.

        Args:
            url: The URL to validate

        Returns:
            True if the URL is valid, False otherwise.
        """        
        #pattern = "^https?://(?:[a-zA-Z0-9-\.]+\.)+[a-zA-Z]{2,}(?:[:\d]+)?(?:/[^\s]*)?$"    
        if url and isinstance(url, str) and validators.url(url)==True:
            return True
        else:
            return False

class NewsScraper:
    """
    Base class for web scraping news articles.

    This class defines an abstract method `get_headers` that needs to be
    implemented by specific scraper classes. It also provides helper methods
    for fetching and parsing website content, and basic error logging.
    """
    
    @abstractmethod
    def get_headers(self) -> List[Article]:     
        """
        Scrapes headers and URLs of articles from a website.

        This method needs to be implemented by specific scraper classes to
        extract article headers and URLs from their respective websites.

        Returns:
            A list of articles (Article class), where each article contains
            the header and URL of an article.
        """

    def get_soup(self, url):
        """
        Connects to the provided URL, fetches content, and parses it with BeautifulSoup.

        Args:
            url: The URL of the website to scrape.

        Returns:
            A BeautifulSoup object representing the parsed website content,
            or None if there's an error.                 
        """
        if not check_url(url):
            return None

        headers = {}                       
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:            
                logger.info(f"Successfully retrieved content of {url}.")
            else:
                logger.error(f"Error: Failed to retrieve content of {url}. Status code: {response.status_code}")              
                return None       
        except ConnectionError as e:
            logger.error(f"ConnectionError: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"{e}")
            return None
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        

class IdnesScraper(NewsScraper):
    """Scraper class for Idnes news website."""

    def get_headers(self) -> List[Article]:
        """
        Scrapes article headers and URLs from Idnes website.

        Implements the `get_headers` method to extract article data from Idnes.

        Returns:
            A list of articles (Article class) containing headers and URLs from Idnes.
        """        
        website_url = f"https://idnes.cz"
        soup = super().get_soup(website_url)
        articles = []

        if soup:
            for item in soup.find_all('a', href=True, attrs={"score-type": "Article"}):
                header = item.text.strip()
                url = item.get('href', None)
                if header and url and check_url(url)==True:
                    articles.append(Article(header=header, url=website_url))  
        
        logger.info(f"Articles from {website_url}: {len(articles)}")
        return articles
    

class IhnedScraper(NewsScraper):
    """Scraper class for Ihned news website."""

    def get_headers(self) -> List[Article]:
        """
        Scrapes article headers and URLs from Ihned website.

        Implements the `get_headers` method to extract article data from Ihned.

        Returns:
            A list of articles (Article class) containing headers and URLs from Ihned.
        """    
        website_url = f"https://ihned.cz"
        soup = super().get_soup(website_url)
        articles = []

        if soup:
            for item in soup.find_all('h3', attrs={"class": "article-title"}):
                header = item.text.strip()          
                link = item.find("a")
                if link:
                    url = link.get("href", None)
                    if header and url and check_url(url)==True:
                        articles.append(Article(header=header, url=url)) 

        logger.info(f"Articles from {website_url}: {len(articles)}")
        return articles
    

class BbcScraper(NewsScraper):
    """Scraper class for Bbc news website."""

    def get_headers(self) -> List[Article]: 
        """
        Scrapes article headers and URLs from Bbc website.

        Implements the `get_headers` method to extract article data from Bbc.

        Returns:
            A list of articles (Article class) containing headers and URLs from Bbc.
        """          
        website_url = f"https://bbc.com"        
        soup = super().get_soup(website_url)
        articles = []

        if soup:
            for item in soup.find_all('a', href=True, attrs={"data-testid": "internal-link"}):
                url = website_url+'/'+item['href']
                h2 = item.find("h2", attrs={"data-testid": "card-headline"})
                if h2:
                    header = h2.text.strip()
                    if header and url and check_url(url)==True:
                        articles.append(Article(header=header, url=url))            

        logger.info(f"Articles from {website_url}: {len(articles)}")
        return articles