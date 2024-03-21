"""
REST API for browsing articles' metadata by keywords.

This module defines a Flask application that implements a REST API for
browsing articles' metadata based on keywords provided by the user.

The API offers an endpoint `/articles/find` that accepts both POST requests.
The request body should be in JSON format and include a 'keywords' field containing
a list of strings representing the keywords to search for.

The API validates the request format and handles potential errors like missing fields,
invalid keyword types, or data parsing issues. It also handles cases where news servers
might be unavailable (implementation details depend on the `get_articles_with_keywords`
function).

Upon successful retrieval of articles matching the keywords, the API returns a JSON
response with a list of articles. Each article object contains the following fields:

- text: The header of the article.
- url: The URL of the article.
"""

from http import HTTPStatus

from flask import Flask, jsonify, request

from app import db
from app.service import get_articles_with_keywords
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["http://localhost:8000"], supports_credentials=True)


# noinspection PyUnusedLocal
@app.teardown_request
def remove_db_session(exception=None):
    """
    Removes the database session after each request.

    Ensures proper database session management by removing it after each request
    to avoid potential connection issues.
    """
    db.session.remove()


@app.route('/articles/find', methods=['POST'])
def find_articles():
    """
    Finds articles matching provided keywords.

    This function handles the `/articles/find` endpoint of the API. It validates
    the request format (JSON) and required fields (`keywords`).

    Returns:
        A JSON response containing a list of articles matching the keywords
        or an error message if the request is invalid or there's an error
        retrieving articles.
    """
    
    if not request.is_json:
        return jsonify({'error': 'Request have to be JSON.'}), HTTPStatus.UNSUPPORTED_MEDIA_TYPE
    
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])

        required_fields = ['keywords']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field '{field}.'")
            
        for keyword in keywords:    
            if not isinstance(keyword, str):
                raise ValueError("Keywords have to be string.")

    except ValueError as err:
        return jsonify({'error': str(err)}),HTTPStatus.UNPROCESSABLE_ENTITY
           
    return jsonify(
        {
            'articles': [
                {'text': i.header, 'url': i.url} for i in get_articles_with_keywords(keywords)
            ]
        }
    ), HTTPStatus.OK


if __name__ == '__main__':
    app.run(debug=True)
