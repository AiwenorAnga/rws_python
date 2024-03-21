The application periodically scrape news servers and store headers and URL of its articles. DB for data storage is launched from docker.The application can run its own REST API, which allow browsing articles by keywords.
Simple web UI in React for browsing the articles' metadata by keywords. The link you can find written below.


## Gitlab BE
https://github.com/AiwenorAnga/rws_python

## Gitlab FE
https://github.com/AiwenorAnga/rws_react

For test reason is CORS accepted from http://localhost:8000


## Requirements:
- Python 3.12+, `pip`, `venv`, `pipenv`
- docker and docker-compose


## Setup
```bash
# Virtual env creation
python3.8 -m venv .venv

# Dependencies installation
.venv/bin/pip install -U pip
.venv/bin/pip install -U pipenv
.venv/bin/pipenv install

# Run docker container with DB
docker-compose down -t1
docker-compose up -d --build

# Create an empty DB
.venv/bin/python -m app.setup
```


## Launching the whole app
Components:

```bash
.venv/bin/python -m app.scraper
.venv/bin/python -m app.api
```


## Testing 
- `python -m pytest ./app/tests`
- Tests CLEAR DATA in DB

- `app.news` scrape headers and URLs of articles from: `idnes.cz`, `ihned.cz`, `bbc.com`
- test with `python -m pytest -k news_test`

- `app.scraper` scrape periodically, store new articles into DB (check uniqueness of article by its URL)
- test with `python -m pytest -k scraper_test`

- `service.test` - save and load article from DB
- test with `python -m pytest -k service_test`

- `app.api` publish the following REST API which will allow to browse the stored articles by keywords
- test by HTTP call
```bash
curl --request POST 'http://localhost:5000/articles/find' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "keywords": [
            "babiš",
            "prymul"
        ]
    }'
```
Example result:
{
    "articles: [
        { "text": "Big monkey got caught in London", "url": "https://www.bbc.com/..." },
        { "text": "Is this dog really cute?", "url": "https://www.bbc.com/..." },
        { "text": "Dog vs Snail – which is better?", "url": "https://www.bbc.com/..." }
    ]
}