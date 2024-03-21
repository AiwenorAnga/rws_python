# Homework

Implement an application that will periodically scrape news servers and store headers and URL of its articles.
The application will store the data into its own DB, and it will publish a REST API which will allow for browsing 
articles' metadata by keywords. In case a news server is unavailable, the application should handle it gracefully.

If you're applying for a full-stack position, please include a simple web UI in React for browsing the articles' 
metadata by keywords.

Implement any tests needed for the application components.

For the implementation, we offer an app skeleton, where you need to fill in the remaining code. Requirements:
- Python 3.8+, `pip`
- docker and docker-compose

In case the app skeleton does not suit you, or you want to use a different infrastructure (e.g. minikube) or frameworks,
feel free to do it your own way.


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

Testing the REST API:

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


## Step by step
- scrape headers and URLs of articles from: `idnes.cz`, `ihned.cz`, `bbc.com`
    - implement in `app.news`
    - test with `python -m pytest -k news_test`
- scrape periodically (e.g. every minute); store new articles into DB (check uniqueness of article by its URL)
    - implement in `app.scraper`
    - test with `python -m pytest -k scraper_test`
- publish the following REST API which will allow to browse the stored articles by keywords
    - implement in `app.api`
    - test by HTTP call
    
    `POST /articles/find`

    
        {
            "keywords": ["monkey", "dog", "snail"]
        }
        
    Example result response for these keywords:

        {
            "articles: [
                { "text": "Big monkey got caught in London", "url": "https://www.bbc.com/..." },
                { "text": "Is this dog really cute?", "url": "https://www.bbc.com/..." },
                { "text": "Dog vs Snail – which is better?", "url": "https://www.bbc.com/..." }
            ]
        }
        
# Preferred frameworks and libraries for implementation
- web scraping: `requests`
- ORM: `sqlalchemy`
- web API: `flask` or `fastapi`
- HTML parsing, REST request validation, scheduling - your choice, we can recommend e.g. `beautifulsoup4`, `marshmallow`

# Submission
Bundle the repo with the completed app by command  `git bundle create rws-python-your_name.bundle --all` 
and send it to us according to the instructions from your hiring contact.
