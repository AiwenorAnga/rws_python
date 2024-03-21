from app.news import IdnesScraper, IhnedScraper, BbcScraper, NewsScraper, check_url
from unittest.mock import patch
import logging
import requests
import re
from app.news import check_url


def test_check_url():
    assert check_url(None) == False, "Invalid URL should return False"
    assert check_url({'test':1}) == False, "Invalid URL should return False"
    assert check_url('') == False, "Invalid URL should return False"
    assert check_url('invalid_url') == False, "Invalid URL should return False"
    assert check_url('https://invalid_url') == False, "Invalid URL should return False"
    assert check_url('https://www.valid.url') == True, "Valid URL should return True"
    assert check_url('https://valid.url') == True, "Valid URL should return True"
    assert check_url('http://valid.url') == True, "Valid URL should return True"


def test_get_soup_invalid_url():
    news_scraper = NewsScraper()
    assert news_scraper.get_soup(None) == None, "With ivalid URL should return False"
    assert news_scraper.get_soup('') == None, "With ivalid URL should return False"
    assert news_scraper.get_soup('http://invalid') == None, "With ivalid URL should return False"
    assert news_scraper.get_soup('invalid_url') == None, "With ivalid URL should return False"


class MockResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content


def test_get_soup_success():
    url = "https://www.idnes.cz"
    with patch("requests.get") as mock_get:
        mock_get.return_value = MockResponse(status_code=200, content=b"<html><body><h1>Hello World!</h1></body></html>")
        soup = NewsScraper().get_soup(url)
        assert soup is not None, "With valid url response should't be None"
        assert type(soup).__name__ == 'BeautifulSoup', "With valid url response should be of BeautifulSoup type"
        assert soup.find("h1").text == "Hello World!", "With valid url response should return tags soup"       


def test_get_soup_bad_status_code():
    url = "https://example.com/not-found"
    with patch("requests.get") as mock_get:
        mock_get.return_value = MockResponse(status_code=404, content="")
        soup = NewsScraper().get_soup(url)
        assert soup is None, "With a response other than 200 fnc should return None"


def test_get_soup_connection_error(caplog):
    caplog.set_level(logging.ERROR)
    soup = NewsScraper().get_soup('http://www.idneeeeeeeeeeeeeeeeeeeeee.ddcz')
    assert len(caplog.records) == 1, "Invalid URL should write down exactly one ERROR logging"
    if len(caplog.records)==1:
        assert caplog.records[0].msg.startswith("ConnectionError:") == True, "Error logging start with ConnectionError:"
    assert soup == None, "With ConnectionError fnc should return None"        


def test_get_soup_request_exception(caplog):
    caplog.set_level(logging.ERROR)
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Network Error")
        soup = NewsScraper().get_soup("https://www.example.com")
        assert soup is None, "With response problem fnc shoul return None"
        assert len(caplog.records) == 1, "Problem with response should be recorded as ERROR logging"
 

def check_provider(provider: NewsScraper):    
    articles = provider.get_headers()
    assert len(articles) > 0
    for a in articles:
        assert len(a.header) > 0 , "Header should not be shorter then 1 char"
        assert a.header.strip() == a.header, "Header should strip from spaces at the beginning and at the end of the string"
        assert re.fullmatch(r'http(s)?://.*', a.url), "Header should start with http(s)://"
        assert check_url(a.url) == True, f"Header ({a.url}) should be valid url"


def test_dtest_idnes():
    check_provider(IdnesScraper())


def test_dtest_ihned():
    check_provider(IhnedScraper())


def test_dtest_bbc():
    check_provider(BbcScraper())
